from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from models.database import get_db, User, MSME, HealthScore
from models.schemas import DashboardStats, PortfolioMetrics
from routers.auth import get_current_user

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_msmes = db.query(MSME).count()

    scores = db.query(HealthScore).order_by(HealthScore.computed_at.desc()).all()
    seen_msmes = set()
    latest_scores = []
    for s in scores:
        if s.msme_id not in seen_msmes:
            seen_msmes.add(s.msme_id)
            latest_scores.append(s)

    avg_score = sum(s.composite_score for s in latest_scores) / len(latest_scores) if latest_scores else 0

    distribution = {"Excellent": 0, "Good": 0, "Fair": 0, "Needs Improvement": 0, "Critical": 0}
    for s in latest_scores:
        if s.category in distribution:
            distribution[s.category] += 1

    msmes = db.query(MSME).all()
    industry_counts = Counter(m.industry for m in msmes if m.industry)
    top_industries = [
        {"industry": ind, "count": cnt}
        for ind, cnt in industry_counts.most_common(5)
    ]

    risk_dist = {"Low": 0, "Moderate": 0, "High": 0, "Very High": 0}
    for s in latest_scores:
        if s.risk_level in risk_dist:
            risk_dist[s.risk_level] += 1

    scored_count = len(latest_scores)
    data_coverage = {
        "scored": scored_count / total_msmes * 100 if total_msmes > 0 else 0,
        "gst_connected": 85.0,
        "upi_connected": 78.0,
        "epfo_connected": 72.0,
        "aa_connected": 68.0,
    }

    return DashboardStats(
        total_msmes=total_msmes,
        avg_health_score=round(avg_score, 1),
        score_distribution=distribution,
        top_industries=top_industries,
        risk_distribution=risk_dist,
        data_coverage=data_coverage,
    )


@router.get("/portfolio", response_model=PortfolioMetrics)
def get_portfolio_metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scores = db.query(HealthScore).order_by(HealthScore.computed_at.desc()).all()
    seen_msmes = set()
    latest_scores = []
    for s in scores:
        if s.msme_id not in seen_msmes:
            seen_msmes.add(s.msme_id)
            latest_scores.append(s)

    if not latest_scores:
        return PortfolioMetrics(
            total_portfolio_value=0,
            avg_score=0,
            median_score=0,
            score_distribution={"Excellent": 0, "Good": 0, "Fair": 0, "Needs Improvement": 0, "Critical": 0},
            industry_breakdown=[],
            risk_concentration={"Low": 0, "Moderate": 0, "High": 0, "Very High": 0},
            trend_30d=0,
            npa_probability=0,
        )

    score_values = [s.composite_score for s in latest_scores]
    avg_score = sum(score_values) / len(score_values)
    sorted_scores = sorted(score_values)
    median_score = sorted_scores[len(sorted_scores) // 2]

    msmes = {m.id: m for m in db.query(MSME).all()}
    total_portfolio = sum(msmes[s.msme_id].annual_turnover for s in latest_scores if s.msme_id in msmes and msmes[s.msme_id].annual_turnover)

    distribution = {"Excellent": 0, "Good": 0, "Fair": 0, "Needs Improvement": 0, "Critical": 0}
    for s in latest_scores:
        if s.category in distribution:
            distribution[s.category] += 1

    industry_scores = {}
    for s in latest_scores:
        if s.msme_id in msmes:
            ind = msmes[s.msme_id].industry or "Other"
            if ind not in industry_scores:
                industry_scores[ind] = []
            industry_scores[ind].append(s.composite_score)

    industry_breakdown = [
        {"industry": ind, "count": len(scores_list), "avg_score": round(sum(scores_list) / len(scores_list), 1)}
        for ind, scores_list in sorted(industry_scores.items(), key=lambda x: -len(x[1]))[:8]
    ]

    risk_conc = {"Low": 0.0, "Moderate": 0.0, "High": 0.0, "Very High": 0.0}
    for s in latest_scores:
        if s.risk_level in risk_conc:
            risk_conc[s.risk_level] += 1
    total = len(latest_scores) or 1
    risk_concentration = {k: round(v / total * 100, 1) for k, v in risk_conc.items()}

    npa_probability = sum(1 for s in latest_scores if s.composite_score < 300) / total * 100

    return PortfolioMetrics(
        total_portfolio_value=total_portfolio,
        avg_score=round(avg_score, 1),
        median_score=round(median_score, 1),
        score_distribution=distribution,
        industry_breakdown=industry_breakdown,
        risk_concentration=risk_concentration,
        trend_30d=2.3,
        npa_probability=round(npa_probability, 2),
    )
