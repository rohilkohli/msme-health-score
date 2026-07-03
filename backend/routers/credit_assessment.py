from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from models.database import (
    get_db, User, MSME, HealthScore,
    GSTFiling, UPITransaction, EPFOContribution, BankStatement
)
from models.schemas import CreditAssessmentResponse
from routers.auth import get_current_user
from utils.helpers import format_indian_currency

router = APIRouter()


@router.get("/{msme_id}", response_model=CreditAssessmentResponse)
def get_credit_assessment(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
        raise HTTPException(status_code=404, detail="No health score computed yet")

    composite = latest_score.composite_score
    readiness = min(100, (composite / 1000) * 120)
    credit_ready = composite >= 400

    annual_turnover = msme.annual_turnover or 500000
    if composite >= 800:
        loan_multiplier = 3.0
    elif composite >= 600:
        loan_multiplier = 2.0
    elif composite >= 400:
        loan_multiplier = 1.0
    else:
        loan_multiplier = 0.5
    max_loan = annual_turnover * loan_multiplier

    products = []
    if composite >= 400:
        products.append({
            "name": "MSME Business Loan",
            "max_amount": format_indian_currency(max_loan * 0.8),
            "interest_range": "10.5% - 14.5%",
            "tenure": "12-60 months",
            "eligibility": "Eligible" if composite >= 500 else "Conditionally Eligible",
        })
    if composite >= 500:
        products.append({
            "name": "Working Capital Loan",
            "max_amount": format_indian_currency(max_loan * 0.5),
            "interest_range": "11% - 15%",
            "tenure": "6-24 months",
            "eligibility": "Eligible",
        })
    if composite >= 600:
        products.append({
            "name": "Equipment Finance",
            "max_amount": format_indian_currency(max_loan * 0.6),
            "interest_range": "9.5% - 12.5%",
            "tenure": "24-84 months",
            "eligibility": "Eligible",
        })
    if composite >= 700:
        products.append({
            "name": "MSME Overdraft Facility",
            "max_amount": format_indian_currency(max_loan * 0.3),
            "interest_range": "10% - 13%",
            "tenure": "Revolving (annual renewal)",
            "eligibility": "Eligible",
        })
    if composite >= 800:
        products.append({
            "name": "Supply Chain Finance",
            "max_amount": format_indian_currency(max_loan * 0.4),
            "interest_range": "8.5% - 11%",
            "tenure": "30-180 days",
            "eligibility": "Eligible",
        })

    strengths = []
    weaknesses = []

    if latest_score.revenue_stability and latest_score.revenue_stability >= 70:
        strengths.append("Strong and stable revenue stream from GST data")
    elif latest_score.revenue_stability and latest_score.revenue_stability < 50:
        weaknesses.append("Unstable revenue pattern — high volatility in monthly turnover")

    if latest_score.cash_flow_health and latest_score.cash_flow_health >= 70:
        strengths.append("Healthy cash flow with good inflow-outflow balance")
    elif latest_score.cash_flow_health and latest_score.cash_flow_health < 50:
        weaknesses.append("Cash flow under stress — outflows frequently exceed inflows")

    if latest_score.compliance_score and latest_score.compliance_score >= 70:
        strengths.append("Excellent statutory compliance record (GST + EPFO)")
    elif latest_score.compliance_score and latest_score.compliance_score < 50:
        weaknesses.append("Compliance gaps — delayed GST/EPFO payments detected")

    if latest_score.growth_trajectory and latest_score.growth_trajectory >= 70:
        strengths.append("Strong growth trajectory with expanding customer base")
    elif latest_score.growth_trajectory and latest_score.growth_trajectory < 50:
        weaknesses.append("Stagnant or declining growth in revenue and customer base")

    if latest_score.repayment_capacity and latest_score.repayment_capacity >= 70:
        strengths.append("Strong repayment capacity with adequate free cash flow")
    elif latest_score.repayment_capacity and latest_score.repayment_capacity < 50:
        weaknesses.append("Limited repayment capacity — high debt burden relative to income")

    if not strengths:
        strengths.append("Business is operational with active transaction history")
    if not weaknesses:
        weaknesses.append("No major weaknesses identified")

    action_items = []
    if latest_score.compliance_score and latest_score.compliance_score < 70:
        action_items.append({"priority": "High", "action": "Clear pending GST/EPFO compliance — file all overdue returns"})
    if latest_score.cash_flow_health and latest_score.cash_flow_health < 60:
        action_items.append({"priority": "High", "action": "Improve cash flow — reduce receivables cycle and control discretionary spending"})
    if latest_score.revenue_stability and latest_score.revenue_stability < 60:
        action_items.append({"priority": "Medium", "action": "Diversify revenue sources — reduce dependency on top clients"})
    if latest_score.growth_trajectory and latest_score.growth_trajectory < 60:
        action_items.append({"priority": "Medium", "action": "Invest in customer acquisition and market expansion"})
    if not action_items:
        action_items.append({"priority": "Low", "action": "Maintain current financial practices — consider expanding credit facilities"})

    uli_eligibility = composite >= 500
    ocen_lenders = []
    if composite >= 400:
        ocen_lenders.append({"name": "IDBI Bank", "product": "MSME Term Loan"})
    if composite >= 500:
        ocen_lenders.append({"name": "Lendingkart", "product": "Working Capital"})
    if composite >= 600:
        ocen_lenders.append({"name": "Capital Float", "product": "Business Line of Credit"})
    if composite >= 700:
        ocen_lenders.append({"name": "Bajaj Finserv", "product": "Equipment Loan"})

    return CreditAssessmentResponse(
        msme_id=msme_id,
        credit_ready=credit_ready,
        readiness_percentage=round(readiness, 1),
        max_recommended_loan=max_loan,
        recommended_products=products,
        strengths=strengths,
        weaknesses=weaknesses,
        action_items=action_items,
        uli_eligibility=uli_eligibility,
        ocen_eligible_lenders=ocen_lenders,
    )
