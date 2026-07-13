from typing import List, Dict


class RecommendationEngine:
    """Generate actionable recommendations based on dimension scores and risk flags."""

    def generate_recommendations(
        self,
        cashflow_strength_score: float,
        repayment_capacity_score: float,
        business_activity_score: float,
        transaction_quality_score: float,
        compliance_score: float,
        resilience_score: float,
        risk_flags: List[Dict[str, str]],
    ) -> List[str]:
        recommendations = []

        if cashflow_strength_score < 50:
            recommendations.append("Implement tighter payment collection policies — consider offering early payment discounts to customers")
            recommendations.append("Reduce unnecessary outflows and build a cash reserve buffer of 2-3 months operating expenses")
        elif cashflow_strength_score < 70:
            recommendations.append("Monitor working capital cycle — aim to reduce receivables days and optimize payables")

        if repayment_capacity_score < 50:
            recommendations.append("Reduce existing debt burden before taking new credit — consider debt consolidation")
            recommendations.append("Improve free cash flow by negotiating better vendor terms and reducing discretionary spending")
        elif repayment_capacity_score < 70:
            recommendations.append("Maintain current EMI discipline and avoid taking additional short-term debt")

        if business_activity_score < 50:
            recommendations.append("Invest in customer acquisition and market expansion to restart growth trajectory")
            recommendations.append("Improve filing regularity and invoice discipline to strengthen business activity signals")
        elif business_activity_score < 70:
            recommendations.append("Growth is moderate — explore adjacent markets or product line extensions for acceleration")

        if transaction_quality_score < 50:
            recommendations.append("Reduce buyer concentration and monitor transaction anomalies to improve conduct score")
        elif transaction_quality_score < 70:
            recommendations.append("Strengthen transaction controls by reviewing reversals and recurring anomalies monthly")

        if compliance_score < 50:
            recommendations.append("Prioritize statutory compliance — set up auto-reminders for GST and EPFO due dates")
            recommendations.append("Clear pending EPFO contributions immediately to avoid penalties and improve compliance score")
        elif compliance_score < 70:
            recommendations.append("Minor compliance gaps detected — ensure all GST returns and EPFO challan are filed before due dates")

        if resilience_score < 50:
            recommendations.append("Build liquidity buffers and reduce earnings volatility to improve resilience during stress periods")
        elif resilience_score < 70:
            recommendations.append("Track liquidity buffer days monthly and target at least 30 days of operating coverage")

        high_risks = [r for r in risk_flags if r.get("severity") == "high"]
        if high_risks:
            recommendations.append("Address high-severity risk flags immediately — these significantly impact creditworthiness")

        if not recommendations:
            recommendations.append("Excellent financial health — maintain current practices and consider expanding credit facilities")
            recommendations.append("Consider applying for higher credit limits or better interest rates based on strong health score")

        return recommendations[:8]
