from regex_extractor import extract_entities_from_jd
from services.nlp_extractor import NLPExtractor
import logging
logging.getLogger("spacy").setLevel(logging.ERROR)

def main():
    # A completely new, unseen Job Description that the Regex is NOT hardcoded for
    new_jd_text = """
    Acme Corp is hiring a Senior Data Scientist in Austin, Texas.
    Required: 5+ years building machine learning pipelines, deep learning, and Natural Language Processing.
    Must be proficient in Python, PyTorch, and cloud platforms like Amazon Web Services.
    Salary: 160k - 180k. Remote work available.
    """

    print("=== 1. REGEX EXTRACTOR OUTPUT (ON UNSEEN JD) ===")
    regex_results = extract_entities_from_jd(new_jd_text)
    found_regex = False
    for category, items in regex_results.items():
        if items:
            found_regex = True
            print(f"{category.upper()}: {', '.join(items)}")
    
    if not found_regex:
        print("REGEX FOUND NOTHING! (Because it wasn't hardcoded for these specific words)")

    print("\n=== 2. NLP (SPACY + SENTENCE TRANSFORMER) OUTPUT (ON UNSEEN JD) ===")
    extractor = NLPExtractor()
    skills = extractor.extract_job_skills(new_jd_text)
    
    print("\nSkills Automatically Standardized by AI:")
    for skill in sorted(skills, key=lambda x: x['confidence_score'], reverse=True):
        print(f" - Found text '{skill['extracted_chunk']}' -> Mapped to Database Skill: [{skill['standardized_skill']}]")

if __name__ == "__main__":
    main()
