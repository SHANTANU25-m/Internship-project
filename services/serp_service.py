import requests
from config import SERPAPI_KEY

def fetch_jobs(keyword: str, location: str, num_pages: int = 1):
    print(f"Fetching {num_pages} pages of jobs for '{keyword}' in '{location}'...")
    url = "https://serpapi.com/search"
    all_jobs = []
    for page in range(num_pages):
        print(f" -> Fetching Page {page + 1}...")
        params = {
            "engine": "google_jobs",
            "q": keyword,
            "location": location,
            "api_key": SERPAPI_KEY,
            "start": page * 10
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            jobs_list = data.get("jobs_results", [])
            if not jobs_list: break
            all_jobs.extend(jobs_list)
        except requests.exceptions.HTTPError as e:
            print(f"SerpAPI Error: {e}")
            break
    return all_jobs
