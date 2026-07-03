from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

from models.database import UPITransaction
from utils.helpers import (
    calculate_coefficient_of_variation, calculate_trend_slope,
    normalize_score, calculate_moving_average
)


class UPIService:
    """Service for analyzing UPI transaction patterns and computing cash flow health."""

    def compute_cash_flow_score(self, transactions: List[UPITransaction]) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Compute cash flow health score (0-100) from UPI transactions.

        Sub-metrics:
        - Inflow/outflow ratio: Credits vs debits balance
        - Transaction regularity: Consistency of transaction frequency
        - Working capital adequacy: Net cash flow sufficiency
        - Payment discipline: Outflow timing patterns
        """
        if not transactions or len(transactions) < 10:
            return 50.0, {"inflow_outflow_ratio": 50, "transaction_regularity": 50, "working_capital": 50, "payment_discipline": 50}, ["Insufficient UPI transaction data"]

        credits = [t for t in transactions if t.is_credit]
        debits = [t for t in transactions if not t.is_credit]

        total_credits = sum(t.amount for t in credits)
        total_debits = sum(t.amount for t in debits)

        if total_debits > 0:
            ratio = total_credits / total_debits
            inflow_outflow_score = normalize_score(ratio, 0.5, 2.0)
        else:
            inflow_outflow_score = 80.0

        monthly_counts = self._get_monthly_transaction_counts(transactions)
        if monthly_counts:
            cv = calculate_coefficient_of_variation(monthly_counts)
            transaction_regularity = normalize_score(100 - cv, 0, 100)
        else:
            transaction_regularity = 50.0

        monthly_net = self._get_monthly_net_flow(transactions)
        if monthly_net:
            positive_months = sum(1 for n in monthly_net if n > 0)
            working_capital = (positive_months / len(monthly_net)) * 100
        else:
            working_capital = 50.0

        payment_discipline = self._calculate_payment_discipline(debits)

        sub_metrics = {
            "inflow_outflow_ratio": round(inflow_outflow_score, 2),
            "transaction_regularity": round(transaction_regularity, 2),
            "working_capital": round(working_capital, 2),
            "payment_discipline": round(payment_discipline, 2),
        }

        composite = (
            inflow_outflow_score * 0.30 +
            transaction_regularity * 0.25 +
            working_capital * 0.25 +
            payment_discipline * 0.20
        )

        insights = self._generate_insights(transactions, credits, debits, sub_metrics)

        return round(min(100, max(0, composite)), 2), sub_metrics, insights

    def _get_monthly_transaction_counts(self, transactions: List[UPITransaction]) -> List[float]:
        """Get monthly transaction count series."""
        monthly = defaultdict(int)
        for t in transactions:
            key = t.transaction_date.strftime("%Y-%m")
            monthly[key] += 1
        return list(monthly.values()) if monthly else []

    def _get_monthly_net_flow(self, transactions: List[UPITransaction]) -> List[float]:
        """Get monthly net cash flow (credits - debits)."""
        monthly = defaultdict(float)
        for t in transactions:
            key = t.transaction_date.strftime("%Y-%m")
            if t.is_credit:
                monthly[key] += t.amount
            else:
                monthly[key] -= t.amount
        sorted_keys = sorted(monthly.keys())
        return [monthly[k] for k in sorted_keys]

    def _calculate_payment_discipline(self, debits: List[UPITransaction]) -> float:
        """Calculate payment discipline score based on outflow patterns."""
        if not debits:
            return 50.0

        monthly_debits = defaultdict(list)
        for t in debits:
            key = t.transaction_date.strftime("%Y-%m")
            monthly_debits[key].append(t)

        regularity_scores = []
        for month, txns in monthly_debits.items():
            days = [t.transaction_date.day for t in txns]
            if len(days) >= 3:
                spread = np.std(days)
                regularity_scores.append(normalize_score(30 - spread, 0, 30))

        if regularity_scores:
            return np.mean(regularity_scores)
        return 60.0

    def _generate_insights(self, all_txns: List[UPITransaction], credits: List, debits: List, sub_metrics: Dict) -> List[str]:
        """Generate insights from UPI transaction patterns."""
        insights = []

        total_credits = sum(t.amount for t in credits)
        total_debits = sum(t.amount for t in debits)

        if total_debits > 0:
            ratio = total_credits / total_debits
            if ratio > 1.5:
                insights.append(f"Strong cash position with credit-to-debit ratio of {ratio:.2f}")
            elif ratio > 1.0:
                insights.append(f"Healthy cash flow with credit-to-debit ratio of {ratio:.2f}")
            else:
                insights.append(f"Cash flow under pressure - outflows exceeding inflows (ratio: {ratio:.2f})")

        monthly_credits = defaultdict(float)
        for t in credits:
            key = t.transaction_date.strftime("%Y-%m")
            monthly_credits[key] += t.amount
        credit_values = list(monthly_credits.values())
        if len(credit_values) >= 3:
            trend = calculate_trend_slope(credit_values)
            avg = np.mean(credit_values)
            if avg > 0:
                trend_pct = (trend / avg) * 100
                if trend_pct > 5:
                    insights.append(f"UPI collections growing at {trend_pct:.1f}% monthly")
                elif trend_pct < -5:
                    insights.append(f"UPI collections declining at {trend_pct:.1f}% monthly")

        if sub_metrics["transaction_regularity"] > 70:
            insights.append("Consistent transaction patterns indicating stable business operations")
        elif sub_metrics["transaction_regularity"] < 40:
            insights.append("Irregular transaction patterns - may indicate volatile business activity")

        unique_counterparties = set()
        for t in credits:
            if t.counterparty_vpa:
                unique_counterparties.add(t.counterparty_vpa)
        if len(unique_counterparties) > 20:
            insights.append(f"Diverse customer base with {len(unique_counterparties)} unique payment sources")
        elif len(unique_counterparties) < 5:
            insights.append("High customer concentration risk - few unique payment sources")

        return insights

    def get_daily_cash_flow(self, transactions: List[UPITransaction]) -> List[Dict]:
        """Get daily cash flow data for visualization."""
        daily = defaultdict(lambda: {"credits": 0, "debits": 0})
        for t in transactions:
            key = t.transaction_date.strftime("%Y-%m-%d")
            if t.is_credit:
                daily[key]["credits"] += t.amount
            else:
                daily[key]["debits"] += t.amount

        sorted_keys = sorted(daily.keys())
        return [
            {
                "date": k,
                "credits": daily[k]["credits"],
                "debits": daily[k]["debits"],
                "net": daily[k]["credits"] - daily[k]["debits"],
            }
            for k in sorted_keys
        ]
