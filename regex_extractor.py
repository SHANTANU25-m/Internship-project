import re
from collections import defaultdict

# 1. The massive Regex Pattern
regex_pattern = r"""(?ix)
(?P<job_title>
    \b(?:AI\s+Applications\s+Engineer|Software\s+Engineer|Data\s+Engineer)\b
)
|
(?P<company>
    \bNotion\b
)
|
(?P<experience>
    \b\d+\s*[-–]\s*\d+\s+years?\b
)
|
(?P<location>
    \b(?:San\s+Francisco|New\s+York\s+City)\b
)
|
(?P<departments>
    \b(?:GTM|Finance|People|Engineering|Data|Business)\b
)
|
(?P<ai_ml>
    \b(?:AI|LLMs?|classical\s+ML|ML|retrieval|evaluation|prompt\s+orchestration|tool\s+orchestration|human[-\s]+in[-\s]+the[-\s]+loop|AI[-\s]+enabled\s+applications)\b
)
|
(?P<programming_and_technical>
    \b(?:APIs?|data\s+pipelines|application\s+code|infrastructure|production\s+systems|production\s+readiness|quality\s+gates|observability|monitoring|incident\s+response|rollouts?|rollbacks?)\b
)
|
(?P<enterprise_tools>
    \b(?:CRM|finance|ticketing|HRIS)\b
)
|
(?P<ai_development_tools>
    \b(?:Cursor|Claude\s+Code|AI[-\s]+assisted\s+development\s+environments?)\b
)
|
(?P<evaluation_and_operations>
    \b(?:metrics|monitoring|evaluation|quality\s+gates|incident\s+response|rollout\s+plans?|real[-\s]+world\s+feedback|iterative\s+releases?)\b
)
|
(?P<security_privacy_governance>
    \b(?:security|privacy|governance|access\s+controls|PII\s+handling|vendor/tool\s+risk|auditability)\b
)
|
(?P<business_entities>
    \b(?:business\s+transformation|business\s+impact|business\s+outcomes|user\s+outcomes|business\s+workflows|strategic\s+partner|stakeholders?)\b
)
|
(?P<problem_solving>
    \b(?:problem\s+framing|ambiguous\s+problem\s+statements?|problem\s+solving|context|technical\s+solutions?|scoped\s+solutions?|actionable\s+business\s+outcomes?)\b
)
|
(?P<collaboration>
    \b(?:communication|collaboration|stakeholders?|technical\s+partners?|non[-\s]+technical\s+partners?|engineering\s+teams?|data\s+teams?|business\s+teams?)\b
)
|
(?P<data_entities>
    \b(?:data|data\s+readiness|data\s+pipelines|data\s+infrastructure|data\s+systems?)\b
)
|
(?P<production_entities>
    \b(?:production|production\s+systems|production\s+rollout|production\s+readiness|live\s+business\s+workflows|reliable\s+at\s+scale)\b
)
|
(?P<development_entities>
    \b(?:reusable\s+components?|tooling|templates?|playbooks?|application\s+code|AI[-\s]+driven\s+solutions?)\b
)
|
(?P<salary>
    \$\d{1,3}(?:,\d{3})*(?:\s*[-–]\s*\$\d{1,3}(?:,\d{3})*)?
    \s*(?:per\s+year|annually)?
)
|
(?P<compensation_benefits>
    \b(?:cash\s+compensation|equity|benefits)\b
)
|
(?P<work_schedule>
    \b(?:Mondays?|Tuesdays?|Thursdays?|Anchor\s+Days)\b
)
|
(?P<employment_information>
    \b(?:San\s+Francisco|New\s+York\s+City|office|offices|work\s+from\s+our\s+offices)\b
)
"""

# 2. Compile the regex pattern
regex = re.compile(regex_pattern, re.IGNORECASE | re.VERBOSE)

def extract_entities_from_jd(raw_text: str) -> dict:
    extracted_data = defaultdict(set)
    for match in regex.finditer(raw_text):
        group_name = match.lastgroup 
        matched_text = match.group(group_name).strip() 
        if group_name:
            extracted_data[group_name].add(matched_text)
    return {k: list(v) for k, v in extracted_data.items()}

# 3. Test it all at once!
if __name__ == "__main__":
    sample_jd_text = """
    We’re looking for an AI Applications Engineer to help drive Notion’s business transformation. 
    You need 4-8 years of experience. Expect to work with LLMs, Claude Code, and Python.
    For roles based in San Francisco, the estimated base salary range is $152,000 - $250,000 per year.
    We work from our offices on Mondays, Tuesdays and Thursdays.
    """
    
    results = extract_entities_from_jd(sample_jd_text)
    
    print("--- REGEX EXTRACTION RESULTS ---")
    for category, items in results.items():
        print(f"{category.upper()}: {', '.join(items)}")
