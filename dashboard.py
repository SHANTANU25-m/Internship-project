import streamlit as st
import pandas as pd
from database import get_db_connection

st.set_page_config(page_title="Job Intelligence Dashboard", layout="wide")

st.title("📊 Job Intelligence Dashboard")
st.markdown("Advanced analytics powered by PostgreSQL")

# Connect to database and fetch data
@st.cache_data(ttl=60)
def fetch_data(query):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            # Use pandas to easily manipulate SQL results for Streamlit
            df = pd.DataFrame(cur.fetchall())
            return df

try:
    # 1. Total Metrics
    col1, col2, col3 = st.columns(3)
    
    total_jobs = fetch_data("SELECT COUNT(*) as c FROM jobs")
    col1.metric("Total Jobs Scraped", total_jobs.iloc[0]['c'])
    
    total_companies = fetch_data("SELECT COUNT(*) as c FROM companies")
    col2.metric("Total Companies", total_companies.iloc[0]['c'])
    
    total_skills = fetch_data("SELECT COUNT(*) as c FROM skills")
    col3.metric("Total Extracted Skills", total_skills.iloc[0]['c'])
    
    st.markdown("---")
    
    # 2. Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Top In-Demand Skills")
        skills_df = fetch_data('''
            SELECT s.name, COUNT(js.job_id) as count 
            FROM skills s 
            JOIN job_skills js ON s.id = js.skill_id 
            GROUP BY s.name ORDER BY count DESC LIMIT 10
        ''')
        if not skills_df.empty:
            st.bar_chart(data=skills_df, x='name', y='count')
            
    with col_chart2:
        st.subheader("Companies Hiring the Most")
        companies_df = fetch_data('''
            SELECT c.name, COUNT(j.id) as count 
            FROM companies c 
            JOIN jobs j ON c.id = j.company_id 
            GROUP BY c.name ORDER BY count DESC LIMIT 10
        ''')
        if not companies_df.empty:
            st.bar_chart(data=companies_df, x='name', y='count')

    st.markdown("---")
    st.subheader("Recent Jobs Data")
    recent_jobs = fetch_data('''
        SELECT j.title, c.name as company, j.location, j.scraped_at
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        ORDER BY j.scraped_at DESC LIMIT 50
    ''')
    st.dataframe(recent_jobs, use_container_width=True)

except Exception as e:
    st.error(f"Failed to load dashboard data. Have you run any searches yet? Error: {e}")
