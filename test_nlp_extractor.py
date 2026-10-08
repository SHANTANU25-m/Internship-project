from services.nlp_extractor import NLPExtractor

def main():
    sample_jd = """
    We’re looking for a Financial Analyst to join Datamine’s Finance team.
    You will need 2–5 years of experience in FP&A, Business Analysis, and Accounting.
    Strong Microsoft Excel and SQL skills are required. Experience with Power BI or Looker is a plus.
    Familiarity with python programming for data pipelines is highly desired.
    Must have excellent communication skills.
    """

    print("Initializing NLP Extractor...")
    extractor = NLPExtractor()
    
    print("\n--- Raw Chunks Extracted by SpaCy ---")
    raw_chunks = extractor.extract_raw_chunks(sample_jd)
    print(f"Found {len(raw_chunks)} potential skill candidates.")
    print("Samples:", raw_chunks[:10], "...")
    
    print("\n--- Standardized Skills via Sentence Transformers ---")
    skills = extractor.extract_job_skills(sample_jd)
    
    for skill in sorted(skills, key=lambda x: x['confidence_score'], reverse=True):
        print(f"Extracted '{skill['extracted_chunk']}' -> Mapped to [{skill['standardized_skill']}] (Confidence: {skill['confidence_score']})")

if __name__ == "__main__":
    main()
