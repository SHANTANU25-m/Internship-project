from database import get_db_connection
conn = get_db_connection()
cur = conn.cursor()
cur.execute('SELECT COUNT(*) as c FROM jobs')
print(f'Jobs: {cur.fetchone()[\
c\]}')
cur.execute('SELECT COUNT(*) as c FROM companies')
print(f'Companies: {cur.fetchone()[\
c\]}')
cur.execute('SELECT COUNT(*) as c FROM skills')
print(f'Skills: {cur.fetchone()[\
c\]}')
