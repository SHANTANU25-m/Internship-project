import pytest
from services.serp_provider import SerpAPIProvider

@pytest.fixture
def provider():
    return SerpAPIProvider()

def test_salary_extraction_standard(provider):
    """Test standard salary extraction from description."""
    desc = "We are looking for a dev. Salary is $100k - $150k per year."
    min_sal, max_sal = provider._extract_salary(desc)
    
    assert min_sal == 100000
    assert max_sal == 150000

def test_salary_extraction_single(provider):
    """Test when only one salary number is provided."""
    desc = "Pays $120,000 annually."
    min_sal, max_sal = provider._extract_salary(desc)
    
    assert min_sal == 120000
    assert max_sal == 120000

def test_salary_extraction_no_salary(provider):
    """Test when no salary is mentioned."""
    desc = "Great benefits and culture! Apply now."
    min_sal, max_sal = provider._extract_salary(desc)
    
    assert min_sal is None
    assert max_sal is None

def test_normalize_job_serp(provider):
    """Test that a raw SerpAPI job is perfectly normalized into a Pydantic JobCreate object."""
    raw = {
        "title": "Data Engineer",
        "company_name": "Tech Corp",
        "location": "New York, NY",
        "description": "Python, SQL. $130k",
        "apply_options": [{"link": "https://example.com/apply"}]
    }
    
    normalized = provider.normalize_job(raw)
    
    # Assert against Pydantic object attributes, not dictionary keys
    assert normalized.title == "Data Engineer"
    assert normalized.company_name == "Tech Corp"
    assert normalized.salary_min == 130000
    assert normalized.job_url == "https://example.com/apply"
