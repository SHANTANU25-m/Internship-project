import psycopg
from config import DATABASE_URL

def check():
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'job_scraper';")
    print("job_scraper:", cur.fetchone())
    
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'content1';")
    print("content1:", cur.fetchone())
    
    conn.close()

if __name__ == "__main__":
    check()
