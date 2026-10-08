import psycopg
from config import DATABASE_URL

def migrate():
    conn = psycopg.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        print("Starting migration from job_scraper to content1...")
        
        tables = [
            'companies', 'locations', 'jobs', 'skills', 'job_skills',
            'job_experience_education', 'job_compensation', 'job_benefits',
            'job_eligibility', 'job_work_conditions', 'job_career',
            'job_workplace', 'job_contract', 'job_other', 'content',
            'searches', 'job_searches'
        ]

        for table in tables:
            print(f"Migrating {table}...")
            # We can use INSERT INTO content1.X SELECT * FROM job_scraper.X
            try:
                cur.execute(f"""
                    INSERT INTO content1.{table}
                    SELECT * FROM job_scraper.{table}
                    ON CONFLICT DO NOTHING;
                """)
                print(f"Successfully migrated {table}.")
            except Exception as e:
                print(f"Failed to migrate {table} (it might not exist or have conflicts): {e}")

        print("Migration complete!")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
