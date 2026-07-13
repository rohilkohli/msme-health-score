"""Tests for the scoring engine."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from services.scoring_engine import ScoringEngine
from services.gst_service import GSTService
from services.upi_service import UPIService
from services.epfo_service import EPFOService
from services.aa_service import AAService
from models.enums import ScoreCategory, RiskLevel


def make_gst_filing(period, turnover, on_time=True):
    filing = MagicMock()
    filing.filing_period = period
    filing.taxable_turnover = turnover
    filing.tax_paid = turnover * 0.12
    filing.is_on_time = on_time
    filing.itc_claimed = turnover * 0.05
    filing.filing_date = datetime.now()
    filing.due_date = datetime.now()
    return filing


def make_upi_txn(amount, is_credit, days_ago=0, counterparty="cust@upi"):
    txn = MagicMock()
    txn.amount = amount
    txn.is_credit = is_credit
    txn.transaction_date = datetime.now() - timedelta(days=days_ago)
    txn.counterparty_vpa = counterparty
    txn.category = "Sales" if is_credit else "Purchase"
    return txn


def make_epfo(month, employees, on_time=True):
    c = MagicMock()
    c.contribution_month = month
    c.num_employees = employees
    c.total_contribution = employees * 5000
    c.employee_contribution = employees * 2500
    c.employer_contribution = employees * 2500
    c.is_on_time = on_time
    c.due_date = datetime.now()
    c.payment_date = datetime.now()
    return c


def make_bank_statement(month, credits, debits, emi=0):
    s = MagicMock()
    s.month = month
    s.total_credits = credits
    s.total_debits = debits
    s.opening_balance = 500000
    s.closing_balance = 500000 + credits - debits
    s.avg_daily_balance = 500000
    s.min_balance = 200000
    s.max_balance = 800000
    s.emi_outflows = emi
    s.salary_outflows = debits * 0.3
    s.tax_outflows = debits * 0.05
    s.num_credit_transactions = 30
    s.num_debit_transactions = 45
    return s


class TestGSTService:
    def test_high_compliance_score(self):
        service = GSTService()
        filings = [make_gst_filing(f"2025-{m:02d}", 500000 + m * 10000, on_time=True) for m in range(1, 13)]
        score, metrics, insights = service.compute_revenue_stability_score(filings)
        assert score >= 70
        assert metrics["filing_consistency"] >= 90

    def test_low_compliance_score(self):
        service = GSTService()
        filings = [make_gst_filing(f"2025-{m:02d}", 500000, on_time=(m % 3 == 0)) for m in range(1, 13)]
        score, metrics, insights = service.compute_revenue_stability_score(filings)
        assert metrics["filing_consistency"] < 50

    def test_empty_filings(self):
        service = GSTService()
        score, metrics, insights = service.compute_revenue_stability_score([])
        assert score == 50.0


class TestUPIService:
    def test_healthy_cash_flow(self):
        service = UPIService()
        txns = []
        for day in range(60):
            txns.append(make_upi_txn(10000, True, days_ago=day, counterparty=f"cust{day%10}@upi"))
            txns.append(make_upi_txn(6000, False, days_ago=day))
        score, metrics, insights = service.compute_cash_flow_score(txns)
        assert score >= 50
        assert metrics["inflow_outflow_ratio"] >= 50

    def test_stressed_cash_flow(self):
        service = UPIService()
        txns = []
        for day in range(60):
            txns.append(make_upi_txn(5000, True, days_ago=day))
            txns.append(make_upi_txn(8000, False, days_ago=day))
        score, metrics, insights = service.compute_cash_flow_score(txns)
        assert score < 60


class TestEPFOService:
    def test_good_compliance(self):
        service = EPFOService()
        contributions = [make_epfo(f"2025-{m:02d}", 20, on_time=True) for m in range(1, 13)]
        score, metrics, insights = service.compute_compliance_score(contributions, gst_on_time_ratio=0.9)
        assert score >= 70

    def test_poor_compliance(self):
        service = EPFOService()
        contributions = [make_epfo(f"2025-{m:02d}", 20, on_time=(m > 9)) for m in range(1, 13)]
        score, metrics, insights = service.compute_compliance_score(contributions, gst_on_time_ratio=0.4)
        assert score < 60


class TestAAService:
    def test_repayment_capacity(self):
        service = AAService()
        statements = [make_bank_statement(f"2025-{m:02d}", 1000000, 700000, emi=100000) for m in range(1, 13)]
        score, metrics, insights = service.compute_repayment_capacity(statements)
        assert score >= 50
        assert "dscr_indicator" in metrics


class TestScoreCategory:
    def test_categories(self):
        assert ScoreCategory.from_score(850) == ScoreCategory.VERY_STRONG
        assert ScoreCategory.from_score(720) == ScoreCategory.STRONG
        assert ScoreCategory.from_score(620) == ScoreCategory.MODERATE
        assert ScoreCategory.from_score(520) == ScoreCategory.WEAK
        assert ScoreCategory.from_score(300) == ScoreCategory.HIGH_RISK


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
