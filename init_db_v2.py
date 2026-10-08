import psycopg
from config import DATABASE_URL

def apply_v2_migrations():
    print("Applying V2 Migrations (Full-Text Search & Expiry)...")
    try:
        conn = psycopg.connect(DATABASE_URL, autocommit=True)
        with conn.cursor() as cur:
            with open('schema_v2.sql', 'r') as f:
                schema_sql = f.read()
            cur.execute(schema_sql)
            print("V2 Database Schema successfully applied!")
        conn.close()
    except Exception as e:
        print(f"Error applying migrations: {e}")

if __name__ == '__main__':
    apply_v2_migrations()
