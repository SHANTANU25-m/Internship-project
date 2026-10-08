import sys
from services import job_service, match_service
from services.serp_provider import SerpAPIProvider
from services.exa_provider import ExaAPIProvider
from database import get_db_connection

def run_scraper():
    print("\n--- Start New Search ---")
    print("Select Provider:")
    print("1. SerpAPI (Google Jobs)")
    print("2. Exa API (Neural Web Search)")
    provider_choice = input("Choice: ")
    
    if provider_choice == '1':
        provider = SerpAPIProvider()
    elif provider_choice == '2':
        provider = ExaAPIProvider()
    else:
        print("Invalid choice.")
        return

    keyword = input("Enter Keyword (e.g., Python Developer): ")
    location = input("Enter Location (e.g., USA): ")
    
    raw_jobs = provider.fetch_jobs(keyword, location, num_pages=1)
    if not raw_jobs:
        print("0 results found.")
        return
        
    print(f"{len(raw_jobs)} results found.")
    
    parsed_jobs = [provider.normalize_job(raw) for raw in raw_jobs]
        
    # Trigger the massive SQL Transaction!
    job_service.save_search_results(keyword, location, provider.__class__.__name__, parsed_jobs)


def view_analytics():
    """Satisfies Section 11 and 16 Analytics Queries"""
    print("\n--- JOB MARKET REPORT ---")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Basic Stats
                cur.execute("SELECT COUNT(*) as c FROM jobs")
                print(f"Total Jobs: {cur.fetchone()['c']}")
                
                cur.execute("SELECT COUNT(*) as c FROM companies")
                print(f"Total Companies: {cur.fetchone()['c']}")
                
                # Q1: Return all Python jobs (title, company, location, URL, posted date)
                print("\n1. Recent Python Jobs:")
                cur.execute('''
                    SELECT j.title, c.name as company, j.location, j.job_url, j.posted_date 
                    FROM jobs j 
                    JOIN companies c ON j.company_id = c.id 
                    WHERE j.title ILIKE '%python%' 
                    LIMIT 3
                ''')
                for row in cur.fetchall():
                    print(f" - {row['title']} at {row['company']} ({row['location']})")
                
                # Q2: Return all jobs requiring PostgreSQL (Jobs -> Job_Skills -> Skills)
                print("\n2. Jobs Requiring PostgreSQL:")
                cur.execute('''
                    SELECT j.title, c.name as company
                    FROM jobs j
                    JOIN companies c ON j.company_id = c.id
                    JOIN job_skills js ON j.id = js.job_id
                    JOIN skills s ON js.skill_id = s.id
                    WHERE s.name ILIKE '%postgres%'
                    LIMIT 3
                ''')
                for row in cur.fetchall():
                    print(f" - {row['title']} at {row['company']}")

                # Q3: Companies with highest number of jobs
                print("\n3. Top Companies:")
                cur.execute('''
                    SELECT c.name, COUNT(j.id) as count 
                    FROM companies c 
                    JOIN jobs j ON c.id = j.company_id 
                    GROUP BY c.name ORDER BY count DESC LIMIT 5
                ''')
                for row in cur.fetchall():
                    print(f" - {row['name']}: {row['count']} jobs")

                # Q4: Top 10 skills by number of associated jobs
                print("\n4. Top Skills:")
                cur.execute('''
                    SELECT s.name, COUNT(js.job_id) as count 
                    FROM skills s 
                    JOIN job_skills js ON s.id = js.skill_id 
                    GROUP BY s.name ORDER BY count DESC LIMIT 5
                ''')
                for row in cur.fetchall():
                    print(f" - {row['name']}: {row['count']} jobs")

                # Q5: Return jobs requiring Python AND PostgreSQL
                print("\n5. Jobs Requiring Python AND PostgreSQL:")
                cur.execute('''
                    SELECT j.title, c.name as company
                    FROM jobs j
                    JOIN companies c ON j.company_id = c.id
                    WHERE j.id IN (
                        SELECT js.job_id FROM job_skills js JOIN skills s ON js.skill_id = s.id WHERE s.name ILIKE '%python%'
                    )
                    AND j.id IN (
                        SELECT js.job_id FROM job_skills js JOIN skills s ON js.skill_id = s.id WHERE s.name ILIKE '%postgres%'
                    )
                    LIMIT 3
                ''')
                for row in cur.fetchall():
                    print(f" - {row['title']} at {row['company']}")

                # Q6: Return job counts by location
                print("\n6. Top Locations:")
                cur.execute('''
                    SELECT location, COUNT(id) as count 
                    FROM jobs 
                    GROUP BY location ORDER BY count DESC LIMIT 5
                ''')
                for row in cur.fetchall():
                    print(f" - {row['location']}: {row['count']} jobs")

                # Q7: Jobs collected during specified date range (Last 7 days)
                print("\n7. Jobs scraped in the last 7 days:")
                cur.execute('''
                    SELECT COUNT(id) as count 
                    FROM jobs 
                    WHERE scraped_at >= NOW() - INTERVAL '7 days'
                ''')
                print(f" - {cur.fetchone()['count']} recent jobs")

                # Q8: Duplicate candidates based on normalized title + company + location
                print("\n8. Potential Duplicates (Title + Company + Location):")
                cur.execute('''
                    SELECT j.title, c.name as company, j.location, COUNT(*) as copies
                    FROM jobs j
                    JOIN companies c ON j.company_id = c.id
                    GROUP BY j.title, c.name, j.location
                    HAVING COUNT(*) > 1
                ''')
                dupes = cur.fetchall()
                if not dupes:
                    print(" - No duplicates found (Deduplication is working perfectly!)")
                for row in dupes:
                    print(f" - {row['title']} at {row['company']} ({row['location']}) - {row['copies']} copies")

    except Exception as e:
        print(f"Could not load analytics. Have you run any searches yet? Error: {e}")


def run_job_matcher():
    """Satisfies Section 17 Advanced Challenge"""
    print("\n--- ADVANCED CHALLENGE: JOB MATCHER ---")
    skills_input = input("Enter your skills separated by commas (e.g., Python, PostgreSQL, AWS): ")
    if not skills_input.strip():
        print("No skills entered.")
        return
        
    candidate_skills = [s.strip() for s in skills_input.split(',')]
    matches = match_service.calculate_job_matches(candidate_skills)
    
    if not matches:
        print("No jobs found with required skills to match against.")
        return
        
    print("\nTop 5 Job Matches:")
    for m in matches[:5]:
        print(f"{m['title']} at {m['company']} - {m['match_percentage']:.1f}% Match ({m['matched_count']}/{m['required_count']} skills)")

def start_server():
    import subprocess
    print("\n--- Starting FastAPI Server ---")
    print("API will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server.")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--reload"])
    except KeyboardInterrupt:
        print("\nServer stopped.")

def run_tests():
    import pytest
    print("\n--- Running Automated Test Suite ---")
    pytest.main(["-v", "tests/"])

def run_full_text_search():
    print("\n--- PostgreSQL Full-Text Search ---")
    query = input("Enter search query (e.g., Python & AWS): ")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Use PostgreSQL tsquery syntax
                cur.execute('''
                    SELECT j.title, c.name, j.location 
                    FROM jobs j 
                    JOIN companies c ON j.company_id = c.id 
                    WHERE j.text_search @@ to_tsquery('english', %s)
                    LIMIT 10
                ''', (query,))
                results = cur.fetchall()
                if not results:
                    print("No jobs found matching your complex query.")
                for row in results:
                    print(f" - {row['title']} at {row['name']} ({row['location']})")
    except Exception as e:
        print(f"Search failed. Have you applied the V2 schema? Error: {e}")

def cleanup_expired_jobs():
    from repositories.job_repository import mark_expired_jobs
    print("\n--- Running Job Expiry Cleanup ---")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                expired = mark_expired_jobs(cur, days=30)
                conn.commit()
                print(f"Successfully marked {expired} old jobs as expired (inactive).")
    except Exception as e:
        print(f"Cleanup failed: {e}")

def start_dashboard():
    import subprocess
    print("\n--- Starting Streamlit Dashboard ---")
    print("Dashboard will open in your browser.")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped.")

def start_scheduler():
    import subprocess
    print("\n--- Starting Background Scheduler ---")
    try:
        subprocess.run([sys.executable, "scheduler.py"])
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

def view_recent_jobs():
    print("\n--- Recent Jobs ---")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT j.title, c.name, j.location, j.scraped_at 
                    FROM jobs j 
                    JOIN companies c ON j.company_id = c.id 
                    ORDER BY j.scraped_at DESC LIMIT 10
                ''')
                results = cur.fetchall()
                for r in results:
                    print(f" - {r['title']} at {r['name']} ({r['location']})")
    except Exception as e:
        print(f"Error fetching recent jobs: {e}")

def search_jobs_by_skill():
    print("\n--- Search Jobs by Skill ---")
    skill_input = input("Enter skill (e.g., Python): ")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT j.title, c.name, j.location 
                    FROM jobs j 
                    JOIN companies c ON j.company_id = c.id 
                    JOIN job_skills js ON j.id = js.job_id
                    JOIN skills s ON js.skill_id = s.id
                    WHERE s.name ILIKE %s
                    LIMIT 10
                ''', (f"%{skill_input}%",))
                results = cur.fetchall()
                if not results: print("No jobs found for that skill.")
                for r in results:
                    print(f" - {r['title']} at {r['name']} ({r['location']})")
    except Exception as e:
        print(f"Error fetching jobs: {e}")

def search_jobs_by_company():
    print("\n--- Search Jobs by Company ---")
    company_input = input("Enter company name: ")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT j.title, c.name, j.location 
                    FROM jobs j 
                    JOIN companies c ON j.company_id = c.id 
                    WHERE c.name ILIKE %s
                    LIMIT 10
                ''', (f"%{company_input}%",))
                results = cur.fetchall()
                if not results: print("No jobs found for that company.")
                for r in results:
                    print(f" - {r['title']} at {r['name']} ({r['location']})")
    except Exception as e:
        print(f"Error fetching jobs: {e}")

def main():
    while True:
        print("\n=================================")
        print("     JOB INTELLIGENCE SYSTEM     ")
        print("=================================")
        print("1. Search Jobs (Run Scraper)")
        print("2. View Recent Jobs")
        print("3. Search Jobs by Skill")
        print("4. Search Jobs by Company")
        print("5. View Job Statistics (8 SQL Queries)")
        print("--- ADVANCED FEATURES & EXTENSIONS ---")
        print("6. Job Match Calculator (Advanced Challenge)")
        print("7. PostgreSQL Full-Text Search")
        print("8. Cleanup Expired Jobs")
        print("9. Start REST API Server (FastAPI)")
        print("10. Start Streamlit Dashboard")
        print("11. Start Automated Scheduler")
        print("12. Run Automated Tests (Pytest)")
        print("13. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1': run_scraper()
        elif choice == '2': view_recent_jobs()
        elif choice == '3': search_jobs_by_skill()
        elif choice == '4': search_jobs_by_company()
        elif choice == '5': view_analytics()
        elif choice == '6': run_job_matcher()
        elif choice == '7': run_full_text_search()
        elif choice == '8': cleanup_expired_jobs()
        elif choice == '9': start_server()
        elif choice == '10': start_dashboard()
        elif choice == '11': start_scheduler()
        elif choice == '12': run_tests()
        elif choice == '13':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
