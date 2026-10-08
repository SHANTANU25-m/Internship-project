def record_search(cur, keyword, location, source, count):
    query = "INSERT INTO searches (keyword, location, source, results_count) VALUES (%s, %s, %s, %s) RETURNING id"
    cur.execute(query, (keyword, location, source, count))
    return cur.fetchone()['id']

def link_job_to_search(cur, search_id, job_id):
    query = "INSERT INTO job_searches (search_id, job_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    cur.execute(query, (search_id, job_id))
