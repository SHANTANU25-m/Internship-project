# Internship Project: Advanced Job Intelligence Scraper 🚀

A production-grade Python backend system that scrapes, validates, deduplicates, and analyzes job listings from SerpAPI and Exa API.

## 🌟 Features (Advanced Rubric & Extensions)
- **Service-Repository Architecture**: Clean separation of concerns with atomic PostgreSQL transactions using `psycopg`.
- **Dual Providers**: Supports both SerpAPI (Google Jobs) and Exa Neural Web Search using a Common Provider Interface.
- **Pydantic Validation**: Strict data validation layer to catch broken API responses before database insertion.
- **Advanced Deduplication**: `ON CONFLICT` algorithms to seamlessly handle URL collisions.
- **PostgreSQL Full-Text Search**: Custom `tsvector` and `GIN` index for lightning-fast keyword searches.
- **Job Matcher Algorithm**: Advanced challenge implemented to calculate percentage matching `(matched_skills / required_skills) * 100`.
- **FastAPI REST Server**: Backend logic is exposed via HTTP endpoints.
- **Streamlit Dashboard**: Visual data analytics for Top Skills and Hiring Companies.
- **Automated Pytest Suite**: Full test coverage of NLP parsing and math algorithms.
- **Automated Background Scheduler**: Built-in cron-style scraping script.

## 🛠️ Tech Stack
- **Python 3.x**
- **PostgreSQL & Psycopg 3**
- **Pydantic**
- **FastAPI & Uvicorn**
- **Streamlit**
- **Pytest**
- **Tenacity (Exponential Backoff)**

---

## 🚀 Setup Instructions (For Grading)

### 1. Database Setup
1. Open pgAdmin.
2. Create a database named `job_intelligence`.
3. Open the pgAdmin Query Tool for that database.
4. Paste the contents of `schema.sql` and run it to build the core tables.

### 2. Environment Variables
1. Rename `.env.example` to `.env`.
2. Open `.env` and fill in your database credentials and API keys:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_intelligence
DB_USER=postgres
DB_PASSWORD=your_password
SERPAPI_KEY=your_serpapi_key
EXA_API_KEY=your_exa_key
```

### 3. Installation
Open your terminal and install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply Final Schema Upgrades (Full-Text Search & Expiry)
Run the migration script to add the V2 architecture to PostgreSQL:
```bash
python init_db_v2.py
```

### 5. Run the Automated Tests (Optional)
Run the unit test suite to verify the NLP parser and Matching algorithms:
```bash
pytest -v tests/
```

---

## 🖥️ Usage

Start the main CLI Application:
```bash
python main.py
```

### CLI Menu Options
1. **Search Jobs**: Scrape jobs using SerpAPI or Exa API. Enforces Pydantic validation and an atomic SQL transaction across 6 tables.
2. **View Recent Jobs**: Shows the 10 most recently scraped jobs.
3. **Search Jobs by Skill**: Performs a complex 4-table SQL JOIN to find jobs requiring a specific skill.
4. **Search Jobs by Company**: Filters jobs by company name.
5. **View Job Statistics**: Executes complex SQL grouping/aggregation queries to show market insights.
6. **Job Match Calculator**: Enter your skills to mathematically calculate your match % for local jobs.
7. **PostgreSQL Full-Text Search**: Uses `tsvector` to execute a lightning-fast keyword search.
8. **Cleanup Expired Jobs**: Flags jobs as inactive if they haven't been scraped in 30 days.
9. **Start REST API Server**: Hosts the backend locally via FastAPI. Access swagger docs at `http://localhost:8000/docs`.
10. **Start Streamlit Dashboard**: Opens a visual analytics dashboard in your web browser.
11. **Start Automated Scheduler**: Runs in the background and triggers a scrape every 12 hours.
12. **Run Automated Tests**: Triggers the `pytest` runner.
13. **Exit**: Closes the application.
