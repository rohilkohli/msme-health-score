from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np
import json

from models.database import (
    MSME, GSTFiling, UPITransaction, EPFOContribution, BankStatement, HealthScore
)
from models.enums import ScoreCategory, ScoreCategoryColor, RiskLevel
from models.schemas import DimensionScore, HealthScoreResponse
from services.gst_service import GSTService
from services.upi_service import UPIService
from services.epfo_service import EPFOService
from services.aa_service import AAService
from services.ml_model import MLModelService
from services.risk_analyzer import RiskAnalyzer
from services.recommendation import RecommendationEngine
from config import get_settings

settings = get_settings()


class ScoringEngine:
    """
    Main scoring engine that combines all dimension scores into a composite
    MSME Financial Health Score (0-1000).
    """

    def __init__(self):
        self.gst_service = GSTService()
        self.upi_service = UPIService()
        self.epfo_service = EPFOService()
        self.aa_service = AAService()
        self.ml_service = MLModelService()
        self.risk_analyzer = RiskAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.weights = settings.SCORING_WEIGHTS

    def compute_health_score(
        self,
        msme: MSME,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
        bank_statements: List[BankStatement],
    ) -> HealthScoreResponse:
        """
        Compute the complete MSME Financial Health Score.

        Steps:
        1. Compute individual dimension scores
        2. Calculate weighted composite score (0-1000)
        3. Run ML prediction for credit risk
        4. Determine risk level and category
        5. Generate recommendations
        """
        revenue_score, revenue_metrics, revenue_insights = self.gst_service.compute_revenue_stability_score(gst_filings)

        cash_flow_score, cash_flow_metrics, cash_flow_insights = self.upi_service.compute_cash_flow_score(upi_transactions)

        gst_on_time = sum(1 for f in gst_filings if f.is_on_time) / len(gst_filings) if gst_filings else 0.5
        compliance_score, compliance_metrics, compliance_insights = self.epfo_service.compute_compliance_score(
            epfo_contributions, gst_on_time
        )

        growth_score, growth_metrics, growth_insights = self._compute_growth_trajectory(
            gst_filings, upi_transactions, epfo_contributions
        )

        repayment_score, repayment_metrics, repayment_insights = self.aa_service.compute_repayment_capacity(
            bank_statements
        )

        aa_metrics, aa_insights = self.aa_service.compute_bank_health_metrics(bank_statements)
        cash_flow_score = (cash_flow_score * 0.6 + np.mean(list(aa_metrics.values())) * 0.4)
        cash_flow_score = round(min(100, max(0, cash_flow_score)), 2)

        composite_score = (
            revenue_score * self.weights["revenue_stability"] +
            cash_flow_score * self.weights["cash_flow_health"] +
            compliance_score * self.weights["compliance_score"] +
            growth_score * self.weights["growth_trajectory"] +
            repayment_score * self.weights["repayment_capacity"]
        ) * 10

        composite_score = round(min(1000, max(0, composite_score)), 2)

        category = ScoreCategory.from_score(composite_score)
        category_color = ScoreCategoryColor.from_category(category)
        risk_level = self.risk_analyzer.determine_risk_level(composite_score)

        ml_score = None
        feature_importance = None
        try:
            features = self._extract_ml_features(
                msme, gst_filings, upi_transactions, epfo_contributions, bank_statements
            )
            ml_score, feature_importance = self.ml_service.predict(features)
        except Exception:
            pass

        all_insights = revenue_insights + cash_flow_insights + compliance_insights + growth_insights + repayment_insights
        risk_flags = self.risk_analyzer.detect_risk_patterns(
            gst_filings, upi_transactions, epfo_contributions, bank_statements
        )

        dimension_scores = {
            revenue_score: ("revenue_stability", revenue_metrics, revenue_insights),
            cash_flow_score: ("cash_flow_health", cash_flow_metrics, cash_flow_insights),
            compliance_score: ("compliance_score", compliance_metrics, compliance_insights),
            growth_score: ("growth_trajectory", growth_metrics, growth_insights),
            repayment_score: ("repayment_capacity", repayment_metrics, repayment_insights),
        }

        recommendations = self.recommendation_engine.generate_recommendations(
            revenue_score, cash_flow_score, compliance_score,
            growth_score, repayment_score, risk_flags
        )

        dimensions = {}
        for score_val, (dim_name, metrics, insights) in dimension_scores.items():
            weight = self.weights[dim_name]
            dimensions[dim_name] = DimensionScore(
                score=score_val,
                weight=weight,
                weighted_score=round(score_val * weight, 2),
                sub_metrics=metrics,
                insights=insights,
            )

        return HealthScoreResponse(
            msme_id=msme.id,
            composite_score=composite_score,
            category=category.value,
            category_color=category_color,
            risk_level=risk_level.value,
            dimensions=dimensions,
            ml_prediction_score=ml_score,
            feature_importance=feature_importance,
            computed_at=datetime.utcnow(),
            recommendations=recommendations,
        )

    def _compute_growth_trajectory(
        self,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
    ) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Compute growth trajectory score (0-100).

        Sub-metrics:
        - Revenue CAGR: Compound annual growth of GST turnover
        - Customer base growth: Growth in unique UPI counterparties
        - Transaction volume trend: Growth in transaction frequency
        - Workforce expansion: Growth in EPFO-reported employee count
        """
        revenue_cagr_score = 50.0
        if gst_filings and len(gst_filings) >= 6:
            sorted_filings = sorted(gst_filings, key=lambda f: f.filing_period)
            turnovers = [f.taxable_turnover for f in sorted_filings if f.taxable_turnover]
            if len(turnovers) >= 6:
                first_q_avg = np.mean(turnovers[:3])
                last_q_avg = np.mean(turnovers[-3:])
                if first_q_avg > 0:
                    periods = len(turnovers) / 12.0
                    if periods > 0 and last_q_avg > 0:
                        cagr = (pow(last_q_avg / first_q_avg, 1 / max(periods, 0.5)) - 1) * 100
                        revenue_cagr_score = min(100, max(0, 50 + cagr * 2))

        customer_growth_score = 50.0
        if upi_transactions and len(upi_transactions) >= 30:
            from collections import defaultdict
            monthly_customers = defaultdict(set)
            for t in upi_transactions:
                if t.is_credit and t.counterparty_vpa:
                    key = t.transaction_date.strftime("%Y-%m")
                    monthly_customers[key].add(t.counterparty_vpa)

            if len(monthly_customers) >= 3:
                sorted_months = sorted(monthly_customers.keys())
                customer_counts = [len(monthly_customers[m]) for m in sorted_months]
                if len(customer_counts) >= 3:
                    first_avg = np.mean(customer_counts[:len(customer_counts)//3])
                    last_avg = np.mean(customer_counts[-len(customer_counts)//3:])
                    if first_avg > 0:
                        growth = ((last_avg - first_avg) / first_avg) * 100
                        customer_growth_score = min(100, max(0, 50 + growth))

        volume_trend_score = 50.0
        if upi_transactions and len(upi_transactions) >= 30:
            from collections import defaultdict
            monthly_volumes = defaultdict(int)
            for t in upi_transactions:
                key = t.transaction_date.strftime("%Y-%m")
                monthly_volumes[key] += 1

            sorted_months = sorted(monthly_volumes.keys())
            volumes = [monthly_volumes[m] for m in sorted_months]
            if len(volumes) >= 3:
                from utils.helpers import calculate_trend_slope
                trend = calculate_trend_slope(volumes)
                avg_vol = np.mean(volumes)
                if avg_vol > 0:
                    trend_pct = (trend / avg_vol) * 100
                    volume_trend_score = min(100, max(0, 50 + trend_pct * 3))

        workforce_score = 50.0
        if epfo_contributions and len(epfo_contributions) >= 3:
            sorted_c = sorted(epfo_contributions, key=lambda c: c.contribution_month)
            emp_counts = [c.num_employees for c in sorted_c if c.num_employees]
            if len(emp_counts) >= 3:
                first_avg = np.mean(emp_counts[:3])
                last_avg = np.mean(emp_counts[-3:])
                if first_avg > 0:
                    growth = ((last_avg - first_avg) / first_avg) * 100
                    workforce_score = min(100, max(0, 50 + growth * 2))

        sub_metrics = {
            "revenue_cagr": round(revenue_cagr_score, 2),
            "customer_base_growth": round(customer_growth_score, 2),
            "transaction_volume_trend": round(volume_trend_score, 2),
            "workforce_expansion": round(workforce_score, 2),
        }

        composite = (
            revenue_cagr_score * 0.35 +
            customer_growth_score * 0.25 +
            volume_trend_score * 0.20 +
            workforce_score * 0.20
        )

        insights = []
        if revenue_cagr_score > 65:
            insights.append("Strong revenue growth trajectory - business expanding well")
        elif revenue_cagr_score < 40:
            insights.append("Revenue growth stagnant or declining - diversification may help")

        if customer_growth_score > 65:
            insights.append("Growing customer base indicates market penetration success")
        elif customer_growth_score < 40:
            insights.append("Customer acquisition slowing - review marketing and sales strategy")

        if workforce_score > 65:
            insights.append("Workforce expansion signals business confidence and growth")
        elif workforce_score < 40:
            insights.append("Workforce contraction may indicate operational challenges")

        return round(min(100, max(0, composite)), 2), sub_metrics, insights

    def _extract_ml_features(
        self,
        msme: MSME,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
        bank_statements: List[BankStatement],
    ) -> Dict[str, float]:
        """Extract features for ML model prediction."""
        features = {}

        features["annual_turnover"] = msme.annual_turnover or 0
        features["employee_count"] = msme.employee_count or 0
        features["years_in_business"] = datetime.now().year - (msme.year_established or 2020)

        if gst_filings:
            turnovers = [f.taxable_turnover for f in gst_filings if f.taxable_turnover]
            features["avg_monthly_revenue"] = np.mean(turnovers) if turnovers else 0
            features["revenue_volatility"] = np.std(turnovers) / np.mean(turnovers) if turnovers and np.mean(turnovers) > 0 else 0
            features["gst_compliance_rate"] = sum(1 for f in gst_filings if f.is_on_time) / len(gst_filings)
            features["avg_tax_paid"] = np.mean([f.tax_paid for f in gst_filings if f.tax_paid])
        else:
            features["avg_monthly_revenue"] = 0
            features["revenue_volatility"] = 0.5
            features["gst_compliance_rate"] = 0.5
            features["avg_tax_paid"] = 0

        if upi_transactions:
            credits = [t.amount for t in upi_transactions if t.is_credit]
            debits = [t.amount for t in upi_transactions if not t.is_credit]
            features["avg_credit_amount"] = np.mean(credits) if credits else 0
            features["avg_debit_amount"] = np.mean(debits) if debits else 0
            features["credit_debit_ratio"] = sum(credits) / sum(debits) if debits and sum(debits) > 0 else 1.0
            features["transaction_frequency"] = len(upi_transactions) / 30.0
        else:
            features["avg_credit_amount"] = 0
            features["avg_debit_amount"] = 0
            features["credit_debit_ratio"] = 1.0
            features["transaction_frequency"] = 0

        if epfo_contributions:
            features["epfo_compliance_rate"] = sum(1 for c in epfo_contributions if c.is_on_time) / len(epfo_contributions)
            features["avg_epfo_contribution"] = np.mean([c.total_contribution for c in epfo_contributions if c.total_contribution])
        else:
            features["epfo_compliance_rate"] = 0.5
            features["avg_epfo_contribution"] = 0

        if bank_statements:
            features["avg_daily_balance"] = np.mean([s.avg_daily_balance for s in bank_statements if s.avg_daily_balance])
            features["avg_monthly_credits"] = np.mean([s.total_credits for s in bank_statements if s.total_credits])
            features["avg_monthly_debits"] = np.mean([s.total_debits for s in bank_statements if s.total_debits])
            emi_list = [s.emi_outflows for s in bank_statements if s.emi_outflows is not None]
            features["emi_to_income_ratio"] = np.mean(emi_list) / features["avg_monthly_credits"] if features["avg_monthly_credits"] > 0 and emi_list else 0
        else:
            features["avg_daily_balance"] = 0
            features["avg_monthly_credits"] = 0
            features["avg_monthly_debits"] = 0
            features["emi_to_income_ratio"] = 0

        return features
