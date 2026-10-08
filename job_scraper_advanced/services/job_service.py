from database import get_db_connection
from repositories import company_repository, job_repository, search_repository

def save_search_results(keyword, location, source, jobs):
    '''
    13. Transaction Requirement
    A single API result may require changes to companies, jobs, skills, job_skills, searches and job_searches. 
    These operations should be atomic.
    '''
    added_count = 0
    updated_skipped_count = 0
    
    # 1. Connect to DB
    with get_db_connection() as conn:
        try:
            # psycopg automatically starts a BEGIN transaction when executing queries on a fresh cursor
            with conn.cursor() as cur:
                # search insert
                search_id = search_repository.record_search(cur, keyword, location, source, len(jobs))
                
                for job in jobs:
                    # company insert/update
                    company_id = company_repository.find_or_create(cur, job['company_name'])
                    
                    # job insert/update
                    job_id, is_new = job_repository.insert_job(cur, company_id, job)
                    
                    # skill insert/update & job_skill insert (To be fully implemented)
                    # skill_extractor.extract_and_save(cur, job_id, job['description'])
                    
                    # job_search insert
                    search_repository.link_job_to_search(cur, search_id, job_id)
                    
                    if is_new:
                        added_count += 1
                    else:
                        updated_skipped_count += 1
                        
            # COMMIT - If all loop iterations succeed, we commit the entire transaction block
            conn.commit()
            print(f"Transaction successful. {added_count} new jobs added. {updated_skipped_count} skipped/updated.")
            
        except Exception as e:
            # ROLLBACK - If ANY error occurs (e.g. database disconnect, constraint violation), rollback everything
            conn.rollback()
            print(f"Transaction failed! Rolling back all changes. Error: {e}")
            raise e
