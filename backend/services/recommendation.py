from typing import List, Dict


class RecommendationEngine:
    """Generate actionable recommendations based on dimension scores and risk flags."""

    def generate_recommendations(
        self,
        revenue_score: float,
        cash_flow_score: float,
        compliance_score: float,
        growth_score: float,
        repayment_score: float,
        risk_flags: List[Dict[str, str]],
    ) -> List[str]:
        recommendations = []

        if revenue_score < 50:
            recommendations.append("Diversify revenue streams to reduce dependency on single clients or products")
            recommendations.append("Consider filing GST returns on time consistently to improve compliance record")
        elif revenue_score < 70:
            recommendations.append("Focus on stabilizing monthly revenue — reduce seasonal variance through advance orders or retainer contracts")

        if cash_flow_score < 50:
            recommendations.append("Implement tighter payment collection policies — consider offering early payment discounts to customers")
            recommendations.append("Reduce unnecessary outflows and build a cash reserve buffer of 2-3 months operating expenses")
        elif cash_flow_score < 70:
            recommendations.append("Monitor working capital cycle — aim to reduce receivables days and optimize payables")

        if compliance_score < 50:
            recommendations.append("Prioritize statutory compliance — set up auto-reminders for GST and EPFO due dates")
            recommendations.append("Clear pending EPFO contributions immediately to avoid penalties and improve compliance score")
        elif compliance_score < 70:
            recommendations.append("Minor compliance gaps detected — ensure all GST returns and EPFO challan are filed before due dates")

        if growth_score < 50:
            recommendations.append("Invest in customer acquisition and market expansion to restart growth trajectory")
            recommendations.append("Consider digital marketing and e-commerce channels to reach new customer segments")
        elif growth_score < 70:
            recommendations.append("Growth is moderate — explore adjacent markets or product line extensions for acceleration")

        if repayment_score < 50:
            recommendations.append("Reduce existing debt burden before taking new credit — consider debt consolidation")
            recommendations.append("Improve free cash flow by negotiating better vendor terms and reducing discretionary spending")
        elif repayment_score < 70:
            recommendations.append("Maintain current EMI discipline and avoid taking additional short-term debt")

        high_risks = [r for r in risk_flags if r.get("severity") == "high"]
        if high_risks:
            recommendations.append("Address high-severity risk flags immediately — these significantly impact creditworthiness")

        if not recommendations:
            recommendations.append("Excellent financial health — maintain current practices and consider expanding credit facilities")
            recommendations.append("Consider applying for higher credit limits or better interest rates based on strong health score")

        return recommendations[:8]
