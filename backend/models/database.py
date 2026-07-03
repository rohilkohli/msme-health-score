from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    msmes = relationship("MSME", back_populates="owner")


class MSME(Base):
    __tablename__ = "msmes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_name = Column(String(255), nullable=False)
    gstin = Column(String(15), unique=True, index=True)
    pan = Column(String(10), index=True)
    udyam_number = Column(String(20), unique=True)
    business_type = Column(String(50))
    industry = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(6))
    annual_turnover = Column(Float)
    employee_count = Column(Integer)
    year_established = Column(Integer)
    upi_id = Column(String(100))
    epfo_establishment_id = Column(String(50))
    bank_account_number = Column(String(20))
    ifsc_code = Column(String(11))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="msmes")
    data_sources = relationship("DataSource", back_populates="msme")
    health_scores = relationship("HealthScore", back_populates="msme")
    gst_filings = relationship("GSTFiling", back_populates="msme")
    upi_transactions = relationship("UPITransaction", back_populates="msme")
    epfo_contributions = relationship("EPFOContribution", back_populates="msme")
    bank_statements = relationship("BankStatement", back_populates="msme")


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    source_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    consent_id = Column(String(100))
    connected_at = Column(DateTime)
    last_fetched_at = Column(DateTime)
    metadata_json = Column(Text)

    msme = relationship("MSME", back_populates="data_sources")


class HealthScore(Base):
    __tablename__ = "health_scores"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    composite_score = Column(Float, nullable=False)
    revenue_stability = Column(Float)
    cash_flow_health = Column(Float)
    compliance_score = Column(Float)
    growth_trajectory = Column(Float)
    repayment_capacity = Column(Float)
    category = Column(String(30))
    risk_level = Column(String(20))
    ml_prediction_score = Column(Float)
    feature_importance = Column(Text)
    recommendations = Column(Text)
    computed_at = Column(DateTime, default=datetime.utcnow)

    msme = relationship("MSME", back_populates="health_scores")


class GSTFiling(Base):
    __tablename__ = "gst_filings"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    filing_period = Column(String(10))
    filing_date = Column(DateTime)
    due_date = Column(DateTime)
    return_type = Column(String(10))
    taxable_turnover = Column(Float)
    tax_paid = Column(Float)
    is_on_time = Column(Boolean)
    itc_claimed = Column(Float)
    filing_status = Column(String(20))

    msme = relationship("MSME", back_populates="gst_filings")


class UPITransaction(Base):
    __tablename__ = "upi_transactions"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(10))
    counterparty_vpa = Column(String(100))
    category = Column(String(50))
    reference_id = Column(String(50))
    is_credit = Column(Boolean)

    msme = relationship("MSME", back_populates="upi_transactions")


class EPFOContribution(Base):
    __tablename__ = "epfo_contributions"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    contribution_month = Column(String(10))
    due_date = Column(DateTime)
    payment_date = Column(DateTime)
    employee_contribution = Column(Float)
    employer_contribution = Column(Float)
    total_contribution = Column(Float)
    num_employees = Column(Integer)
    is_on_time = Column(Boolean)
    challan_number = Column(String(30))

    msme = relationship("MSME", back_populates="epfo_contributions")


class BankStatement(Base):
    __tablename__ = "bank_statements"

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    month = Column(String(10))
    opening_balance = Column(Float)
    closing_balance = Column(Float)
    total_credits = Column(Float)
    total_debits = Column(Float)
    num_credit_transactions = Column(Integer)
    num_debit_transactions = Column(Integer)
    avg_daily_balance = Column(Float)
    min_balance = Column(Float)
    max_balance = Column(Float)
    emi_outflows = Column(Float)
    salary_outflows = Column(Float)
    tax_outflows = Column(Float)

    msme = relationship("MSME", back_populates="bank_statements")


def init_db():
    Base.metadata.create_all(bind=engine)
