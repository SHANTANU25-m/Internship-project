import psycopg
from config import DATABASE_URL

def fix_sequences():
    conn = psycopg.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    tables_with_sequences = [
        'companies', 'locations', 'jobs', 'skills', 'job_benefits', 'searches'
    ]
    
    for table in tables_with_sequences:
        try:
            # Sync the sequence to the maximum ID currently in the table
            cur.execute(f"SELECT setval('content1.{table}_id_seq', COALESCE((SELECT MAX(id) FROM content1.{table}), 1));")
            print(f"Sequence synced for {table}")
        except Exception as e:
            print(f"Error syncing {table}: {e}")
            
    conn.close()

if __name__ == "__main__":
    fix_sequences()
