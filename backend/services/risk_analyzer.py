from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

from models.database import GSTFiling, UPITransaction, EPFOContribution, BankStatement
from models.enums import RiskLevel


class RiskAnalyzer:
    """Service for detecting risk patterns and determining overall risk level."""

    def determine_risk_level(self, composite_score: float) -> RiskLevel:
        """Determine risk level from composite score."""
        if composite_score >= 800:
            return RiskLevel.VERY_LOW
        elif composite_score >= 700:
            return RiskLevel.LOW
        elif composite_score >= 600:
            return RiskLevel.MODERATE
        elif composite_score >= 500:
            return RiskLevel.HIGH
        else:
            return RiskLevel.HIGH

    def detect_risk_patterns(
        self,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
        bank_statements: List[BankStatement],
    ) -> List[Dict[str, str]]:
        """
        Detect risk patterns across all data sources.

        Returns list of risk flags with severity and description.
        """
        risk_flags = []

        risk_flags.extend(self._check_gst_risks(gst_filings))
        risk_flags.extend(self._check_upi_risks(upi_transactions))
        risk_flags.extend(self._check_epfo_risks(epfo_contributions))
        risk_flags.extend(self._check_bank_risks(bank_statements))
        risk_flags.extend(self._check_cross_source_risks(
            gst_filings, upi_transactions, epfo_contributions, bank_statements
        ))

        return risk_flags

    def _check_gst_risks(self, filings: List[GSTFiling]) -> List[Dict[str, str]]:
        """Check GST-related risk patterns."""
        risks = []
        if not filings:
            risks.append({
                "severity": "high",
                "category": "data_gap",
                "description": "No GST filing data available - unable to assess revenue patterns"
            })
            return risks

        sorted_filings = sorted(filings, key=lambda f: f.filing_period)

        consecutive_late = 0
        max_consecutive_late = 0
        for f in sorted_filings:
            if not f.is_on_time:
                consecutive_late += 1
                max_consecutive_late = max(max_consecutive_late, consecutive_late)
            else:
                consecutive_late = 0

        if max_consecutive_late >= 3:
            risks.append({
                "severity": "high",
                "category": "compliance",
                "description": f"Consecutive late GST filings detected ({max_consecutive_late} months) - indicates cash flow stress or compliance negligence"
            })

        turnovers = [f.taxable_turnover for f in sorted_filings if f.taxable_turnover]
        if len(turnovers) >= 6:
            recent_3 = np.mean(turnovers[-3:])
            prev_3 = np.mean(turnovers[-6:-3])
            if prev_3 > 0 and recent_3 < prev_3 * 0.7:
                decline = ((prev_3 - recent_3) / prev_3) * 100
                risks.append({
                    "severity": "high",
                    "category": "revenue_decline",
                    "description": f"Sharp revenue decline of {decline:.1f}% in recent quarter compared to previous quarter"
                })

        if turnovers and len(turnovers) >= 3:
            recent = turnovers[-1]
            avg = np.mean(turnovers[:-1])
            if avg > 0 and recent > avg * 3:
                risks.append({
                    "severity": "moderate",
                    "category": "anomaly",
                    "description": "Sudden spike in reported revenue - may need verification"
                })

        return risks

    def _check_upi_risks(self, transactions: List[UPITransaction]) -> List[Dict[str, str]]:
        """Check UPI transaction risk patterns."""
        risks = []
        if not transactions:
            return risks

        monthly_credits = defaultdict(float)
        monthly_debits = defaultdict(float)
        for t in transactions:
            key = t.transaction_date.strftime("%Y-%m")
            if t.is_credit:
                monthly_credits[key] += t.amount
            else:
                monthly_debits[key] += t.amount

        sorted_months = sorted(monthly_credits.keys())
        if len(sorted_months) >= 3:
            recent_months = sorted_months[-3:]
            for month in recent_months:
                if monthly_debits.get(month, 0) > monthly_credits.get(month, 0) * 1.5:
                    risks.append({
                        "severity": "moderate",
                        "category": "cash_flow",
                        "description": f"Outflows significantly exceed inflows in {month} - potential cash crunch"
                    })
                    break

        credit_counterparties = defaultdict(float)
        for t in transactions:
            if t.is_credit and t.counterparty_vpa:
                credit_counterparties[t.counterparty_vpa] += t.amount

        if credit_counterparties:
            total_credits = sum(credit_counterparties.values())
            top_customer_share = max(credit_counterparties.values()) / total_credits if total_credits > 0 else 0
            if top_customer_share > 0.5:
                risks.append({
                    "severity": "moderate",
                    "category": "concentration",
                    "description": f"High customer concentration - top customer accounts for {top_customer_share*100:.0f}% of revenue"
                })

        if sorted_months and len(sorted_months) >= 2:
            last_month_credits = monthly_credits.get(sorted_months[-1], 0)
            prev_avg = np.mean([monthly_credits.get(m, 0) for m in sorted_months[:-1]])
            if prev_avg > 0 and last_month_credits < prev_avg * 0.5:
                risks.append({
                    "severity": "high",
                    "category": "revenue_drop",
                    "description": "Significant drop in UPI collections in the most recent month"
                })

        return risks

    def _check_epfo_risks(self, contributions: List[EPFOContribution]) -> List[Dict[str, str]]:
        """Check EPFO compliance risk patterns."""
        risks = []
        if not contributions:
            return risks

        sorted_c = sorted(contributions, key=lambda c: c.contribution_month)

        late_count = sum(1 for c in sorted_c if not c.is_on_time)
        if len(sorted_c) > 0 and late_count / len(sorted_c) > 0.4:
            risks.append({
                "severity": "moderate",
                "category": "compliance",
                "description": f"Frequent EPF payment delays ({late_count}/{len(sorted_c)} months late) - regulatory risk"
            })

        emp_counts = [c.num_employees for c in sorted_c if c.num_employees]
        if len(emp_counts) >= 6:
            recent_avg = np.mean(emp_counts[-3:])
            earlier_avg = np.mean(emp_counts[:3])
            if earlier_avg > 0 and recent_avg < earlier_avg * 0.7:
                decline = ((earlier_avg - recent_avg) / earlier_avg) * 100
                risks.append({
                    "severity": "high",
                    "category": "workforce",
                    "description": f"Significant workforce reduction of {decline:.0f}% - may indicate business distress"
                })

        contributions_amt = [c.total_contribution for c in sorted_c if c.total_contribution]
        if len(contributions_amt) >= 3:
            recent = contributions_amt[-1]
            avg = np.mean(contributions_amt[:-1])
            if avg > 0 and recent < avg * 0.5:
                risks.append({
                    "severity": "moderate",
                    "category": "compliance",
                    "description": "Sharp drop in EPF contribution amount - possible salary cuts or layoffs"
                })

        return risks

    def _check_bank_risks(self, statements: List[BankStatement]) -> List[Dict[str, str]]:
        """Check bank statement risk patterns."""
        risks = []
        if not statements:
            return risks

        sorted_s = sorted(statements, key=lambda s: s.month)

        for s in sorted_s[-3:]:
            if s.min_balance is not None and s.min_balance < 0:
                risks.append({
                    "severity": "high",
                    "category": "liquidity",
                    "description": f"Account went into overdraft in {s.month} - severe liquidity stress"
                })
                break

        closing_balances = [s.closing_balance for s in sorted_s if s.closing_balance is not None]
        if len(closing_balances) >= 3:
            declining = all(closing_balances[i] < closing_balances[i-1] for i in range(max(1, len(closing_balances)-3), len(closing_balances)))
            if declining:
                risks.append({
                    "severity": "moderate",
                    "category": "balance_decline",
                    "description": "Consistently declining bank balance over recent months"
                })

        for s in sorted_s[-3:]:
            if s.total_credits and s.emi_outflows:
                emi_ratio = s.emi_outflows / s.total_credits
                if emi_ratio > 0.5:
                    risks.append({
                        "severity": "high",
                        "category": "debt_burden",
                        "description": f"EMI outflows exceed 50% of income in {s.month} - high debt burden"
                    })
                    break

        return risks

    def _check_cross_source_risks(
        self,
        gst_filings: List[GSTFiling],
        upi_transactions: List[UPITransaction],
        epfo_contributions: List[EPFOContribution],
        bank_statements: List[BankStatement],
    ) -> List[Dict[str, str]]:
        """Check risks that emerge from cross-referencing multiple data sources."""
        risks = []

        if gst_filings and bank_statements:
            gst_revenue = sum(f.taxable_turnover for f in gst_filings if f.taxable_turnover) / max(len(gst_filings), 1)
            bank_credits = np.mean([s.total_credits for s in bank_statements if s.total_credits]) if bank_statements else 0

            if gst_revenue > 0 and bank_credits > 0:
                discrepancy = abs(gst_revenue - bank_credits) / gst_revenue
                if discrepancy > 0.5:
                    risks.append({
                        "severity": "moderate",
                        "category": "data_mismatch",
                        "description": "Significant discrepancy between GST-reported revenue and bank inflows - needs reconciliation"
                    })

        if gst_filings and epfo_contributions:
            gst_trend_up = False
            epfo_trend_down = False

            turnovers = [f.taxable_turnover for f in sorted(gst_filings, key=lambda f: f.filing_period) if f.taxable_turnover]
            emp_counts = [c.num_employees for c in sorted(epfo_contributions, key=lambda c: c.contribution_month) if c.num_employees]

            if len(turnovers) >= 6:
                recent_rev = np.mean(turnovers[-3:])
                early_rev = np.mean(turnovers[:3])
                gst_trend_up = recent_rev > early_rev * 1.2

            if len(emp_counts) >= 6:
                recent_emp = np.mean(emp_counts[-3:])
                early_emp = np.mean(emp_counts[:3])
                epfo_trend_down = recent_emp < early_emp * 0.85

            if gst_trend_up and epfo_trend_down:
                risks.append({
                    "severity": "moderate",
                    "category": "inconsistency",
                    "description": "Revenue growing but workforce shrinking - may indicate informal labor or over-reported revenue"
                })

        return risks
