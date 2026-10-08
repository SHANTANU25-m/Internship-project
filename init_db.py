import psycopg
from config import DATABASE_URL

def init_database():
    try:
        # Connect strictly to the root database, without the default schema option
        conn = psycopg.connect(DATABASE_URL, autocommit=True)
        with conn.cursor() as cur:
            with open('schema.sql', 'r') as f:
                schema_sql = f.read()
            cur.execute(schema_sql)
            print("Database Schema successfully created!")
        conn.close()
    except Exception as e:
        print(f"Error initializing DB: {e}")

if __name__ == '__main__':
    init_database()
