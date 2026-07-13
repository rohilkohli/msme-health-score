from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from models.database import (
    get_db, User, MSME, HealthScore,
    GSTFiling, UPITransaction, EPFOContribution, BankStatement
)
from models.schemas import HealthScoreResponse, HealthScoreHistory
from routers.auth import get_current_user
from services.scoring_engine import ScoringEngine

router = APIRouter()


@router.post("/compute/{msme_id}", response_model=HealthScoreResponse)
def compute_health_score(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    gst_filings = db.query(GSTFiling).filter(GSTFiling.msme_id == msme_id).all()
    upi_transactions = db.query(UPITransaction).filter(UPITransaction.msme_id == msme_id).all()
    epfo_contributions = db.query(EPFOContribution).filter(EPFOContribution.msme_id == msme_id).all()
    bank_statements = db.query(BankStatement).filter(BankStatement.msme_id == msme_id).all()

    engine = ScoringEngine()
    result = engine.compute_health_score(
        msme, gst_filings, upi_transactions, epfo_contributions, bank_statements
    )

    score_record = HealthScore(
        msme_id=msme_id,
        composite_score=result.composite_score,
        revenue_stability=result.dimensions["business_activity_growth"].score,
        cash_flow_health=result.dimensions["cashflow_strength_stability"].score,
        compliance_score=result.dimensions["compliance_formalization"].score,
        growth_trajectory=result.dimensions["transaction_quality_conduct"].score,
        repayment_capacity=result.dimensions["repayment_capacity_leverage"].score,
        category=result.category,
        risk_level=result.risk_level,
        ml_prediction_score=result.ml_prediction_score,
        feature_importance=json.dumps(result.feature_importance) if result.feature_importance else None,
        recommendations=json.dumps(result.recommendations),
        computed_at=datetime.utcnow(),
    )
    db.add(score_record)
    db.commit()

    return result


@router.get("/{msme_id}", response_model=HealthScoreResponse)
def get_health_score(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    latest_score = (
        db.query(HealthScore)
        .filter(HealthScore.msme_id == msme_id)
        .order_by(HealthScore.computed_at.desc())
        .first()
    )
    if not latest_score:
        raise HTTPException(status_code=404, detail="No health score computed yet. Use POST /compute first.")

    gst_filings = db.query(GSTFiling).filter(GSTFiling.msme_id == msme_id).all()
    upi_transactions = db.query(UPITransaction).filter(UPITransaction.msme_id == msme_id).all()
    epfo_contributions = db.query(EPFOContribution).filter(EPFOContribution.msme_id == msme_id).all()
    bank_statements = db.query(BankStatement).filter(BankStatement.msme_id == msme_id).all()

    engine = ScoringEngine()
    return engine.compute_health_score(
        msme, gst_filings, upi_transactions, epfo_contributions, bank_statements
    )


@router.get("/{msme_id}/history", response_model=HealthScoreHistory)
def get_score_history(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scores = (
        db.query(HealthScore)
        .filter(HealthScore.msme_id == msme_id)
        .order_by(HealthScore.computed_at.asc())
        .all()
    )
    if not scores:
        return HealthScoreHistory(scores=[], trend="stable", average_score=0)

    score_list = [
        {
            "composite_score": s.composite_score,
            "revenue_stability": s.revenue_stability,
            "cash_flow_health": s.cash_flow_health,
            "compliance_score": s.compliance_score,
            "growth_trajectory": s.growth_trajectory,
            "repayment_capacity": s.repayment_capacity,
            "category": s.category,
            "computed_at": s.computed_at.isoformat() if s.computed_at else None,
        }
        for s in scores
    ]

    avg_score = sum(s.composite_score for s in scores) / len(scores)

    if len(scores) >= 2:
        recent = scores[-1].composite_score
        previous = scores[-2].composite_score
        if recent > previous * 1.05:
            trend = "improving"
        elif recent < previous * 0.95:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    return HealthScoreHistory(scores=score_list, trend=trend, average_score=round(avg_score, 2))
