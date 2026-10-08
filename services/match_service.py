from database import get_db_connection

def calculate_job_matches(candidate_skills: list):
    """
    Advanced Challenge: Job Matching
    Formula: matched_skills / required_skills * 100
    """
    candidate_skills_lower = [s.strip().lower() for s in candidate_skills]
    results = []
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get all jobs and their required skills
            query = '''
                SELECT j.id, j.title, c.name as company, string_agg(s.name, ',') as required_skills
                FROM jobs j
                JOIN companies c ON j.company_id = c.id
                JOIN job_skills js ON j.id = js.job_id
                JOIN skills s ON js.skill_id = s.id
                GROUP BY j.id, j.title, c.name
            '''
            cur.execute(query)
            jobs = cur.fetchall()
            
            for job in jobs:
                if not job['required_skills']:
                    continue
                    
                job_reqs = [s.strip().lower() for s in job['required_skills'].split(',')]
                required_count = len(job_reqs)
                
                # Count matches
                matched_count = 0
                for req in job_reqs:
                    if req in candidate_skills_lower:
                        matched_count += 1
                        
                if required_count > 0:
                    match_percentage = (matched_count / required_count) * 100
                    results.append({
                        'title': job['title'],
                        'company': job['company'],
                        'match_percentage': match_percentage,
                        'matched_count': matched_count,
                        'required_count': required_count
                    })
                    
    # Sort by match percentage descending
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results
