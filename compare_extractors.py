from regex_extractor import extract_entities_from_jd
from services.nlp_extractor import NLPExtractor
import logging
# Suppress spacy warnings
logging.getLogger("spacy").setLevel(logging.ERROR)

def main():
    sample_jd_text = """
    We’re looking for an AI Applications Engineer to help drive Notion’s business transformation. 
    You need 4-8 years of experience. Expect to work with LLMs, Claude Code, and Python.
    For roles based in San Francisco, the estimated base salary range is $152,000 - $250,000 per year.
    We work from our offices on Mondays, Tuesdays and Thursdays.
    """

    print("=== 1. REGEX EXTRACTOR OUTPUT ===")
    regex_results = extract_entities_from_jd(sample_jd_text)
    for category, items in regex_results.items():
        if items:
            print(f"{category.upper()}: {', '.join(items)}")

    print("\n=== 2. NLP (SPACY + SENTENCE TRANSFORMER) OUTPUT ===")
    extractor = NLPExtractor()
    skills = extractor.extract_job_skills(sample_jd_text)
    
    print("\nSkills Automatically Standardized by AI:")
    for skill in sorted(skills, key=lambda x: x['confidence_score'], reverse=True):
        print(f" - Found text '{skill['extracted_chunk']}' -> Mapped to Database Skill: [{skill['standardized_skill']}]")

if __name__ == "__main__":
    main()
