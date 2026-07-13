from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    full_name: str = Field(..., description="Full name of the user")


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MSMERegister(BaseModel):
    business_name: str = Field(..., description="Name of the MSME business")
    gstin: str = Field(..., min_length=15, max_length=15, description="15-char GSTIN")
    pan: str = Field(..., min_length=10, max_length=10, description="PAN number")
    udyam_number: Optional[str] = Field(None, description="Udyam registration number")
    business_type: str = Field(..., description="Micro, Small, or Medium")
    industry: str = Field(..., description="Industry type")
    city: str = Field(..., description="City of operation")
    state: str = Field(..., description="State of operation")
    pincode: str = Field(..., min_length=6, max_length=6)
    annual_turnover: float = Field(..., description="Annual turnover in INR")
    employee_count: int = Field(..., ge=1)
    year_established: int = Field(..., ge=1900)
    upi_id: Optional[str] = None
    epfo_establishment_id: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None


class MSMEProfile(BaseModel):
    id: int
    business_name: str
    gstin: str
    pan: str
    udyam_number: Optional[str]
    business_type: str
    industry: str
    city: str
    state: str
    pincode: str
    annual_turnover: float
    employee_count: int
    year_established: int
    upi_id: Optional[str]
    epfo_establishment_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DataSourceConnect(BaseModel):
    msme_id: int
    source_type: str = Field(..., description="GST, UPI, EPFO, or Account Aggregator")
    consent_duration_months: int = Field(default=12, ge=1, le=24)


class DataSourceStatus(BaseModel):
    source_type: str
    status: str
    connected_at: Optional[datetime]
    last_fetched_at: Optional[datetime]


class DimensionScore(BaseModel):
    score: float = Field(..., ge=0, le=100)
    weight: float
    weighted_score: float
    sub_metrics: Dict[str, float]
    insights: List[str]
    trend_3m: str = "stable"
    trend_6m: str = "stable"
    trend_12m: str = "stable"


class HealthScoreResponse(BaseModel):
    msme_id: int
    composite_score: float = Field(..., ge=0, le=1000)
    category: str
    category_color: str
    risk_level: str
    dimensions: Dict[str, DimensionScore]
    ml_prediction_score: Optional[float]
    feature_importance: Optional[Dict[str, float]]
    computed_at: datetime
    recommendations: List[str]
    top_strengths: List[str] = []
    top_risks: List[str] = []
    reason_codes: List[Dict[str, Any]] = []
    data_confidence_index: Dict[str, float] = {}
    score_improvement_guidance: List[str] = []
    insufficient_data_flags: List[str] = []


class HealthScoreHistory(BaseModel):
    scores: List[Dict[str, Any]]
    trend: str
    average_score: float


class CreditAssessmentResponse(BaseModel):
    msme_id: int
    credit_ready: bool
    readiness_percentage: float
    max_recommended_loan: float
    recommended_products: List[Dict[str, Any]]
    strengths: List[str]
    weaknesses: List[str]
    action_items: List[Dict[str, str]]
    uli_eligibility: bool
    ocen_eligible_lenders: List[Dict[str, str]]


class DashboardStats(BaseModel):
    total_msmes: int
    avg_health_score: float
    score_distribution: Dict[str, int]
    top_industries: List[Dict[str, Any]]
    risk_distribution: Dict[str, int]
    data_coverage: Dict[str, float]


class PortfolioMetrics(BaseModel):
    total_portfolio_value: float
    avg_score: float
    median_score: float
    score_distribution: Dict[str, int]
    industry_breakdown: List[Dict[str, Any]]
    risk_concentration: Dict[str, float]
    trend_30d: float
    npa_probability: float
