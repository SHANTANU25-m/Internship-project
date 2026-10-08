import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")
