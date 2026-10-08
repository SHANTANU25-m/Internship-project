from database import get_db_connection
from repositories import company_repository, job_repository, search_repository
from models.job_structured import (
    StructuredJobIntelligence, JobBaseModel, CompanyModel, LocationModel,
    SkillModel, ExperienceEducationModel, CompensationModel, EligibilityModel,
    BenefitModel, WorkConditionsModel, CareerModel, WorkplaceModel, ContractModel, JobOtherModel
)

def run():
    intelligence = StructuredJobIntelligence(
        job=JobBaseModel(
            title="Financial Analyst",
            category="Finance",
            level="Mid-Level",
            job_type="Full-time",
            employment_type="Full-time",
            description="We’re looking for a Financial Analyst to join Datamine’s Finance team and help transform financial and business data into actionable insights...",
            responsibilities="Analyze financial and operational data; Prepare financial reports; Support budgeting and forecasting; Perform variance analysis; Build financial models; Develop dashboards; Automate reporting.",
            requirements="2–5 years of experience in Financial Analysis, FP&A, Business Analysis, Accounting; Strong Microsoft Excel skills; Strong SQL skills; Experience with Power BI, Tableau, or Looker; Bachelor’s degree in Finance, Accounting, Economics, Business.",
            work_mode="Flexible",
            relocation_required=False
        ),
        company=CompanyModel(
            name="Datamine",
            industry="Data & Analytics",
            culture="Data-driven, strategic decision-making, improving business performance",
            work_environment="Inclusive workplace, flexible work arrangements"
        ),
        location=LocationModel(
            city="Unknown",
            country="Unknown"
        ),
        skills=[
            SkillModel(name="Financial Analysis", type="Domain"),
            SkillModel(name="FP&A", type="Domain"),
            SkillModel(name="Accounting", type="Domain"),
            SkillModel(name="Microsoft Excel", type="Tool"),
            SkillModel(name="SQL", type="Language"),
            SkillModel(name="Power BI", type="Tool"),
            SkillModel(name="Tableau", type="Tool"),
            SkillModel(name="Looker", type="Tool"),
            SkillModel(name="ERP Systems", type="Tool"),
            SkillModel(name="CRM Systems", type="Tool"),
            SkillModel(name="Financial Modeling", type="Hard Skill"),
            SkillModel(name="Variance Analysis", type="Hard Skill")
        ],
        experience_education=ExperienceEducationModel(
            min_experience=2,
            max_experience=5,
            degree="Bachelor’s degree",
            education="Finance, Accounting, Economics, Business, Mathematics, Statistics"
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
        "title": "Financial Analyst",
        "company_name": "Datamine",
        "location": "Unknown",
        "source": "Manual Upload",
        "job_url": "https://datamine.com/careers/financial-analyst-upload-3"
    }

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            company_id = company_repository.find_or_create(cur, "Datamine", intelligence.company)
            job_id = job_repository.insert_full_job(cur, company_id, intelligence, raw_data)
            print(f"Successfully analyzed and inserted job: 'Financial Analyst' at Datamine! Job ID: {job_id}")
        conn.commit()

if __name__ == "__main__":
    run()
