from typing import List, Dict, Tuple
from datetime import datetime
import numpy as np

from models.database import GSTFiling
from utils.helpers import (
    calculate_coefficient_of_variation, calculate_trend_slope,
    normalize_score, calculate_cagr, detect_seasonality
)


class GSTService:
    """Service for processing GST filing data and computing revenue stability score."""

    def compute_revenue_stability_score(self, filings: List[GSTFiling]) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Compute revenue stability score (0-100) from GST filings.

        Sub-metrics:
        - Filing consistency: % of filings done on time
        - Revenue growth trend: CAGR of taxable turnover
        - Seasonal variance: Lower variance = higher score
        - Revenue regularity: Coefficient of variation of monthly revenue
        """
        if not filings or len(filings) < 3:
            return 50.0, {"filing_consistency": 50, "revenue_growth": 50, "seasonal_variance": 50, "revenue_regularity": 50}, ["Insufficient GST data for analysis"]

        sorted_filings = sorted(filings, key=lambda f: f.filing_period)
        turnovers = [f.taxable_turnover for f in sorted_filings if f.taxable_turnover]
        on_time_filings = [f for f in sorted_filings if f.is_on_time]

        filing_consistency = (len(on_time_filings) / len(sorted_filings)) * 100 if sorted_filings else 50

        revenue_growth = 50.0
        if len(turnovers) >= 6:
            first_half_avg = np.mean(turnovers[:len(turnovers)//2])
            second_half_avg = np.mean(turnovers[len(turnovers)//2:])
            if first_half_avg > 0:
                growth_rate = ((second_half_avg - first_half_avg) / first_half_avg) * 100
                revenue_growth = normalize_score(growth_rate, -30, 50)

        cv = calculate_coefficient_of_variation(turnovers) if turnovers else 50
        seasonal_variance = normalize_score(100 - cv, 0, 100)

        regularity_score = 100 - min(cv, 100) if turnovers else 50
        revenue_regularity = max(0, regularity_score)

        sub_metrics = {
            "filing_consistency": round(filing_consistency, 2),
            "revenue_growth": round(revenue_growth, 2),
            "seasonal_variance": round(seasonal_variance, 2),
            "revenue_regularity": round(revenue_regularity, 2),
        }

        composite = (
            filing_consistency * 0.30 +
            revenue_growth * 0.30 +
            seasonal_variance * 0.20 +
            revenue_regularity * 0.20
        )

        insights = self._generate_insights(sorted_filings, turnovers, sub_metrics)

        return round(min(100, max(0, composite)), 2), sub_metrics, insights

    def _generate_insights(self, filings: List[GSTFiling], turnovers: List[float], sub_metrics: Dict) -> List[str]:
        """Generate human-readable insights from GST data."""
        insights = []

        if sub_metrics["filing_consistency"] >= 90:
            insights.append("Excellent GST filing compliance - all returns filed on time")
        elif sub_metrics["filing_consistency"] >= 70:
            insights.append("Good GST compliance with minor delays in some periods")
        else:
            late_count = len(filings) - int(len(filings) * sub_metrics["filing_consistency"] / 100)
            insights.append(f"GST compliance needs attention - {late_count} late filings detected")

        if turnovers and len(turnovers) >= 6:
            trend = calculate_trend_slope(turnovers)
            avg_turnover = np.mean(turnovers)
            if avg_turnover > 0:
                trend_pct = (trend / avg_turnover) * 100
                if trend_pct > 5:
                    insights.append(f"Revenue showing strong upward trend (+{trend_pct:.1f}% monthly)")
                elif trend_pct > 0:
                    insights.append(f"Revenue showing moderate growth (+{trend_pct:.1f}% monthly)")
                elif trend_pct > -5:
                    insights.append("Revenue relatively stable with minor fluctuations")
                else:
                    insights.append(f"Revenue declining trend detected ({trend_pct:.1f}% monthly)")

        if turnovers:
            seasonality = detect_seasonality(turnovers)
            if seasonality > 0.3:
                insights.append("High seasonal variation in revenue - consider working capital planning")
            elif seasonality > 0.15:
                insights.append("Moderate seasonality detected in revenue patterns")

        if turnovers and len(turnovers) >= 12:
            recent_avg = np.mean(turnovers[-3:])
            overall_avg = np.mean(turnovers)
            if recent_avg > overall_avg * 1.2:
                insights.append("Recent revenue performance significantly above historical average")
            elif recent_avg < overall_avg * 0.8:
                insights.append("Recent revenue performance below historical average - monitor closely")

        return insights

    def get_monthly_revenue_trend(self, filings: List[GSTFiling]) -> List[Dict]:
        """Get monthly revenue trend data for visualization."""
        sorted_filings = sorted(filings, key=lambda f: f.filing_period)
        return [
            {
                "period": f.filing_period,
                "turnover": f.taxable_turnover,
                "tax_paid": f.tax_paid,
                "itc_claimed": f.itc_claimed,
                "on_time": f.is_on_time,
            }
            for f in sorted_filings
        ]

    def calculate_itc_ratio(self, filings: List[GSTFiling]) -> float:
        """Calculate ITC to tax paid ratio - indicates business health."""
        total_tax = sum(f.tax_paid for f in filings if f.tax_paid)
        total_itc = sum(f.itc_claimed for f in filings if f.itc_claimed)
        if total_tax == 0:
            return 0.0
        return total_itc / total_tax
