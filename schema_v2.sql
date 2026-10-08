-- Advanced Architecture: V2 Schema Upgrades
-- Run this to apply the final Optional Extensions to the database!

SET search_path TO job_scraper;

-- 1. Job Expiry Handling
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP;

-- Set all current jobs to active
UPDATE jobs SET is_active = TRUE WHERE is_active IS NULL;

-- 2. PostgreSQL Full-Text Search (tsvector)
-- Add a calculated column for full-text searching
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS text_search tsvector 
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, ''))) STORED;

-- Create an index to make full-text search lightning fast!
CREATE INDEX IF NOT EXISTS idx_jobs_text_search ON jobs USING GIN (text_search);
