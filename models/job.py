from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class JobCreate(BaseModel):
    """Pydantic schema to strictly validate normalized job data from any API."""
    title: str = Field(..., description="The job title")
    company_name: str = Field(..., description="The company hiring")
    location: str = Field(default="Unknown", description="The job location")
    description: str = Field(default="", description="The full job description")
    job_url: str = Field(..., description="The link to apply for the job")
    source: str = Field(..., description="The API provider that scraped this job")
    salary_min: Optional[int] = Field(default=None, description="Minimum salary extracted")
    salary_max: Optional[int] = Field(default=None, description="Maximum salary extracted")