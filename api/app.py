from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from services import job_service, match_service
from services.serp_provider import SerpAPIProvider
from services.exa_provider import ExaAPIProvider
from database import get_db_connection

app = FastAPI(
    title="Job Intelligence System API",
    description="REST API for scraping, storing, and analyzing job data.",
    version="1.0.0"
)

# Pydantic Schemas
class SearchRequest(BaseModel):
    keyword: str
    location: str
    provider: str = "serpapi" # "serpapi" or "exa"

class MatchRequest(BaseModel):
    skills: List[str]


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Job Intelligence API!",
        "docs_url": "http://localhost:8000/docs"
    }


@app.post("/search")
def search_jobs(request: SearchRequest):
    """Trigger the scraper remotely and run the atomic transaction."""
    try:
        if request.provider.lower() == "exa":
            provider = ExaAPIProvider()
        else:
            provider = SerpAPIProvider()

        raw_jobs = provider.fetch_jobs(request.keyword, request.location, num_pages=1)
        if not raw_jobs:
            return {"message": "0 results found."}
            
        parsed_jobs = [provider.normalize_job(raw) for raw in raw_jobs]
        
        # Trigger the massive SQL Transaction!
        job_service.save_search_results(request.keyword, request.location, provider.__class__.__name__, parsed_jobs)
        
        return {
            "message": f"Scraping ({provider.__class__.__name__}) and transaction successful!",
            "jobs_found": len(parsed_jobs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/match")
def get_job_matches(request: MatchRequest):
    """Send a list of skills and receive job match percentages."""
    try:
        matches = match_service.calculate_job_matches(request.skills)
        return {"matches": matches[:10]} # Return top 10 matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics")
def get_analytics():
    """Returns the complex SQL queries as a clean JSON payload."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Basic Stats
                cur.execute("SELECT COUNT(*) as c FROM jobs")
                total_jobs = cur.fetchone()['c']
                
                cur.execute("SELECT COUNT(*) as c FROM companies")
                total_companies = cur.fetchone()['c']
                
                # Top Skills
                cur.execute('''
                    SELECT s.name, COUNT(js.job_id) as count 
                    FROM skills s 
                    JOIN job_skills js ON s.id = js.skill_id 
                    GROUP BY s.name ORDER BY count DESC LIMIT 5
                ''')
                top_skills = cur.fetchall()
                
                # Top Companies
                cur.execute('''
                    SELECT c.name, COUNT(j.id) as count 
                    FROM companies c 
                    JOIN jobs j ON c.id = j.company_id 
                    GROUP BY c.name ORDER BY count DESC LIMIT 5
                ''')
                top_companies = cur.fetchall()
                
                return {
                    "overview": {
                        "total_jobs": total_jobs,
                        "total_companies": total_companies
                    },
                    "top_skills": top_skills,
                    "top_companies": top_companies
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
