from database import get_db_connection
from repositories import company_repository, job_repository, search_repository
from models.job_structured import (
    StructuredJobIntelligence, JobBaseModel, CompanyModel, LocationModel,
    SkillModel, ExperienceEducationModel, CompensationModel, EligibilityModel,
    BenefitModel, WorkConditionsModel, CareerModel, WorkplaceModel, ContractModel, JobOtherModel
)

def run():
    # Constructing the intelligence object based on the AI's analysis of the second JD
    intelligence = StructuredJobIntelligence(
        job=JobBaseModel(
            title="Backend Developer",
            category="Engineering",
            level="Mid-Level",
            job_type="Full-time",
            employment_type="Full-time",
            description="We’re looking for a Backend Developer to help design, build, and operate reliable backend services that power our applications...",
            responsibilities="Design, develop, test, and maintain scalable backend services and APIs; Build RESTful APIs and integrations; Work with databases to design schemas, write efficient queries; Identify performance bottlenecks; Troubleshoot production issues.",
            requirements="2–5 years of experience in backend software development; Strong programming experience with Python, Java, Node.js, Go; Strong understanding of SQL and relational databases; Experience working with cloud platforms.",
            work_mode="Flexible",
            relocation_required=False
        ),
        company=CompanyModel(
            name="Confidential Company",
            industry="Technology",
            culture="Thoughtful engineering, strong collaboration, and continuous learning",
            work_environment="Inclusive workplace, flexible work arrangements"
        ),
        location=LocationModel(
            city="Unknown",
            country="Unknown"
        ),
        skills=[
            SkillModel(name="Python", type="Language"),
            SkillModel(name="Java", type="Language"),
            SkillModel(name="Node.js", type="Language"),
            SkillModel(name="Go", type="Language"),
            SkillModel(name="REST APIs", type="Hard Skill"),
            SkillModel(name="SQL", type="Hard Skill"),
            SkillModel(name="PostgreSQL", type="Tool"),
            SkillModel(name="MySQL", type="Tool"),
            SkillModel(name="NoSQL", type="Hard Skill"),
            SkillModel(name="MongoDB", type="Tool"),
            SkillModel(name="Redis", type="Tool"),
            SkillModel(name="Git", type="Tool"),
            SkillModel(name="JWT", type="Tool"),
            SkillModel(name="OAuth", type="Tool"),
            SkillModel(name="AWS", type="Cloud"),
            SkillModel(name="Azure", type="Cloud"),
            SkillModel(name="Google Cloud", type="Cloud"),
            SkillModel(name="Docker", type="Tool"),
            SkillModel(name="Kubernetes", type="Tool"),
            SkillModel(name="CI/CD", type="Hard Skill"),
            SkillModel(name="FastAPI", type="Tool"),
            SkillModel(name="Django", type="Tool")
        ],
        experience_education=ExperienceEducationModel(
            min_experience=2,
            max_experience=5
        ),
        compensation=CompensationModel(
            currency="USD"
        ),
        eligibility=EligibilityModel(
            background_check=True
        ),
        benefits=[
            BenefitModel(benefit_type="Healthcare", benefit_value="Health insurance"),
            BenefitModel(benefit_type="Retirement", benefit_value="Retirement plans"),
            BenefitModel(benefit_type="Paid Time Off", benefit_value="Paid time off"),
            BenefitModel(benefit_type="Perks", benefit_value="Flexible work arrangements"),
            BenefitModel(benefit_type="Career", benefit_value="Professional development opportunities")
        ],
        work_conditions=WorkConditionsModel(
            flexible_hours=True
        ),
        career=CareerModel(
            career_growth="Opportunities to work on systems from initial design through production deployment and ongoing improvement",
            professional_development="Professional development opportunities provided"
        ),
        workplace=WorkplaceModel(
            work_life_balance="Flexible work arrangements",
            diversity="Inclusive workplace and equal employment opportunities",
            accessibility="Reasonable accommodations may be provided throughout the application process"
        ),
        contract=ContractModel(
            contract_type="Full-time"
        ),
        other=JobOtherModel()
    )

    raw_data = {
        "title": "Backend Developer",
        "company_name": "Confidential Company",
        "location": "Unknown",
        "source": "Manual Upload",
        "job_url": "https://unknown.com/careers/backend-developer-upload-2"
    }

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create company
            company_id = company_repository.find_or_create(cur, "Confidential Company", intelligence.company)
            
            # Create Job
            job_id = job_repository.insert_full_job(cur, company_id, intelligence, raw_data)
            
            print(f"Successfully analyzed and inserted job: 'Backend Developer' at Confidential Company! Job ID: {job_id}")
        conn.commit()

if __name__ == "__main__":
    run()
