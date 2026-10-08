import re

def extract_salary(description: str):
    if not description: return None, None
    matches = re.findall(r'\$([\d,]+)[kK]?', description)
    if not matches: return None, None
    cleaned_numbers = []
    for match in matches:
        num = int(match.replace(',', ''))
        if num < 1000: num *= 1000
        cleaned_numbers.append(num)
    return (min(cleaned_numbers), max(cleaned_numbers)) if len(cleaned_numbers) > 1 else (cleaned_numbers[0], cleaned_numbers[0])

def normalize_serp_job(raw_job: dict):
    description = raw_job.get('description', '')
    salary_min, salary_max = extract_salary(description)
    apply_links = raw_job.get('apply_options', [])
    job_url = apply_links[0].get('link', '') if apply_links else 'Unknown URL'
    return {
        "title": raw_job.get('title', 'Unknown Title'),
        "company_name": raw_job.get('company_name', 'Unknown Company'),
        "location": raw_job.get('location', 'Unknown Location'),
        "description": description,
        "job_url": job_url,
        "source": "SerpAPI",
        "salary_min": salary_min,
        "salary_max": salary_max
    }
