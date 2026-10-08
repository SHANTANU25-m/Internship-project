def insert_job(cur, company_id, job_data):
    # ON CONFLICT DO NOTHING deduplication
    query = '''
        INSERT INTO job_scraper.jobs (company_id, title, description, location, job_url, salary_min, salary_max)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (job_url) DO UPDATE SET is_active = TRUE
        RETURNING id
    '''
    cur.execute(query, (
        company_id, job_data.get('title'), job_data.get('description'), 
        job_data.get('location'), job_data.get('job_url'), 
        job_data.get('salary_min'), job_data.get('salary_max')
    ))
    row = cur.fetchone()
    if row:
        return row['id'], True
    else:
        # If no id returned, get the existing ID for linking
        cur.execute("SELECT id FROM job_scraper.jobs WHERE job_url = %s", (job_data.get('job_url'),))
        return cur.fetchone()['id'], False
