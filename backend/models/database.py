from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, UniqueConstraint, Index
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
    data_source_connections = relationship("DataSourceConnection", back_populates="msme")
    health_scores = relationship("HealthScore", back_populates="msme")
    gst_filings = relationship("GSTFiling", back_populates="msme")
    upi_transactions = relationship("UPITransaction", back_populates="msme")
    epfo_contributions = relationship("EPFOContribution", back_populates="msme")
    bank_statements = relationship("BankStatement", back_populates="msme")
    ingestion_runs = relationship("IngestionRun", back_populates="msme")
    normalized_facts = relationship("NormalizedFact", back_populates="msme")
    feature_snapshots = relationship("FeatureSnapshot", back_populates="msme")
    quality_issues = relationship("QualityIssue", back_populates="msme")
    gst_filing_facts = relationship("GSTFilingFact", back_populates="msme")
    upi_txn_facts = relationship("UPITxnFact", back_populates="msme")
    aa_bank_statement_facts = relationship("AABankStatementFact", back_populates="msme")
    epfo_contribution_facts = relationship("EPFOContributionFact", back_populates="msme")


class DataSourceConnection(Base):
    __tablename__ = "data_source_connections"
    __table_args__ = (
        UniqueConstraint("msme_id", "source_type", name="uq_msme_source_connection"),
    )

    id = Column(Integer, primary_key=True, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False)
    source_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    consent_id = Column(String(100))
    consent_artifact_id = Column(String(100))
    consent_expires_at = Column(DateTime)
    connected_at = Column(DateTime)
    last_sync_at = Column(DateTime)
    last_fetched_at = Column(DateTime)  # backward-compatible alias usage
    metadata_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    msme = relationship("MSME", back_populates="data_source_connections")
    ingestion_runs = relationship("IngestionRun", back_populates="connection")


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


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    data_source_connection_id = Column(Integer, ForeignKey("data_source_connections.id"))
    status = Column(String(20), nullable=False, default="pending", index=True)
    window_start = Column(DateTime)
    window_end = Column(DateTime)
    records_received = Column(Integer, default=0)
    records_valid = Column(Integer, default=0)
    error_summary = Column(Text)
    run_version = Column(Integer, default=1)
    coverage_score = Column(Float, default=0.0)
    recency_score = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    msme = relationship("MSME", back_populates="ingestion_runs")
    connection = relationship("DataSourceConnection", back_populates="ingestion_runs")
    raw_payloads = relationship("RawPayload", back_populates="ingestion_run")
    normalized_facts = relationship("NormalizedFact", back_populates="ingestion_run")
    quality_issues = relationship("QualityIssue", back_populates="ingestion_run")
    feature_snapshots = relationship("FeatureSnapshot", back_populates="ingestion_run")
    gst_filing_facts = relationship("GSTFilingFact", back_populates="ingestion_run")
    upi_txn_facts = relationship("UPITxnFact", back_populates="ingestion_run")
    aa_bank_statement_facts = relationship("AABankStatementFact", back_populates="ingestion_run")
    epfo_contribution_facts = relationship("EPFOContributionFact", back_populates="ingestion_run")


class RawPayload(Base):
    __tablename__ = "raw_payloads"
    __table_args__ = (
        UniqueConstraint("source", "source_record_id", "msme_id", name="uq_raw_payload_source_record_msme"),
        Index("idx_raw_payload_ingestion_run", "ingestion_run_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)
    source_record_id = Column(String(120), nullable=False)
    payload_json = Column(Text, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    checksum = Column(String(64), nullable=False)

    ingestion_run = relationship("IngestionRun", back_populates="raw_payloads")


class NormalizedFact(Base):
    __tablename__ = "normalized_facts"
    __table_args__ = (
        UniqueConstraint("source", "source_record_id", "msme_id", name="uq_normalized_fact_source_record_msme"),
        Index("idx_normalized_fact_msme_source_time", "msme_id", "source", "event_time"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)
    source_record_id = Column(String(120), nullable=False)
    event_time = Column(DateTime, nullable=False, index=True)
    amount = Column(Float)
    direction = Column(String(10))
    counterparty_id = Column(String(255))
    compliance_flag = Column(Boolean)
    metadata_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="normalized_facts")
    msme = relationship("MSME", back_populates="normalized_facts")


class FeatureSnapshot(Base):
    __tablename__ = "feature_snapshots"
    __table_args__ = (
        Index("idx_feature_snapshot_msme_period", "msme_id", "snapshot_period"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    snapshot_period = Column(String(20), nullable=False, index=True)
    snapshot_granularity = Column(String(20), nullable=False, default="monthly")
    window_3m_json = Column(Text)
    window_6m_json = Column(Text)
    window_12m_json = Column(Text)
    metrics_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="feature_snapshots")
    msme = relationship("MSME", back_populates="feature_snapshots")


class QualityIssue(Base):
    __tablename__ = "quality_issues"
    __table_args__ = (
        Index("idx_quality_issue_msme_source", "msme_id", "source"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"))
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)
    source_record_id = Column(String(120))
    issue_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False, default="medium")
    field_name = Column(String(100))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

    ingestion_run = relationship("IngestionRun", back_populates="quality_issues")
    msme = relationship("MSME", back_populates="quality_issues")


class GSTFilingFact(Base):
    __tablename__ = "gst_filing_facts"
    __table_args__ = (
        UniqueConstraint("msme_id", "filing_period", "return_type", name="uq_gst_fact_msme_period_type"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    filing_period = Column(String(10), nullable=False, index=True)
    filing_date = Column(DateTime)
    due_date = Column(DateTime)
    return_type = Column(String(20), nullable=False)
    taxable_turnover = Column(Float)
    tax_paid = Column(Float)
    itc_claimed = Column(Float)
    is_on_time = Column(Boolean)
    source_record_id = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="gst_filing_facts")
    msme = relationship("MSME", back_populates="gst_filing_facts")


class UPITxnFact(Base):
    __tablename__ = "upi_txn_facts"
    __table_args__ = (
        UniqueConstraint("msme_id", "source_record_id", name="uq_upi_fact_msme_source_record"),
        Index("idx_upi_fact_msme_txn_time", "msme_id", "transaction_time"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    transaction_time = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False)
    payer_vpa_hash = Column(String(64))
    payee_vpa_hash = Column(String(64))
    merchant_category = Column(String(80))
    reference_id = Column(String(80))
    is_success = Column(Boolean, default=True)
    source_record_id = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="upi_txn_facts")
    msme = relationship("MSME", back_populates="upi_txn_facts")


class AABankStatementFact(Base):
    __tablename__ = "aa_bank_statement_facts"
    __table_args__ = (
        UniqueConstraint("msme_id", "month", name="uq_aa_fact_msme_month"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    month = Column(String(10), nullable=False, index=True)
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
    source_record_id = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="aa_bank_statement_facts")
    msme = relationship("MSME", back_populates="aa_bank_statement_facts")


class EPFOContributionFact(Base):
    __tablename__ = "epfo_contribution_facts"
    __table_args__ = (
        UniqueConstraint("msme_id", "contribution_month", "challan_id", name="uq_epfo_fact_msme_month_challan"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=False)
    msme_id = Column(Integer, ForeignKey("msmes.id"), nullable=False, index=True)
    contribution_month = Column(String(10), nullable=False, index=True)
    due_date = Column(DateTime)
    payment_date = Column(DateTime)
    employee_contribution = Column(Float)
    employer_contribution = Column(Float)
    total_contribution = Column(Float)
    employee_count = Column(Integer)
    is_on_time = Column(Boolean)
    challan_id = Column(String(80), nullable=False)
    source_record_id = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingestion_run = relationship("IngestionRun", back_populates="epfo_contribution_facts")
    msme = relationship("MSME", back_populates="epfo_contribution_facts")


# Backward-compatible alias
DataSource = DataSourceConnection


def init_db():
    Base.metadata.create_all(bind=engine)
