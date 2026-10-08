import requests
import re
import time
from typing import List
from config import SERPAPI_KEY
from services.base_provider import BaseProvider
from models.job import JobCreate
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class SerpAPIProvider(BaseProvider):
    """Implementation of the BaseProvider for SerpAPI."""
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def _fetch_page(self, url, params):
        """Helper method with Exponential Backoff Retry Logic"""
        response = requests.get(url, params=params, timeout=100)
        response.raise_for_status()
        return response.json()

    def fetch_jobs(self, keyword: str, location: str, num_pages: int = 1) -> List[dict]:
        print(f"Fetching {num_pages} pages from SerpAPI for '{keyword}' in '{location}'...")
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
                data = self._fetch_page(url, params)
                if "error" in data:
                    print(f"SerpAPI Error Message: {data['error']}")
                jobs_list = data.get("jobs_results", [])
                if not jobs_list: break
                all_jobs.extend(jobs_list)
                
                # Rate Limiting: Sleep to avoid hammering the API
                if page < num_pages - 1:
                    time.sleep(1.5)
            except Exception as e:
                print(f"SerpAPI Error after retries: {e}")
                break
        return all_jobs

    def normalize_job(self, raw_job: dict) -> JobCreate:
        description = raw_job.get('description', '')
        salary_min, salary_max = self._extract_salary(description)
        apply_links = raw_job.get('apply_options', [])
        job_url = apply_links[0].get('link', '') if apply_links else 'Unknown URL'
        
        # Pydantic will instantly validate these fields!
        return JobCreate(
            title=raw_job.get('title', 'Unknown Title'),
            company_name=raw_job.get('company_name', 'Unknown Company'),
            location=raw_job.get('location', 'Unknown Location'),
            description=description,
            job_url=job_url,
            source="SerpAPI",
            salary_min=salary_min,
            salary_max=salary_max
        )

    def _extract_salary(self, description: str):
        if not description: return None, None
        matches = re.findall(r'\$([\d,]+)[kK]?', description)
        if not matches: return None, None
        cleaned_numbers = []
        for match in matches:
            num = int(match.replace(',', ''))
            if num < 1000: num *= 1000
            cleaned_numbers.append(num)
        return (min(cleaned_numbers), max(cleaned_numbers)) if len(cleaned_numbers) > 1 else (cleaned_numbers[0], cleaned_numbers[0])
