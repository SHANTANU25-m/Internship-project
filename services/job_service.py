from database import get_db_connection
from repositories import company_repository, job_repository, search_repository
from typing import List
from models.job import JobCreate
from services.transformer import extract_job_intelligence

def save_search_results(keyword: str, location: str, source: str, parsed_jobs: List[JobCreate]):
    added_count = 0
    updated_skipped_count = 0
    
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                search_id = search_repository.record_search(cur, keyword, location, source, len(parsed_jobs))
                for job in parsed_jobs:
                    # 1. Check if job already exists via its URL in the content table
                    if job_repository.url_exists(cur, job.job_url):
                        updated_skipped_count += 1
                        continue
                        
                    # 2. Use Gemini to extract Structured Intelligence
                    print(f"Transforming unstructured JD via Gemini for: {job.title}...")
                    intelligence = extract_job_intelligence(job.description)
                    
                    if not intelligence:
                        print(f"Skipping {job.title} due to extraction failure.")
                        updated_skipped_count += 1
                        continue
                    
                    # 3. Insert or find Company
                    company_name = intelligence.company.name or job.company_name
                    company_id = company_repository.find_or_create(cur, company_name, intelligence.company)
                    
                    # 4. Insert the massively structured Job
                    raw_data = job.model_dump()
                    job_id = job_repository.insert_full_job(cur, company_id, intelligence, raw_data)
                    
                    # 5. Link job to search
                    search_repository.link_job_to_search(cur, search_id, job_id)
                    added_count += 1
                    
            conn.commit()
            print(f"Transaction successful! {added_count} new jobs structured and added. {updated_skipped_count} skipped/updated.")
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed! Rolling back all changes. Error: {e}")
            raise e
