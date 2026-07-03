from typing import List, Dict, Tuple
from datetime import datetime
import numpy as np

from models.database import EPFOContribution
from utils.helpers import normalize_score, calculate_trend_slope, calculate_coefficient_of_variation


class EPFOService:
    """Service for processing EPFO contribution data and computing compliance score."""

    def compute_compliance_score(self, contributions: List[EPFOContribution], gst_on_time_ratio: float = 0.8) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Compute compliance score (0-100) from EPFO contributions and GST filing timeliness.

        Sub-metrics:
        - EPF payment timeliness: % of contributions paid on time
        - Contribution regularity: Consistency of monthly contributions
        - Employee growth indicator: Trend in number of employees
        - GST filing timeliness: Combined from GST on-time ratio
        """
        if not contributions or len(contributions) < 3:
            return 50.0, {"epf_timeliness": 50, "contribution_regularity": 50, "employee_growth": 50, "gst_timeliness": gst_on_time_ratio * 100}, ["Insufficient EPFO data for analysis"]

        sorted_contributions = sorted(contributions, key=lambda c: c.contribution_month)

        on_time = [c for c in sorted_contributions if c.is_on_time]
        epf_timeliness = (len(on_time) / len(sorted_contributions)) * 100

        amounts = [c.total_contribution for c in sorted_contributions if c.total_contribution]
        if amounts:
            cv = calculate_coefficient_of_variation(amounts)
            contribution_regularity = normalize_score(100 - cv, 0, 100)
        else:
            contribution_regularity = 50.0

        employee_counts = [c.num_employees for c in sorted_contributions if c.num_employees]
        if len(employee_counts) >= 3:
            trend = calculate_trend_slope(employee_counts)
            avg_employees = np.mean(employee_counts)
            if avg_employees > 0:
                growth_rate = (trend / avg_employees) * 100
                employee_growth = normalize_score(growth_rate, -10, 20)
            else:
                employee_growth = 50.0
        else:
            employee_growth = 50.0

        gst_timeliness = gst_on_time_ratio * 100

        sub_metrics = {
            "epf_timeliness": round(epf_timeliness, 2),
            "contribution_regularity": round(contribution_regularity, 2),
            "employee_growth": round(employee_growth, 2),
            "gst_timeliness": round(gst_timeliness, 2),
        }

        composite = (
            epf_timeliness * 0.35 +
            contribution_regularity * 0.20 +
            employee_growth * 0.15 +
            gst_timeliness * 0.30
        )

        insights = self._generate_insights(sorted_contributions, sub_metrics, employee_counts)

        return round(min(100, max(0, composite)), 2), sub_metrics, insights

    def _generate_insights(self, contributions: List[EPFOContribution], sub_metrics: Dict, employee_counts: List) -> List[str]:
        """Generate compliance insights."""
        insights = []

        if sub_metrics["epf_timeliness"] >= 95:
            insights.append("Exemplary EPF compliance - all contributions paid on or before due dates")
        elif sub_metrics["epf_timeliness"] >= 80:
            insights.append("Good EPF payment discipline with occasional minor delays")
        elif sub_metrics["epf_timeliness"] >= 60:
            insights.append("EPF payment delays observed - may attract penalty and impact compliance rating")
        else:
            insights.append("Significant EPF compliance issues - multiple delayed payments detected")

        if employee_counts and len(employee_counts) >= 6:
            recent = np.mean(employee_counts[-3:])
            earlier = np.mean(employee_counts[:3])
            if recent > earlier * 1.1:
                growth = ((recent - earlier) / earlier) * 100
                insights.append(f"Workforce growing by {growth:.1f}% - positive business expansion signal")
            elif recent < earlier * 0.9:
                decline = ((earlier - recent) / earlier) * 100
                insights.append(f"Workforce reduced by {decline:.1f}% - may indicate business contraction")
            else:
                insights.append("Stable workforce maintained - consistent employment pattern")

        if sub_metrics["contribution_regularity"] > 80:
            insights.append("Regular and predictable EPF contributions indicate stable payroll management")
        elif sub_metrics["contribution_regularity"] < 50:
            insights.append("Irregular contribution amounts suggest variable payroll or compliance gaps")

        if sub_metrics["gst_timeliness"] >= 90 and sub_metrics["epf_timeliness"] >= 90:
            insights.append("Strong overall statutory compliance across both GST and EPFO")
        elif sub_metrics["gst_timeliness"] < 70 or sub_metrics["epf_timeliness"] < 70:
            insights.append("Compliance gaps detected across regulatory filings - needs immediate attention")

        return insights

    def get_contribution_trend(self, contributions: List[EPFOContribution]) -> List[Dict]:
        """Get contribution trend data for visualization."""
        sorted_c = sorted(contributions, key=lambda c: c.contribution_month)
        return [
            {
                "month": c.contribution_month,
                "total_contribution": c.total_contribution,
                "employee_count": c.num_employees,
                "on_time": c.is_on_time,
                "employer_share": c.employer_contribution,
                "employee_share": c.employee_contribution,
            }
            for c in sorted_c
        ]
