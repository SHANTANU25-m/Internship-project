from models.job_structured import StructuredJobIntelligence

def url_exists(cur, job_url: str) -> bool:
    cur.execute("SELECT job_id FROM content WHERE source_url = %s", (job_url,))
    return cur.fetchone() is not None

def insert_full_job(cur, company_id: int, intelligence: StructuredJobIntelligence, raw_data: dict) -> int:
    """Inserts a fully structured job across all tables."""
    
    # 1. Insert into jobs
    job = intelligence.job
    cur.execute('''
        INSERT INTO jobs (title, category, level, job_type, employment_type, description, 
                          responsibilities, requirements, company_id, location_id, work_mode, relocation_required)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s)
        RETURNING id
    ''', (
        job.title or raw_data.get('title'), job.category, job.level, job.job_type, job.employment_type,
        job.description, job.responsibilities, job.requirements, company_id,
        job.work_mode, job.relocation_required
    ))
    job_id = cur.fetchone()['id']

    # 2. Insert into content
    cur.execute('''
        INSERT INTO content (job_id, source, source_url, raw_jd)
        VALUES (%s, %s, %s, %s)
    ''', (job_id, raw_data.get('source'), raw_data.get('job_url'), raw_data.get('description')))

    # 3. Skills (handled by skill_repository usually, but we have structured skills)
    for skill in intelligence.skills:
        cur.execute("INSERT INTO skills (name, type) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING RETURNING id", (skill.name, skill.type))
        row = cur.fetchone()
        if row:
            skill_id = row['id']
        else:
            cur.execute("SELECT id FROM skills WHERE name = %s", (skill.name,))
            skill_id = cur.fetchone()['id']
            
        cur.execute("INSERT INTO job_skills (job_id, skill_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (job_id, skill_id))

    # 4. Compensation
    comp = intelligence.compensation
    cur.execute('''
        INSERT INTO job_compensation (job_id, salary_min, salary_max, currency, bonus, signing_bonus, performance_bonus, commission, equity, rsu, stock_options, profit_sharing)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, comp.salary_min, comp.salary_max, comp.currency, comp.bonus, comp.signing_bonus, comp.performance_bonus, comp.commission, comp.equity, comp.rsu, comp.stock_options, comp.profit_sharing))

    # 5. Experience / Education
    edu = intelligence.experience_education
    cur.execute('''
        INSERT INTO job_experience_education (job_id, min_experience, max_experience, education, degree, certification, language, professional_membership)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, edu.min_experience, edu.max_experience, edu.education, edu.degree, edu.certification, edu.language, edu.professional_membership))

    # 6. Benefits
    for benefit in intelligence.benefits:
        cur.execute("INSERT INTO job_benefits (job_id, benefit_type, benefit_value) VALUES (%s, %s, %s)", (job_id, benefit.benefit_type, benefit.benefit_value))

    # 7. Eligibility
    elg = intelligence.eligibility
    cur.execute('''
        INSERT INTO job_eligibility (job_id, work_authorization, visa_sponsorship, h1b, opt, cpt, green_card, citizenship_requirement, security_clearance, background_check, drug_testing)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, elg.work_authorization, elg.visa_sponsorship, elg.h1b, elg.opt, elg.cpt, elg.green_card, elg.citizenship_requirement, elg.security_clearance, elg.background_check, elg.drug_testing))

    # 8. Work Conditions
    wc = intelligence.work_conditions
    cur.execute('''
        INSERT INTO job_work_conditions (job_id, shift, working_hours, work_schedule, flexible_hours, four_day_week, weekend_work, overtime, on_call, travel_required, travel_frequency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, wc.shift, wc.working_hours, wc.work_schedule, wc.flexible_hours, wc.four_day_week, wc.weekend_work, wc.overtime, wc.on_call, wc.travel_required, wc.travel_frequency))

    # 9. Career
    car = intelligence.career
    cur.execute('''
        INSERT INTO job_career (job_id, career_growth, promotion_opportunities, training, mentorship, professional_development, certification_support, tuition_assistance, management_opportunity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, car.career_growth, car.promotion_opportunities, car.training, car.mentorship, car.professional_development, car.certification_support, car.tuition_assistance, car.management_opportunity))

    # 10. Workplace
    wp = intelligence.workplace
    cur.execute('''
        INSERT INTO job_workplace (job_id, work_life_balance, flexible_workplace, diversity, inclusion, accessibility, employee_friendly, workplace_culture)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, wp.work_life_balance, wp.flexible_workplace, wp.diversity, wp.inclusion, wp.accessibility, wp.employee_friendly, wp.workplace_culture))

    # 11. Contract
    ctr = intelligence.contract
    cur.execute('''
        INSERT INTO job_contract (job_id, contract_duration, contract_type, w2, contract_to_hire, direct_hire, staffing_agency, recruitment_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, ctr.contract_duration, ctr.contract_type, ctr.w2, ctr.contract_to_hire, ctr.direct_hire, ctr.staffing_agency, ctr.recruitment_type))

    # 12. Other
    oth = intelligence.other
    cur.execute('''
        INSERT INTO job_other (job_id, equipment, company_laptop, home_office, internet_requirement, driving_requirement, application_method, employee_ownership, esop, "union", veteran_preference, accessibility)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (job_id, oth.equipment, oth.company_laptop, oth.home_office, oth.internet_requirement, oth.driving_requirement, oth.application_method, oth.employee_ownership, oth.esop, oth.union, oth.veteran_preference, oth.accessibility))

    return job_id
