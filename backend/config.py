from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "MSME Financial Health Score"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./msme_health.db"

    SECRET_KEY: str = "idbi-innovate-2026-msme-health-score-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GST_API_BASE_URL: str = "https://sandbox.gst.gov.in/api/v1"
    EPFO_API_BASE_URL: str = "https://sandbox.epfo.gov.in/api/v1"
    AA_API_BASE_URL: str = "https://sandbox.accountaggregator.in/api/v1"

    SCORING_WEIGHTS: dict = {
        "cashflow_strength_stability": 0.25,
        "repayment_capacity_leverage": 0.20,
        "business_activity_growth": 0.15,
        "transaction_quality_conduct": 0.15,
        "compliance_formalization": 0.15,
        "resilience_risk_buffers": 0.10,
    }

    ML_MODEL_PATH: str = "ml/model_artifacts/health_score_model.joblib"
    ML_FEATURE_COLUMNS_PATH: str = "ml/model_artifacts/feature_columns.joblib"

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
