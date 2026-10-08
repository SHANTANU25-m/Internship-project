from database import get_db_connection
from repositories import company_repository, job_repository, search_repository
from models.job_structured import (
    StructuredJobIntelligence, JobBaseModel, CompanyModel, LocationModel,
    SkillModel, ExperienceEducationModel, CompensationModel, EligibilityModel,
    BenefitModel, WorkConditionsModel, CareerModel, WorkplaceModel, ContractModel, JobOtherModel
)

def run():
    # Constructing the intelligence object based on the AI's analysis of the JD
    intelligence = StructuredJobIntelligence(
        job=JobBaseModel(
            title="AI Applications Engineer",
            category="Engineering",
            level="Mid-Senior",
            job_type="Full-time",
            employment_type="Full-time",
            description="We’re looking for an AI Applications Engineer to help drive Notion’s business transformation efforts...",
            responsibilities="Work with stakeholders to discover opportunities; Build and ship end‑to‑end AI solutions; Establish evaluation and production-readiness patterns; Create reusable components and tooling.",
            requirements="4-8 years of experience as Software Engineer or Data Engineer; Experience building AI-enabled applications in production; Strong production-readiness instincts; Systems and integration fluency.",
            work_mode="Hybrid",
            relocation_required=False
        ),
        company=CompanyModel(
            name="Notion",
            industry="Software Development",
            culture="Collaborative, intellectual curiosity, tinkering and discovery",
            work_environment="In-person Anchor Days (Mon, Tue, Thu)"
        ),
        location=LocationModel(
            city="San Francisco / New York City",
            country="United States"
        ),
        skills=[
            SkillModel(name="LLMs", type="Hard Skill"),
            SkillModel(name="Classical ML", type="Hard Skill"),
            SkillModel(name="Prompt Orchestration", type="Hard Skill"),
            SkillModel(name="APIs", type="Hard Skill"),
            SkillModel(name="Data Pipelines", type="Hard Skill"),
            SkillModel(name="Cursor", type="Tool"),
            SkillModel(name="Claude Code", type="Tool")
        ],
        experience_education=ExperienceEducationModel(
            min_experience=4,
            max_experience=8
        ),
        compensation=CompensationModel(
            salary_min=152000,
            salary_max=250000,
            currency="USD",
            equity="Competitive equity offered"
        ),
        eligibility=EligibilityModel(
            background_check=True
        ),
        benefits=[
            BenefitModel(benefit_type="Cash Compensation", benefit_value="Highly competitive"),
            BenefitModel(benefit_type="Equity", benefit_value="Yes"),
            BenefitModel(benefit_type="Benefits", benefit_value="Comprehensive")
        ],
        work_conditions=WorkConditionsModel(
            work_schedule="Hybrid (3 days in-office: Mon, Tue, Thu)"
        ),
        career=CareerModel(
            professional_development="Strategic partner to internal stakeholders, driving business transformation."
        ),
        workplace=WorkplaceModel(
            diversity="Equal opportunity employer, hiring from a wide range of backgrounds.",
            accessibility="Reasonable accommodations provided during application process."
        ),
        contract=ContractModel(
            contract_type="Full-time",
            w2=True
        ),
        other=JobOtherModel(
            application_method="Submit Application link"
        )
    )

    raw_data = {
        "title": "AI Applications Engineer",
        "company_name": "Notion",
        "location": "San Francisco or New York City",
        "source": "Manual Upload",
        "job_url": "https://notion.so/careers/ai-applications-engineer-upload"
    }

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create company
            company_id = company_repository.find_or_create(cur, "Notion", intelligence.company)
            
            # Create Job
            job_id = job_repository.insert_full_job(cur, company_id, intelligence, raw_data)
            
            print(f"Successfully analyzed and inserted job: 'AI Applications Engineer' at Notion! Job ID: {job_id}")
        conn.commit()

if __name__ == "__main__":
    run()
