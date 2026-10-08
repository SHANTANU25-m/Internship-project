import requests
import time
from typing import List
from config import EXA_API_KEY
from services.base_provider import BaseProvider
from models.job import JobCreate
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class ExaAPIProvider(BaseProvider):
    """Implementation of the BaseProvider for Exa API."""
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def _fetch_page(self, url, payload, headers):
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def fetch_jobs(self, keyword: str, location: str, num_pages: int = 1) -> List[dict]:
        print(f"Fetching {num_pages} pages from Exa API for '{keyword}' in '{location}'...")
        query = f"Job posting for {keyword} located in {location}"
        
        url = "https://api.exa.ai/search"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": EXA_API_KEY
        }
        
        all_jobs = []
        for page in range(num_pages):
            payload = {
                "query": query,
                "useAutoprompt": True,
                "type": "neural",
                "numResults": 10, # 10 per page
                "contents": {"text": True}
            }
            
            try:
                data = self._fetch_page(url, payload, headers)
                results = data.get("results", [])
                if not results: break
                all_jobs.extend(results)
                
                if page < num_pages - 1:
                    time.sleep(1.5)
            except Exception as e:
                print(f"Exa API Error after retries: {e}")
                break
                
        return all_jobs

    def normalize_job(self, raw_job: dict) -> JobCreate:
        # Exa returns web results, so we have to map them to our job schema
        description = raw_job.get('text', '')
        
        return JobCreate(
            title=raw_job.get('title', 'Unknown Title'),
            company_name="Various (Exa Web Result)", # Exa doesn't strictly parse company
            location="See Description", 
            description=description,
            job_url=raw_job.get('url', 'Unknown URL'),
            source="Exa API",
            salary_min=None,
            salary_max=None
        )
