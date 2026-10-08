from abc import ABC, abstractmethod
from typing import List
from models.job import JobCreate

class BaseProvider(ABC):
    """
    Abstract Base Class for API Providers.
    Enforces a strict interface that all providers MUST implement.
    """
    
    @abstractmethod
    def fetch_jobs(self, keyword: str, location: str, num_pages: int = 1) -> List[dict]:
        """Fetch raw job data from the external API."""
        pass

    @abstractmethod
    def normalize_job(self, raw_job: dict) -> JobCreate:
        """
        Normalize the raw API response into our standardized database format.
        Must return a validated Pydantic JobCreate object.
        """
        pass
