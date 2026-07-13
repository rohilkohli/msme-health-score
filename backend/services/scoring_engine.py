from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import numpy as np

from models.database import (
    MSME, GSTFiling, UPITransaction, EPFOContribution, BankStatement
)
from models.enums import ScoreCategory, ScoreCategoryColor
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
    """Main scoring engine for MSME Financial Health Score (0-1000)."""

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
        gst_score, gst_metrics, gst_insights = self.gst_service.compute_revenue_stability_score(gst_filings)
        upi_score, upi_metrics, upi_insights = self.upi_service.compute_cash_flow_score(upi_transactions)

        gst_on_time = sum(1 for f in gst_filings if f.is_on_time) / len(gst_filings) if gst_filings else 0.5
        compliance_score, compliance_metrics, compliance_insights = self.epfo_service.compute_compliance_score(
            epfo_contributions, gst_on_time
        )

        growth_score, growth_metrics, growth_insights = self._compute_growth_trajectory(
            gst_filings, upi_transactions, epfo_contributions
        )
        repayment_score, repayment_metrics, repayment_insights = self.aa_service.compute_repayment_capacity(bank_statements)
        aa_metrics, aa_insights = self.aa_service.compute_bank_health_metrics(bank_statements)

        risk_flags = self.risk_analyzer.detect_risk_patterns(
            gst_filings, upi_transactions, epfo_contributions, bank_statements
        )

        dimension_definitions = self._build_dimension_definitions(
            msme=msme,
            gst_score=gst_score,
            gst_metrics=gst_metrics,
            gst_insights=gst_insights,
            upi_score=upi_score,
            upi_metrics=upi_metrics,
            upi_insights=upi_insights,
            compliance_score=compliance_score,
            compliance_metrics=compliance_metrics,
            compliance_insights=compliance_insights,
            growth_score=growth_score,
            growth_metrics=growth_metrics,
            growth_insights=growth_insights,
            repayment_score=repayment_score,
            repayment_metrics=repayment_metrics,
            repayment_insights=repayment_insights,
            aa_metrics=aa_metrics,
            aa_insights=aa_insights,
            risk_flags=risk_flags,
        )

        availability = {
            "cashflow_strength_stability": bool(upi_transactions or bank_statements),
            "repayment_capacity_leverage": bool(bank_statements),
            "business_activity_growth": bool(gst_filings or upi_transactions),
            "transaction_quality_conduct": bool(upi_transactions or gst_filings),
            "compliance_formalization": bool(gst_filings or epfo_contributions),
            "resilience_risk_buffers": bool(bank_statements),
        }

        insufficient_data_flags = [f"Insufficient data for {k}" for k, ok in availability.items() if not ok]

        active_weight_sum = sum(self.weights[k] for k, ok in availability.items() if ok)
        effective_weights: Dict[str, float] = {}
        for key, base_weight in self.weights.items():
            if availability.get(key) and active_weight_sum > 0:
                effective_weights[key] = base_weight / active_weight_sum
            else:
                effective_weights[key] = 0.0

        base_composite = 0.0
        for key, dim in dimension_definitions.items():
            base_composite += dim["score"] * effective_weights.get(key, 0.0)

        data_confidence_index = self._compute_data_confidence(
            gst_filings, upi_transactions, epfo_contributions, bank_statements
        )
        confidence_penalty = (100 - data_confidence_index["overall"]) * 1.2

        critical_dims = [
            "cashflow_strength_stability",
            "repayment_capacity_leverage",
            "compliance_formalization",
        ]
        critical_missing_penalty = sum(25 for key in critical_dims if not availability.get(key))

        composite_score = self._clip((base_composite * 10) - confidence_penalty - critical_missing_penalty, 0, 1000)
        composite_score = round(composite_score, 2)

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

        reason_codes = self._extract_reason_codes(dimension_definitions, risk_flags)
        positive_reasons = sorted([r for r in reason_codes if r["impact"] > 0], key=lambda r: r["impact"], reverse=True)
        negative_reasons = sorted([r for r in reason_codes if r["impact"] < 0], key=lambda r: r["impact"])

        top_strengths = [r["message"] for r in positive_reasons[:3]]
        top_risks = [r["message"] for r in negative_reasons[:3]]

        recommendations = self.recommendation_engine.generate_recommendations(
            dimension_definitions["cashflow_strength_stability"]["score"],
            dimension_definitions["repayment_capacity_leverage"]["score"],
            dimension_definitions["business_activity_growth"]["score"],
            dimension_definitions["transaction_quality_conduct"]["score"],
            dimension_definitions["compliance_formalization"]["score"],
            dimension_definitions["resilience_risk_buffers"]["score"],
            risk_flags,
        )

        score_improvement_guidance = recommendations[:4]
        if insufficient_data_flags:
            score_improvement_guidance.append("Connect missing data sources (GST/UPI/AA/EPFO) to improve score confidence")

        dimensions: Dict[str, DimensionScore] = {}
        for key, definition in dimension_definitions.items():
            trends = definition["trends"]
            weight = effective_weights.get(key, 0.0)
            score = round(definition["score"], 2)
            dimensions[key] = DimensionScore(
                score=score,
                weight=round(weight, 4),
                weighted_score=round(score * weight, 2),
                sub_metrics=definition["sub_metrics"],
                insights=definition["insights"],
                trend_3m=trends["3m"],
                trend_6m=trends["6m"],
                trend_12m=trends["12m"],
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
            top_strengths=top_strengths,
            top_risks=top_risks,
            reason_codes=reason_codes,
            data_confidence_index=data_confidence_index,
            score_improvement_guidance=score_improvement_guidance,
            insufficient_data_flags=insufficient_data_flags,
        )

    def _build_dimension_definitions(self, **kwargs) -> Dict[str, Dict[str, Any]]:
        gst_metrics = kwargs["gst_metrics"]
        upi_metrics = kwargs["upi_metrics"]
        compliance_metrics = kwargs["compliance_metrics"]
        growth_metrics = kwargs["growth_metrics"]
        repayment_metrics = kwargs["repayment_metrics"]
        aa_metrics = kwargs["aa_metrics"]
        risk_flags = kwargs["risk_flags"]
        msme = kwargs["msme"]

        high_risk_count = sum(1 for flag in risk_flags if flag.get("severity") == "high")
        moderate_risk_count = sum(1 for flag in risk_flags if flag.get("severity") == "moderate")

        cashflow_strength = (
            kwargs["upi_score"] * 0.45 +
            aa_metrics.get("inflow_stability", 50) * 0.25 +
            aa_metrics.get("cash_buffer", 50) * 0.15 +
            gst_metrics.get("revenue_growth", 50) * 0.15
        )

        repayment_capacity = (
            kwargs["repayment_score"] * 0.70 +
            aa_metrics.get("emi_burden", 50) * 0.20 +
            repayment_metrics.get("obligation_coverage", 50) * 0.10
        )

        business_activity = (
            kwargs["growth_score"] * 0.45 +
            kwargs["gst_score"] * 0.35 +
            upi_metrics.get("transaction_regularity", 50) * 0.20
        )

        transaction_quality = (
            upi_metrics.get("payment_discipline", 50) * 0.35 +
            upi_metrics.get("transaction_regularity", 50) * 0.25 +
            (100 - min(100, moderate_risk_count * 12 + high_risk_count * 20)) * 0.40
        )

        vintage_years = max(0, datetime.now().year - (msme.year_established or datetime.now().year))
        vintage_score = self._clip((vintage_years / 10) * 100, 0, 100)
        compliance_formalization = (
            kwargs["compliance_score"] * 0.60 +
            gst_metrics.get("filing_consistency", 50) * 0.20 +
            compliance_metrics.get("epf_timeliness", 50) * 0.10 +
            vintage_score * 0.10
        )

        resilience = (
            aa_metrics.get("cash_buffer", 50) * 0.40 +
            aa_metrics.get("inflow_stability", 50) * 0.30 +
            repayment_metrics.get("free_cash_flow", 50) * 0.15 +
            (100 - min(100, high_risk_count * 20 + moderate_risk_count * 10)) * 0.15
        )

        definitions = {
            "cashflow_strength_stability": {
                "score": self._clip(cashflow_strength, 0, 100),
                "sub_metrics": {
                    "upi_cashflow_health": round(kwargs["upi_score"], 2),
                    "bank_inflow_stability": round(aa_metrics.get("inflow_stability", 50), 2),
                    "liquidity_buffer": round(aa_metrics.get("cash_buffer", 50), 2),
                    "gst_sales_momentum": round(gst_metrics.get("revenue_growth", 50), 2),
                },
                "insights": list(dict.fromkeys(kwargs["upi_insights"][:2] + kwargs["aa_insights"][:2])),
                "trends": {
                    "3m": self._trend_label(kwargs["upi_metrics"].get("working_capital", 50) - 50),
                    "6m": self._trend_label(kwargs["upi_score"] - 50),
                    "12m": self._trend_label(kwargs["gst_metrics"].get("revenue_growth", 50) - 50),
                },
            },
            "repayment_capacity_leverage": {
                "score": self._clip(repayment_capacity, 0, 100),
                "sub_metrics": {
                    "dscr_proxy": round(repayment_metrics.get("dscr_indicator", 50), 2),
                    "obligation_coverage": round(repayment_metrics.get("obligation_coverage", 50), 2),
                    "free_cash_flow_consistency": round(repayment_metrics.get("free_cash_flow", 50), 2),
                    "emi_burden_proxy": round(aa_metrics.get("emi_burden", 50), 2),
                },
                "insights": kwargs["repayment_insights"][:4],
                "trends": {
                    "3m": self._trend_label(repayment_metrics.get("balance_trend", 50) - 50),
                    "6m": self._trend_label(repayment_metrics.get("dscr_indicator", 50) - 50),
                    "12m": self._trend_label(kwargs["repayment_score"] - 50),
                },
            },
            "business_activity_growth": {
                "score": self._clip(business_activity, 0, 100),
                "sub_metrics": {
                    "gst_filing_regularity": round(gst_metrics.get("filing_consistency", 50), 2),
                    "invoice_growth_proxy": round(growth_metrics.get("revenue_cagr", 50), 2),
                    "transaction_volume_trend": round(growth_metrics.get("transaction_volume_trend", 50), 2),
                    "customer_growth": round(growth_metrics.get("customer_base_growth", 50), 2),
                },
                "insights": list(dict.fromkeys(kwargs["gst_insights"][:2] + kwargs["growth_insights"][:2])),
                "trends": {
                    "3m": self._trend_label(growth_metrics.get("transaction_volume_trend", 50) - 50),
                    "6m": self._trend_label(growth_metrics.get("customer_base_growth", 50) - 50),
                    "12m": self._trend_label(growth_metrics.get("revenue_cagr", 50) - 50),
                },
            },
            "transaction_quality_conduct": {
                "score": self._clip(transaction_quality, 0, 100),
                "sub_metrics": {
                    "payment_discipline": round(upi_metrics.get("payment_discipline", 50), 2),
                    "transaction_regularity": round(upi_metrics.get("transaction_regularity", 50), 2),
                    "anomaly_risk_control": round(100 - min(100, high_risk_count * 20 + moderate_risk_count * 12), 2),
                    "concentration_risk_control": round(100 - min(100, moderate_risk_count * 10), 2),
                },
                "insights": [f.get("description", "") for f in risk_flags[:2] if f.get("description")] or ["No major transaction quality alerts detected"],
                "trends": {
                    "3m": self._trend_label(upi_metrics.get("transaction_regularity", 50) - 50),
                    "6m": self._trend_label(upi_metrics.get("payment_discipline", 50) - 50),
                    "12m": self._trend_label(50 - (high_risk_count * 8 + moderate_risk_count * 4)),
                },
            },
            "compliance_formalization": {
                "score": self._clip(compliance_formalization, 0, 100),
                "sub_metrics": {
                    "gst_timeliness": round(compliance_metrics.get("gst_timeliness", 50), 2),
                    "epfo_timeliness": round(compliance_metrics.get("epf_timeliness", 50), 2),
                    "contribution_continuity": round(compliance_metrics.get("contribution_regularity", 50), 2),
                    "business_vintage_consistency": round(vintage_score, 2),
                },
                "insights": kwargs["compliance_insights"][:4],
                "trends": {
                    "3m": self._trend_label(compliance_metrics.get("gst_timeliness", 50) - 50),
                    "6m": self._trend_label(compliance_metrics.get("epf_timeliness", 50) - 50),
                    "12m": self._trend_label(kwargs["compliance_score"] - 50),
                },
            },
            "resilience_risk_buffers": {
                "score": self._clip(resilience, 0, 100),
                "sub_metrics": {
                    "liquidity_buffer_days_proxy": round(aa_metrics.get("cash_buffer", 50), 2),
                    "volatility_stress_control": round(aa_metrics.get("inflow_stability", 50), 2),
                    "adverse_event_control": round(100 - min(100, high_risk_count * 20 + moderate_risk_count * 8), 2),
                    "balance_trend_resilience": round(repayment_metrics.get("balance_trend", 50), 2),
                },
                "insights": kwargs["aa_insights"][:2] + [
                    f"Detected {high_risk_count} high-severity and {moderate_risk_count} moderate-severity risk signals"
                ],
                "trends": {
                    "3m": self._trend_label(repayment_metrics.get("balance_trend", 50) - 50),
                    "6m": self._trend_label(aa_metrics.get("cash_buffer", 50) - 50),
                    "12m": self._trend_label(aa_metrics.get("inflow_stability", 50) - 50),
                },
            },
        }

        return definitions

    def _compute_data_confidence(
        self,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
        bank_statements: List[BankStatement],
    ) -> Dict[str, float]:
        source_presence = {
            "gst": 100 if gst_filings else 0,
            "upi": 100 if upi_transactions else 0,
            "epfo": 100 if epfo_contributions else 0,
            "aa": 100 if bank_statements else 0,
        }

        coverage = round(sum(source_presence.values()) / max(len(source_presence), 1), 2)

        recency_components = []
        now = datetime.utcnow()
        if gst_filings:
            try:
                latest_gst = max(datetime.strptime(f.filing_period + "-01", "%Y-%m-%d") for f in gst_filings)
                recency_components.append(max(0, 100 - (now - latest_gst).days * 1.2))
            except Exception:
                recency_components.append(60)
        if upi_transactions:
            latest_upi = max(t.transaction_date for t in upi_transactions)
            recency_components.append(max(0, 100 - (now - latest_upi).days * 1.5))
        if epfo_contributions:
            try:
                latest_epfo = max(datetime.strptime(c.contribution_month + "-01", "%Y-%m-%d") for c in epfo_contributions)
                recency_components.append(max(0, 100 - (now - latest_epfo).days * 1.2))
            except Exception:
                recency_components.append(60)
        if bank_statements:
            try:
                latest_bank = max(datetime.strptime(s.month + "-01", "%Y-%m-%d") for s in bank_statements)
                recency_components.append(max(0, 100 - (now - latest_bank).days * 1.2))
            except Exception:
                recency_components.append(60)

        recency = round(float(np.mean(recency_components)) if recency_components else 35.0, 2)

        reliability_parts = []
        if gst_filings:
            reliability_parts.append(sum(1 for f in gst_filings if f.is_on_time) / len(gst_filings) * 100)
        if epfo_contributions:
            reliability_parts.append(sum(1 for c in epfo_contributions if c.is_on_time) / len(epfo_contributions) * 100)
        if upi_transactions:
            reliability_parts.append(min(100, len(upi_transactions) / 2))
        if bank_statements:
            reliability_parts.append(min(100, len(bank_statements) * 8))

        reliability = round(float(np.mean(reliability_parts)) if reliability_parts else 35.0, 2)
        overall = round((coverage * 0.4) + (recency * 0.3) + (reliability * 0.3), 2)

        return {
            "coverage": coverage,
            "recency": recency,
            "reliability": reliability,
            "overall": overall,
            "gst": round(source_presence["gst"], 2),
            "upi": round(source_presence["upi"], 2),
            "aa": round(source_presence["aa"], 2),
            "epfo": round(source_presence["epfo"], 2),
        }

    def _extract_reason_codes(
        self,
        dimension_definitions: Dict[str, Dict[str, Any]],
        risk_flags: List[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        reason_codes: List[Dict[str, Any]] = []

        for key, dim in dimension_definitions.items():
            score = dim["score"]
            if score >= 75:
                reason_codes.append({
                    "code": f"{key.upper()}_STRONG",
                    "dimension": key,
                    "impact": round((score - 70) * 1.4, 2),
                    "message": f"Strong {key.replace('_', ' ')} with score {score:.1f}/100",
                })
            elif score < 55:
                reason_codes.append({
                    "code": f"{key.upper()}_WEAK",
                    "dimension": key,
                    "impact": round(-(55 - score) * 1.6, 2),
                    "message": f"Weak {key.replace('_', ' ')} with score {score:.1f}/100",
                })

        for idx, flag in enumerate(risk_flags[:6]):
            severity = flag.get("severity", "moderate")
            penalty = -20 if severity == "high" else -10
            reason_codes.append({
                "code": f"RISK_FLAG_{idx+1}",
                "dimension": flag.get("category", "cross_source"),
                "impact": penalty,
                "message": flag.get("description", "Risk flag detected"),
            })

        return reason_codes

    def _trend_label(self, delta: float) -> str:
        if delta > 8:
            return "up"
        if delta < -8:
            return "down"
        return "stable"

    def _clip(self, value: float, low: float, high: float) -> float:
        return max(low, min(high, value))

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
