from pydantic import BaseModel, Field
from typing import Optional, List

class JobBaseModel(BaseModel):
    title: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    level: Optional[str] = Field(default=None)
    job_type: Optional[str] = Field(default=None)
    employment_type: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    responsibilities: Optional[str] = Field(default=None)
    requirements: Optional[str] = Field(default=None)
    work_mode: Optional[str] = Field(default=None)
    relocation_required: Optional[bool] = Field(default=None)

class CompanyModel(BaseModel):
    name: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    department: Optional[str] = Field(default=None)
    company_size: Optional[str] = Field(default=None)
    company_type: Optional[str] = Field(default=None)
    culture: Optional[str] = Field(default=None)
    work_environment: Optional[str] = Field(default=None)
    product_type: Optional[str] = Field(default=None)
    client_type: Optional[str] = Field(default=None)
    government_contract: Optional[bool] = Field(default=None)

class LocationModel(BaseModel):
    country: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    office_location: Optional[str] = Field(default=None)

class SkillModel(BaseModel):
    name: str = Field(...)
    type: Optional[str] = Field(default=None)

class ExperienceEducationModel(BaseModel):
    min_experience: Optional[int] = Field(default=None)
    max_experience: Optional[int] = Field(default=None)
    education: Optional[str] = Field(default=None)
    degree: Optional[str] = Field(default=None)
    certification: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    professional_membership: Optional[str] = Field(default=None)

class CompensationModel(BaseModel):
    salary_min: Optional[int] = Field(default=None)
    salary_max: Optional[int] = Field(default=None)
    currency: Optional[str] = Field(default=None)
    bonus: Optional[str] = Field(default=None)
    signing_bonus: Optional[str] = Field(default=None)
    performance_bonus: Optional[str] = Field(default=None)
    commission: Optional[str] = Field(default=None)
    equity: Optional[str] = Field(default=None)
    rsu: Optional[str] = Field(default=None)
    stock_options: Optional[str] = Field(default=None)
    profit_sharing: Optional[str] = Field(default=None)

class EligibilityModel(BaseModel):
    work_authorization: Optional[str] = Field(default=None)
    visa_sponsorship: Optional[bool] = Field(default=None)
    h1b: Optional[bool] = Field(default=None)
    opt: Optional[bool] = Field(default=None)
    cpt: Optional[bool] = Field(default=None)
    green_card: Optional[bool] = Field(default=None)
    citizenship_requirement: Optional[str] = Field(default=None)
    security_clearance: Optional[str] = Field(default=None)
    background_check: Optional[bool] = Field(default=None)
    drug_testing: Optional[bool] = Field(default=None)

class BenefitModel(BaseModel):
    benefit_type: Optional[str] = Field(default=None)
    benefit_value: Optional[str] = Field(default=None)

class WorkConditionsModel(BaseModel):
    shift: Optional[str] = Field(default=None)
    working_hours: Optional[str] = Field(default=None)
    work_schedule: Optional[str] = Field(default=None)
    flexible_hours: Optional[bool] = Field(default=None)
    four_day_week: Optional[bool] = Field(default=None)
    weekend_work: Optional[bool] = Field(default=None)
    overtime: Optional[bool] = Field(default=None)
    on_call: Optional[bool] = Field(default=None)
    travel_required: Optional[bool] = Field(default=None)
    travel_frequency: Optional[str] = Field(default=None)

class CareerModel(BaseModel):
    career_growth: Optional[str] = Field(default=None)
    promotion_opportunities: Optional[str] = Field(default=None)
    training: Optional[str] = Field(default=None)
    mentorship: Optional[bool] = Field(default=None)
    professional_development: Optional[str] = Field(default=None)
    certification_support: Optional[bool] = Field(default=None)
    tuition_assistance: Optional[bool] = Field(default=None)
    management_opportunity: Optional[bool] = Field(default=None)

class WorkplaceModel(BaseModel):
    work_life_balance: Optional[str] = Field(default=None)
    flexible_workplace: Optional[bool] = Field(default=None)
    diversity: Optional[str] = Field(default=None)
    inclusion: Optional[str] = Field(default=None)
    accessibility: Optional[str] = Field(default=None)
    employee_friendly: Optional[bool] = Field(default=None)
    workplace_culture: Optional[str] = Field(default=None)

class ContractModel(BaseModel):
    contract_duration: Optional[str] = Field(default=None)
    contract_type: Optional[str] = Field(default=None)
    w2: Optional[bool] = Field(default=None)
    contract_to_hire: Optional[bool] = Field(default=None)
    direct_hire: Optional[bool] = Field(default=None)
    staffing_agency: Optional[bool] = Field(default=None)
    recruitment_type: Optional[str] = Field(default=None)

class JobOtherModel(BaseModel):
    equipment: Optional[str] = Field(default=None)
    company_laptop: Optional[bool] = Field(default=None)
    home_office: Optional[bool] = Field(default=None)
    internet_requirement: Optional[bool] = Field(default=None)
    driving_requirement: Optional[bool] = Field(default=None)
    application_method: Optional[str] = Field(default=None)
    employee_ownership: Optional[bool] = Field(default=None)
    esop: Optional[bool] = Field(default=None)
    union: Optional[bool] = Field(default=None)
    veteran_preference: Optional[bool] = Field(default=None)
    accessibility: Optional[str] = Field(default=None)

class StructuredJobIntelligence(BaseModel):
    """The master model for LLM structured output parsing."""
    job: JobBaseModel
    company: CompanyModel
    location: LocationModel
    skills: List[SkillModel]
    experience_education: ExperienceEducationModel
    compensation: CompensationModel
    eligibility: EligibilityModel
    benefits: List[BenefitModel]
    work_conditions: WorkConditionsModel
    career: CareerModel
    workplace: WorkplaceModel
    contract: ContractModel
    other: JobOtherModel
