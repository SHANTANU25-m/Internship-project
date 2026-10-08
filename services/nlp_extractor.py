import spacy
from sentence_transformers import SentenceTransformer, util
import torch

class NLPExtractor:
    def __init__(self, standard_skills=None):
        print("Loading NLP models... This may take a moment the first time.")
        # Load SpaCy model for NER and chunking
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
            
        # Load Sentence Transformer model (lightweight, fast)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define a taxonomy of standard skills if none provided
        self.standard_skills = standard_skills or [
            "Python", "JavaScript", "React", "Node.js", "SQL", "PostgreSQL",
            "Machine Learning", "Data Engineering", "Data Analysis", "Artificial Intelligence",
            "AWS", "Docker", "Kubernetes", "Git", "Agile", "Communication", 
            "Problem Solving", "Leadership", "Financial Analysis", "Accounting",
            "Microsoft Excel", "Power BI", "Tableau", "Business Analysis"
        ]
        
        # Pre-compute embeddings for our standard skills taxonomy
        self.standard_skill_embeddings = self.encoder.encode(self.standard_skills, convert_to_tensor=True)
        print("Models loaded successfully!")

    def extract_raw_chunks(self, text: str) -> list[str]:
        """Extract potential skill chunks from text using SpaCy."""
        doc = self.nlp(text)
        
        candidates = set()
        # Extract Noun Chunks (e.g., "financial analysis", "machine learning")
        for chunk in doc.noun_chunks:
            # Filter out generic pronouns or very short words
            if len(chunk.text) > 2 and chunk.root.pos_ not in ["PRON", "DET"]:
                # Clean up determiners (e.g. "a python developer" -> "python developer")
                clean_text = " ".join([t.text for t in chunk if t.pos_ != "DET"])
                candidates.add(clean_text.lower().strip())
                
        # Extract specific Named Entities (Organizations, Products)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "PERSON"]:
                candidates.add(ent.text.lower().strip())
                
        return list(candidates)

    def standardize_skills(self, raw_chunks: list[str], threshold: float = 0.6) -> list[dict]:
        """Match raw text chunks to standard taxonomy using vector similarity."""
        if not raw_chunks:
            return []
            
        # Encode all candidates at once
        chunk_embeddings = self.encoder.encode(raw_chunks, convert_to_tensor=True)
        
        # Compute cosine similarities between candidates and standard taxonomy
        cosine_scores = util.cos_sim(chunk_embeddings, self.standard_skill_embeddings)
        
        matched_skills = []
        # Find the best match for each candidate
        for i, chunk in enumerate(raw_chunks):
            # Find the max score for this chunk against all standard skills
            best_score_idx = torch.argmax(cosine_scores[i]).item()
            best_score = cosine_scores[i][best_score_idx].item()
            
            if best_score >= threshold:
                matched_skills.append({
                    "extracted_chunk": chunk,
                    "standardized_skill": self.standard_skills[best_score_idx],
                    "confidence_score": round(best_score, 3)
                })
                
        # Deduplicate matches by standardized skill name (keeping highest confidence)
        unique_matches = {}
        for match in matched_skills:
            std_skill = match["standardized_skill"]
            if std_skill not in unique_matches or match["confidence_score"] > unique_matches[std_skill]["confidence_score"]:
                unique_matches[std_skill] = match
                
        return list(unique_matches.values())

    def extract_job_skills(self, jd_text: str) -> list[dict]:
        """End-to-end extraction from raw text to standardized skills."""
        # Step 1: Extract potential candidates (noun chunks & entities)
        raw_chunks = self.extract_raw_chunks(jd_text)
        
        # Step 2: Map them to standardized skills
        standardized = self.standardize_skills(raw_chunks, threshold=0.55)
        
        return standardized
