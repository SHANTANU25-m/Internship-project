import pytest
from unittest.mock import patch, MagicMock
from services import match_service

@patch('services.match_service.get_db_connection')
def test_calculate_job_matches(mock_get_db_connection):
    """Test the (matched_skills / required_skills) * 100 math formula."""
    
    # Mock the database cursor and its return value
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_get_db_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Simulate the DB returning a job that requires Python and PostgreSQL
    mock_cursor.fetchall.return_value = [
        {
            'id': 1,
            'title': 'Backend Developer',
            'company': 'Mock Inc',
            'required_skills': 'python,postgresql'
        }
    ]
    
    # Test 1: Perfect Match (2 out of 2)
    candidate_skills = ['Python', 'PostgreSQL', 'AWS']
    results = match_service.calculate_job_matches(candidate_skills)
    
    assert len(results) == 1
    assert results[0]['match_percentage'] == 100.0
    assert results[0]['matched_count'] == 2
    
    # Test 2: Partial Match (1 out of 2)
    candidate_skills = ['Python']
    results = match_service.calculate_job_matches(candidate_skills)
    
    assert results[0]['match_percentage'] == 50.0
    assert results[0]['matched_count'] == 1

    # Test 3: Zero Match (0 out of 2)
    candidate_skills = ['Java']
    results = match_service.calculate_job_matches(candidate_skills)
    
    assert results[0]['match_percentage'] == 0.0
    assert results[0]['matched_count'] == 0
