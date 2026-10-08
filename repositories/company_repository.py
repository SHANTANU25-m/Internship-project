def find_or_create(cur, name, company_intel=None):
    cur.execute("SELECT id FROM companies WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        return row['id']
        
    if company_intel:
        cur.execute('''
            INSERT INTO companies (name, industry, department, company_size, company_type, culture, work_environment, product_type, client_type, government_contract)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        ''', (
            name, company_intel.industry, company_intel.department, company_intel.company_size, company_intel.company_type,
            company_intel.culture, company_intel.work_environment, company_intel.product_type, company_intel.client_type, company_intel.government_contract
        ))
    else:
        cur.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", (name,))
        
    return cur.fetchone()['id']
