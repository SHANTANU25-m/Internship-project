def find_or_create(cur, name):
    cur.execute("SELECT id FROM skills WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        return row['id']
    cur.execute("INSERT INTO skills (name) VALUES (%s) RETURNING id", (name,))
    return cur.fetchone()['id']

def link_job_to_skill(cur, job_id, skill_id):
    query = "INSERT INTO job_skills (job_id, skill_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    cur.execute(query, (job_id, skill_id))

def extract_and_save_skills(cur, job_id, description):
    if not description: return
    desc_lower = description.lower()
    skill_keywords = {
        "Python": ["python", "django", "flask", "fastapi"],
        "PostgreSQL": ["postgres", "postgresql", "sql", "relational"],
        "AWS": ["aws", "cloud", "s3", "ec2"],
        "Docker": ["docker", "container", "kubernetes"]
    }
    for skill_name, keywords in skill_keywords.items():
        if any(keyword in desc_lower for keyword in keywords):
            skill_id = find_or_create(cur, skill_name)
            link_job_to_skill(cur, job_id, skill_id)
