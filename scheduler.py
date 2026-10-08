import schedule
import time
from services.serp_provider import SerpAPIProvider
from services.exa_provider import ExaAPIProvider
from services import job_service

def scrape_job(provider_type, keyword, location):
    print(f"\n[Scheduler] Triggering Automated Scrape: {keyword} in {location}")
    if provider_type == 'exa':
        provider = ExaAPIProvider()
    else:
        provider = SerpAPIProvider()
        
    try:
        raw_jobs = provider.fetch_jobs(keyword, location, num_pages=1)
        if raw_jobs:
            parsed_jobs = [provider.normalize_job(raw) for raw in raw_jobs]
            job_service.save_search_results(keyword, location, provider.__class__.__name__, parsed_jobs)
            print(f"[Scheduler] Successfully scraped {len(parsed_jobs)} jobs.")
        else:
            print("[Scheduler] 0 results found.")
    except Exception as e:
        print(f"[Scheduler] Scrape failed: {e}")

def run_scheduler():
    print("Starting Automated Scheduler...")
    print("Scraping 'Python Developer' in 'USA' every 12 hours.")
    
    # Schedule a scrape every 12 hours
    schedule.every(12).hours.do(scrape_job, 'serpapi', 'Python Developer', 'USA')
    
    # For testing, you can uncomment this to run it every 10 seconds:
    # schedule.every(10).seconds.do(scrape_job, 'serpapi', 'Python Developer', 'USA')
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_scheduler()
