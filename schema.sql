-- Database: job_intelligence
-- Schema: job_scraper
CREATE SCHEMA IF NOT EXISTS job_scraper;
SET search_path TO job_scraper;

-- 1. jobs - Core Job Information
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    level VARCHAR(100),
    job_type VARCHAR(100),
    employment_type VARCHAR(100),
    description TEXT,
    responsibilities TEXT,
    requirements TEXT,
    posting_date TIMESTAMP WITH TIME ZONE,
    start_date TIMESTAMP WITH TIME ZONE,
    company_id INTEGER,
    location_id INTEGER,
    work_mode VARCHAR(100),
    relocation_required BOOLEAN
);

-- 2. companies
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    industry VARCHAR(255),
    department VARCHAR(255),
    company_size VARCHAR(100),
    company_type VARCHAR(100),
    culture TEXT,
    work_environment TEXT,
    product_type VARCHAR(100),
    client_type VARCHAR(100),
    government_contract BOOLEAN
);

-- 3. locations
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    office_location VARCHAR(255)
);

-- Add Foreign Keys for jobs after tables are created
ALTER TABLE jobs 
    ADD CONSTRAINT fk_jobs_company FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_jobs_location FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL;

-- 4. skills
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(100)
);

-- 5. job_skills
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);

-- 6. job_experience_education
CREATE TABLE IF NOT EXISTS job_experience_education (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    min_experience INTEGER,
    max_experience INTEGER,
    education VARCHAR(255),
    degree VARCHAR(255),
    certification VARCHAR(255),
    language VARCHAR(255),
    professional_membership VARCHAR(255)
);

-- 7. job_compensation
CREATE TABLE IF NOT EXISTS job_compensation (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(10),
    bonus VARCHAR(255),
    signing_bonus VARCHAR(255),
    performance_bonus VARCHAR(255),
    commission VARCHAR(255),
    equity VARCHAR(255),
    rsu VARCHAR(255),
    stock_options VARCHAR(255),
    profit_sharing VARCHAR(255)
);

-- 8. job_benefits
CREATE TABLE IF NOT EXISTS job_benefits (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    benefit_type VARCHAR(100),
    benefit_value TEXT
);

-- 9. job_eligibility
CREATE TABLE IF NOT EXISTS job_eligibility (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    work_authorization VARCHAR(255),
    visa_sponsorship BOOLEAN,
    h1b BOOLEAN,
    opt BOOLEAN,
    cpt BOOLEAN,
    green_card BOOLEAN,
    citizenship_requirement VARCHAR(255),
    security_clearance VARCHAR(255),
    background_check BOOLEAN,
    drug_testing BOOLEAN
);

-- 10. job_work_conditions
CREATE TABLE IF NOT EXISTS job_work_conditions (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    shift VARCHAR(100),
    working_hours VARCHAR(100),
    work_schedule VARCHAR(100),
    flexible_hours BOOLEAN,
    four_day_week BOOLEAN,
    weekend_work BOOLEAN,
    overtime BOOLEAN,
    on_call BOOLEAN,
    travel_required BOOLEAN,
    travel_frequency VARCHAR(100)
);

-- 11. job_career
CREATE TABLE IF NOT EXISTS job_career (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    career_growth TEXT,
    promotion_opportunities TEXT,
    training TEXT,
    mentorship BOOLEAN,
    professional_development TEXT,
    certification_support BOOLEAN,
    tuition_assistance BOOLEAN,
    management_opportunity BOOLEAN
);

-- 12. job_workplace
CREATE TABLE IF NOT EXISTS job_workplace (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    work_life_balance TEXT,
    flexible_workplace BOOLEAN,
    diversity TEXT,
    inclusion TEXT,
    accessibility TEXT,
    employee_friendly BOOLEAN,
    workplace_culture TEXT
);

-- 13. job_contract
CREATE TABLE IF NOT EXISTS job_contract (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    contract_duration VARCHAR(100),
    contract_type VARCHAR(100),
    w2 BOOLEAN,
    contract_to_hire BOOLEAN,
    direct_hire BOOLEAN,
    staffing_agency BOOLEAN,
    recruitment_type VARCHAR(100)
);

-- 14. job_other
CREATE TABLE IF NOT EXISTS job_other (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    equipment TEXT,
    company_laptop BOOLEAN,
    home_office BOOLEAN,
    internet_requirement BOOLEAN,
    driving_requirement BOOLEAN,
    application_method VARCHAR(100),
    employee_ownership BOOLEAN,
    esop BOOLEAN,
    "union" BOOLEAN,
    veteran_preference BOOLEAN,
    accessibility TEXT
);

-- 15. content
CREATE TABLE IF NOT EXISTS content (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    source VARCHAR(100),
    source_url TEXT,
    raw_jd TEXT,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Legacy/App requirements preserved (Not in PDF but required for app logic)
CREATE TABLE IF NOT EXISTS searches (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    source VARCHAR(50),
    searched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    results_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS job_searches (
    search_id INTEGER REFERENCES searches(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    PRIMARY KEY (search_id, job_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_company_id ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_location_id ON jobs(location_id);
CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(name);
