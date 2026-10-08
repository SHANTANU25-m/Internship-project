import os
import json
from google import genai
from google.genai import types
from models.job_structured import StructuredJobIntelligence

def extract_job_intelligence(raw_jd: str) -> StructuredJobIntelligence:
    """Uses Gemini 2.5 Structured Outputs to extract intelligence from raw job text."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Returning empty intelligence.")
        return None
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert HR analyst and data extraction system.
    Please extract the structured job intelligence from the following job description.
    Map it precisely to the provided JSON schema. If information is missing or unclear, leave it as null/None.
    
    JOB DESCRIPTION:
    {raw_jd}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StructuredJobIntelligence,
            temperature=0.0
        ),
    )
    
    if response.text:
        parsed_dict = json.loads(response.text)
        return StructuredJobIntelligence(**parsed_dict)
    
    return None
