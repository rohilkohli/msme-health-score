from typing import List, Dict, Tuple
from datetime import datetime
import numpy as np

from models.database import BankStatement
from utils.helpers import (
    normalize_score, calculate_trend_slope,
    calculate_coefficient_of_variation, calculate_dscr
)


class AAService:
    """Service for analyzing Account Aggregator bank statement data."""

    def compute_bank_health_metrics(self, statements: List[BankStatement]) -> Tuple[Dict[str, float], List[str]]:
        """
        Compute bank statement health metrics from AA data.

        Returns metrics that feed into cash flow health and repayment capacity scores.
        """
        if not statements or len(statements) < 3:
            return {"avg_balance_score": 50, "cash_buffer": 50, "inflow_stability": 50, "emi_burden": 50}, ["Insufficient bank statement data"]

        sorted_statements = sorted(statements, key=lambda s: s.month)

        avg_balances = [s.avg_daily_balance for s in sorted_statements if s.avg_daily_balance]
        if avg_balances:
            trend = calculate_trend_slope(avg_balances)
            avg_bal = np.mean(avg_balances)
            if avg_bal > 0:
                balance_growth = (trend / avg_bal) * 100
                avg_balance_score = normalize_score(balance_growth, -20, 30)
            else:
                avg_balance_score = 30.0
        else:
            avg_balance_score = 50.0

        min_balances = [s.min_balance for s in sorted_statements if s.min_balance is not None]
        total_debits_list = [s.total_debits for s in sorted_statements if s.total_debits]
        if min_balances and total_debits_list:
            avg_min = np.mean(min_balances)
            avg_monthly_debit = np.mean(total_debits_list)
            if avg_monthly_debit > 0:
                buffer_months = avg_min / avg_monthly_debit
                cash_buffer = normalize_score(buffer_months, 0, 3)
            else:
                cash_buffer = 70.0
        else:
            cash_buffer = 50.0

        credits_list = [s.total_credits for s in sorted_statements if s.total_credits]
        if credits_list:
            cv = calculate_coefficient_of_variation(credits_list)
            inflow_stability = normalize_score(100 - cv, 0, 100)
        else:
            inflow_stability = 50.0

        emi_list = [s.emi_outflows for s in sorted_statements if s.emi_outflows is not None]
        credits_for_emi = [s.total_credits for s in sorted_statements if s.total_credits]
        if emi_list and credits_for_emi:
            avg_emi = np.mean(emi_list)
            avg_credit = np.mean(credits_for_emi)
            if avg_credit > 0:
                emi_ratio = avg_emi / avg_credit
                emi_burden = normalize_score(1 - emi_ratio, 0, 1) * 100
                emi_burden = normalize_score(emi_burden, 0, 100)
            else:
                emi_burden = 50.0
        else:
            emi_burden = 70.0

        metrics = {
            "avg_balance_score": round(avg_balance_score, 2),
            "cash_buffer": round(cash_buffer, 2),
            "inflow_stability": round(inflow_stability, 2),
            "emi_burden": round(emi_burden, 2),
        }

        insights = self._generate_insights(sorted_statements, metrics)

        return metrics, insights

    def compute_repayment_capacity(self, statements: List[BankStatement]) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Compute repayment capacity score (0-100).

        Sub-metrics:
        - DSCR indicator: Debt Service Coverage Ratio proxy
        - Free cash flow: Net surplus after all obligations
        - Obligation coverage: Ability to cover existing EMIs
        - Balance trend: Direction of account balances
        """
        if not statements or len(statements) < 3:
            return 50.0, {"dscr_indicator": 50, "free_cash_flow": 50, "obligation_coverage": 50, "balance_trend": 50}, ["Insufficient data for repayment capacity analysis"]

        sorted_statements = sorted(statements, key=lambda s: s.month)

        total_credits_avg = np.mean([s.total_credits for s in sorted_statements if s.total_credits]) if sorted_statements else 0
        total_emis_avg = np.mean([s.emi_outflows for s in sorted_statements if s.emi_outflows is not None]) if sorted_statements else 0

        operating_surplus = total_credits_avg - np.mean([s.total_debits for s in sorted_statements if s.total_debits])
        dscr = calculate_dscr(total_credits_avg * 0.3, total_emis_avg) if total_emis_avg > 0 else 2.5
        dscr_score = normalize_score(dscr, 0.5, 3.0)

        free_cash_flows = []
        for s in sorted_statements:
            if s.total_credits and s.total_debits:
                fcf = s.total_credits - s.total_debits
                free_cash_flows.append(fcf)

        if free_cash_flows:
            positive_fcf_ratio = sum(1 for f in free_cash_flows if f > 0) / len(free_cash_flows)
            free_cash_flow_score = positive_fcf_ratio * 100
        else:
            free_cash_flow_score = 50.0

        if total_emis_avg > 0 and total_credits_avg > 0:
            coverage = total_credits_avg / total_emis_avg
            obligation_coverage = normalize_score(coverage, 1, 10)
        else:
            obligation_coverage = 70.0

        closing_balances = [s.closing_balance for s in sorted_statements if s.closing_balance]
        if len(closing_balances) >= 3:
            trend = calculate_trend_slope(closing_balances)
            avg_bal = np.mean(closing_balances)
            if avg_bal > 0:
                trend_pct = (trend / avg_bal) * 100
                balance_trend = normalize_score(trend_pct, -15, 15)
            else:
                balance_trend = 40.0
        else:
            balance_trend = 50.0

        sub_metrics = {
            "dscr_indicator": round(dscr_score, 2),
            "free_cash_flow": round(free_cash_flow_score, 2),
            "obligation_coverage": round(obligation_coverage, 2),
            "balance_trend": round(balance_trend, 2),
        }

        composite = (
            dscr_score * 0.30 +
            free_cash_flow_score * 0.25 +
            obligation_coverage * 0.25 +
            balance_trend * 0.20
        )

        insights = self._generate_repayment_insights(sorted_statements, sub_metrics, dscr)

        return round(min(100, max(0, composite)), 2), sub_metrics, insights

    def _generate_insights(self, statements: List[BankStatement], metrics: Dict) -> List[str]:
        """Generate insights from bank statement analysis."""
        insights = []

        if metrics["cash_buffer"] > 70:
            insights.append("Strong cash buffer maintained - sufficient reserves for 2+ months of operations")
        elif metrics["cash_buffer"] > 40:
            insights.append("Adequate cash buffer but room for improvement in reserve management")
        else:
            insights.append("Low cash reserves - business vulnerable to cash flow disruptions")

        if metrics["inflow_stability"] > 70:
            insights.append("Stable and predictable bank inflows indicating reliable revenue streams")
        elif metrics["inflow_stability"] < 40:
            insights.append("Highly variable bank inflows - suggests irregular revenue patterns")

        if metrics["emi_burden"] > 70:
            insights.append("Low EMI burden relative to income - good capacity for additional borrowing")
        elif metrics["emi_burden"] < 40:
            insights.append("High EMI burden detected - limited headroom for new obligations")

        return insights

    def _generate_repayment_insights(self, statements: List[BankStatement], metrics: Dict, dscr: float) -> List[str]:
        """Generate repayment capacity insights."""
        insights = []

        if dscr >= 2.0:
            insights.append(f"Strong debt service coverage (DSCR: {dscr:.2f}) - well positioned for new credit")
        elif dscr >= 1.5:
            insights.append(f"Adequate debt service coverage (DSCR: {dscr:.2f}) - moderate borrowing capacity")
        elif dscr >= 1.0:
            insights.append(f"Marginal debt service coverage (DSCR: {dscr:.2f}) - limited new borrowing advisable")
        else:
            insights.append(f"Insufficient debt service coverage (DSCR: {dscr:.2f}) - debt restructuring may be needed")

        if metrics["free_cash_flow"] > 70:
            insights.append("Consistently positive free cash flow - strong repayment ability")
        elif metrics["free_cash_flow"] < 40:
            insights.append("Frequent negative cash flow months - repayment risk elevated")

        if metrics["balance_trend"] > 60:
            insights.append("Improving balance trend indicates strengthening financial position")
        elif metrics["balance_trend"] < 40:
            insights.append("Declining balance trend may signal deteriorating financial health")

        return insights
