from services.serp_provider import SerpAPIProvider
from services.job_service import save_search_results

def test_scraper():
    print("--- Testing Live Scraper ---")
    provider = SerpAPIProvider()
    
    keyword = "Software Engineer"
    location = "San Francisco"
    
    print(f"Fetching jobs for '{keyword}' in '{location}' from Google Jobs (via SerpAPI)...")
    
    # Fetch just 1 page to test
    raw_jobs = provider.fetch_jobs(keyword, location, num_pages=1)
    
    if not raw_jobs:
        print("0 results found. Check your SerpAPI Key.")
        return
        
    print(f"Success! {len(raw_jobs)} live jobs scraped from the internet.")
    
    # Print the first job to prove it works
    first_job = raw_jobs[0]
    print("\n--- FIRST JOB PREVIEW ---")
    print(f"Title: {first_job.get('title')}")
    print(f"Company: {first_job.get('company_name')}")
    print(f"Location: {first_job.get('location')}")
    
    print("\nNote: Moving to the Database Transformation step...")
    parsed_jobs = [provider.normalize_job(raw) for raw in raw_jobs]
    
    # This will trigger Gemini transformation. If no API key, it will skip saving.
    save_search_results(keyword, location, "SerpAPI", parsed_jobs)

if __name__ == "__main__":
    test_scraper()
