def find_or_create(cur, name):
    cur.execute("SELECT id FROM job_scraper.companies WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        return row['id']
    cur.execute("INSERT INTO job_scraper.companies (name) VALUES (%s) RETURNING id", (name,))
    return cur.fetchone()['id']
