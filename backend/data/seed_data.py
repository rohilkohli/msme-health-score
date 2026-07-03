"""
Generate realistic synthetic MSME data for demonstration.
Run: python data/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from models.database import (
    init_db, SessionLocal, User, MSME, DataSource,
    GSTFiling, UPITransaction, EPFOContribution, BankStatement, HealthScore
)
from utils.helpers import (
    generate_pan, generate_gstin, generate_udyam_number,
    generate_upi_id, generate_epfo_id, generate_bank_account, generate_ifsc
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

INDIAN_STATES = {
    "27": "Maharashtra", "29": "Karnataka", "33": "Tamil Nadu",
    "24": "Gujarat", "07": "Delhi", "06": "Haryana",
    "08": "Rajasthan", "09": "Uttar Pradesh", "36": "Telangana",
    "32": "Kerala",
}

CITIES = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangalore"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
    "Uttar Pradesh": ["Noida", "Lucknow", "Kanpur", "Agra"],
    "Telangana": ["Hyderabad", "Warangal", "Karimnagar"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
}

BUSINESS_NAMES = [
    "Sri Lakshmi Textiles", "Bharat Electronics Works", "Ganga Steel Fabricators",
    "Patel Engineering Solutions", "Krishna Auto Parts", "Sharma IT Services",
    "Sai Precision Tools", "Jai Hind Packaging", "Annapurna Foods Pvt Ltd",
    "Durga Manufacturing Co", "NextGen Software Labs", "Green Valley Organics",
    "Pioneer Plastics", "Excel Machine Works", "Shree Ram Traders",
    "TechVista Solutions", "Sunrise Pharma", "Vishwakarma Foundry",
    "Apex Digital Marketing", "Rajesh Exports", "InfoBridge Technologies",
    "Mahesh Agro Industries", "Priya Fashion House", "Ganesh Paper Mills",
    "Srinivasa Constructions", "AKS Engineering", "Neelam Chemicals",
    "Om Sai Electronics", "Global Freight Logistics", "Dhanush Automotive",
    "CloudNine IT Solutions", "Raman Bio Sciences", "Narmada Cement Works",
    "Jayant Rubber Industries", "Pinnacle Design Studio", "Saraswati Publishers",
    "Balaji Cold Storage", "Matrix Infotech", "Heritage Handicrafts",
    "Kunal Food Processing", "Stellar Innovations", "Venkatesh Textiles",
    "Pacific Marine Exports", "Digital Dreams Agency", "Shakti Power Solutions",
    "Golden Harvest Mills", "Alpha Diagnostics", "Metro Logistics Services",
    "Sankalp Solar Energy", "Vande Mataram Steels"
]

INDUSTRIES = [
    "Manufacturing", "Services", "Trading", "Technology",
    "Food Processing", "Textiles", "Healthcare", "Logistics",
    "Construction", "Agriculture"
]

BANK_PREFIXES = ["IDBI", "SBIN", "HDFC", "ICIC", "UTIB", "PUNB", "BARB"]

UPI_COUNTERPARTIES = [
    "customer1@upi", "vendor_abc@paytm", "rawmaterial.shop@ybl",
    "logistics.co@oksbi", "electricity.board@npci", "salary.emp@ibl",
    "rent.landlord@axl", "gst.gov@rbi", "insurance.premium@ybl",
    "maintenance@upi", "supplier.steel@paytm", "client.order@ybl",
    "bulk.buyer@oksbi", "export.agent@ibl", "raw.cotton@axl",
    "fuel.station@upi", "courier.service@paytm", "advert.agency@ybl",
]


def generate_msme_profile(idx: int, state_code: str, state_name: str) -> dict:
    pan = generate_pan()
    business_type = random.choices(["Micro", "Small", "Medium"], weights=[0.5, 0.35, 0.15])[0]

    if business_type == "Micro":
        turnover_range = (500000, 5000000)
        emp_range = (2, 15)
    elif business_type == "Small":
        turnover_range = (5000000, 50000000)
        emp_range = (10, 80)
    else:
        turnover_range = (50000000, 250000000)
        emp_range = (50, 300)

    return {
        "business_name": BUSINESS_NAMES[idx],
        "gstin": generate_gstin(state_code, pan),
        "pan": pan,
        "udyam_number": generate_udyam_number(state_code),
        "business_type": business_type,
        "industry": random.choice(INDUSTRIES),
        "state": state_name,
        "city": random.choice(CITIES.get(state_name, ["Unknown"])),
        "pincode": f"{random.randint(100, 999)}{random.randint(100, 999):03d}",
        "annual_turnover": random.uniform(*turnover_range),
        "employee_count": random.randint(*emp_range),
        "year_established": random.randint(2005, 2022),
        "upi_id": generate_upi_id(BUSINESS_NAMES[idx]),
        "epfo_establishment_id": generate_epfo_id(),
        "bank_account_number": generate_bank_account(),
        "ifsc_code": generate_ifsc(random.choice(BANK_PREFIXES)),
    }


def generate_gst_filings(msme_id: int, months: int = 24, health_profile: str = "good") -> list:
    filings = []
    base_turnover = random.uniform(200000, 5000000)

    if health_profile == "excellent":
        growth_rate = random.uniform(0.02, 0.05)
        on_time_prob = 0.95
        variance = 0.1
    elif health_profile == "good":
        growth_rate = random.uniform(0.01, 0.03)
        on_time_prob = 0.85
        variance = 0.15
    elif health_profile == "fair":
        growth_rate = random.uniform(-0.01, 0.02)
        on_time_prob = 0.70
        variance = 0.25
    else:
        growth_rate = random.uniform(-0.03, 0.0)
        on_time_prob = 0.50
        variance = 0.35

    for i in range(months):
        month_offset = months - i
        filing_date = datetime.now() - timedelta(days=month_offset * 30)
        period = filing_date.strftime("%Y-%m")
        due_date = filing_date.replace(day=20)

        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * filing_date.month / 12)
        growth_factor = (1 + growth_rate) ** i
        noise = random.uniform(1 - variance, 1 + variance)

        turnover = base_turnover * growth_factor * seasonal_factor * noise
        tax_rate = random.uniform(0.05, 0.18)
        tax_paid = turnover * tax_rate
        itc = tax_paid * random.uniform(0.3, 0.7)

        is_on_time = random.random() < on_time_prob
        actual_filing = due_date - timedelta(days=random.randint(1, 5)) if is_on_time else due_date + timedelta(days=random.randint(1, 30))

        filings.append({
            "msme_id": msme_id,
            "filing_period": period,
            "filing_date": actual_filing,
            "due_date": due_date,
            "return_type": random.choice(["GSTR-3B", "GSTR-1"]),
            "taxable_turnover": round(turnover, 2),
            "tax_paid": round(tax_paid, 2),
            "is_on_time": is_on_time,
            "itc_claimed": round(itc, 2),
            "filing_status": "Filed",
        })
    return filings


def generate_upi_transactions(msme_id: int, days: int = 180, health_profile: str = "good") -> list:
    transactions = []

    if health_profile == "excellent":
        daily_txn_range = (5, 15)
        credit_ratio = 0.65
        avg_amount = random.uniform(5000, 50000)
    elif health_profile == "good":
        daily_txn_range = (3, 10)
        credit_ratio = 0.58
        avg_amount = random.uniform(3000, 30000)
    elif health_profile == "fair":
        daily_txn_range = (2, 7)
        credit_ratio = 0.52
        avg_amount = random.uniform(2000, 20000)
    else:
        daily_txn_range = (1, 5)
        credit_ratio = 0.45
        avg_amount = random.uniform(1000, 15000)

    for day in range(days):
        date = datetime.now() - timedelta(days=days - day)
        num_txns = random.randint(*daily_txn_range)

        for _ in range(num_txns):
            is_credit = random.random() < credit_ratio
            amount = abs(np.random.lognormal(np.log(avg_amount), 0.8))
            amount = round(min(amount, avg_amount * 10), 2)

            transactions.append({
                "msme_id": msme_id,
                "transaction_date": date + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                "amount": amount,
                "transaction_type": "CREDIT" if is_credit else "DEBIT",
                "counterparty_vpa": random.choice(UPI_COUNTERPARTIES),
                "category": random.choice(["Sales", "Purchase", "Salary", "Rent", "Utilities", "Marketing", "Transport"]),
                "reference_id": f"TXN{random.randint(100000000, 999999999)}",
                "is_credit": is_credit,
            })
    return transactions


def generate_epfo_contributions(msme_id: int, months: int = 24, employee_count: int = 10, health_profile: str = "good") -> list:
    contributions = []
    base_employees = employee_count

    if health_profile == "excellent":
        on_time_prob = 0.95
        growth = 0.02
    elif health_profile == "good":
        on_time_prob = 0.82
        growth = 0.01
    elif health_profile == "fair":
        on_time_prob = 0.65
        growth = 0.0
    else:
        on_time_prob = 0.45
        growth = -0.02

    for i in range(months):
        month_offset = months - i
        date = datetime.now() - timedelta(days=month_offset * 30)
        period = date.strftime("%Y-%m")
        due_date = date.replace(day=15)

        current_employees = max(2, int(base_employees * (1 + growth) ** i + random.randint(-1, 1)))
        avg_salary = random.uniform(15000, 45000)
        employee_contribution = current_employees * avg_salary * 0.12
        employer_contribution = current_employees * avg_salary * 0.12
        total = employee_contribution + employer_contribution

        is_on_time = random.random() < on_time_prob
        payment_date = due_date - timedelta(days=random.randint(1, 3)) if is_on_time else due_date + timedelta(days=random.randint(1, 20))

        contributions.append({
            "msme_id": msme_id,
            "contribution_month": period,
            "due_date": due_date,
            "payment_date": payment_date,
            "employee_contribution": round(employee_contribution, 2),
            "employer_contribution": round(employer_contribution, 2),
            "total_contribution": round(total, 2),
            "num_employees": current_employees,
            "is_on_time": is_on_time,
            "challan_number": f"ECR-{random.randint(10000000, 99999999)}",
        })
    return contributions


def generate_bank_statements(msme_id: int, months: int = 12, annual_turnover: float = 5000000, health_profile: str = "good") -> list:
    statements = []
    monthly_income = annual_turnover / 12
    opening_balance = random.uniform(monthly_income * 0.5, monthly_income * 2)

    if health_profile == "excellent":
        credit_multiplier = 1.3
        debit_ratio = 0.75
        emi_ratio = 0.1
    elif health_profile == "good":
        credit_multiplier = 1.1
        debit_ratio = 0.85
        emi_ratio = 0.15
    elif health_profile == "fair":
        credit_multiplier = 0.95
        debit_ratio = 0.95
        emi_ratio = 0.25
    else:
        credit_multiplier = 0.8
        debit_ratio = 1.1
        emi_ratio = 0.35

    for i in range(months):
        month_offset = months - i
        date = datetime.now() - timedelta(days=month_offset * 30)
        period = date.strftime("%Y-%m")

        total_credits = monthly_income * credit_multiplier * random.uniform(0.8, 1.2)
        total_debits = total_credits * debit_ratio * random.uniform(0.85, 1.15)
        emi_outflows = total_credits * emi_ratio * random.uniform(0.9, 1.1)
        salary_outflows = total_credits * random.uniform(0.2, 0.4)
        tax_outflows = total_credits * random.uniform(0.03, 0.08)

        closing_balance = opening_balance + total_credits - total_debits
        avg_daily = (opening_balance + closing_balance) / 2
        min_balance = min(opening_balance, closing_balance) * random.uniform(0.3, 0.8)
        max_balance = max(opening_balance, closing_balance) * random.uniform(1.1, 1.5)

        statements.append({
            "msme_id": msme_id,
            "month": period,
            "opening_balance": round(opening_balance, 2),
            "closing_balance": round(closing_balance, 2),
            "total_credits": round(total_credits, 2),
            "total_debits": round(total_debits, 2),
            "num_credit_transactions": random.randint(15, 80),
            "num_debit_transactions": random.randint(20, 100),
            "avg_daily_balance": round(avg_daily, 2),
            "min_balance": round(max(0, min_balance), 2),
            "max_balance": round(max_balance, 2),
            "emi_outflows": round(emi_outflows, 2),
            "salary_outflows": round(salary_outflows, 2),
            "tax_outflows": round(tax_outflows, 2),
        })
        opening_balance = closing_balance

    return statements


def seed_database():
    print("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already seeded. Skipping.")
            return

        print("Creating demo user...")
        demo_user = User(
            email="demo@idbihealthscore.in",
            hashed_password=pwd_context.hash("demo123"),
            full_name="IDBI Demo User",
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        admin_user = User(
            email="admin@idbihealthscore.in",
            hashed_password=pwd_context.hash("admin123"),
            full_name="Platform Administrator",
        )
        db.add(admin_user)
        db.commit()

        print("Generating 50 MSME profiles...")
        state_codes = list(INDIAN_STATES.keys())
        health_profiles = ["excellent"] * 10 + ["good"] * 20 + ["fair"] * 12 + ["poor"] * 8

        msme_objects = []
        for idx in range(50):
            state_code = random.choice(state_codes)
            state_name = INDIAN_STATES[state_code]
            profile_data = generate_msme_profile(idx, state_code, state_name)

            msme = MSME(user_id=demo_user.id, **profile_data)
            db.add(msme)
            db.commit()
            db.refresh(msme)
            msme_objects.append((msme, health_profiles[idx]))

            for source_type in ["GST", "UPI", "EPFO", "Account Aggregator"]:
                ds = DataSource(
                    msme_id=msme.id,
                    source_type=source_type,
                    status="completed",
                    consent_id=f"CONSENT-SEED-{msme.id}-{source_type[:3]}",
                    connected_at=datetime.utcnow(),
                    last_fetched_at=datetime.utcnow(),
                )
                db.add(ds)

        db.commit()
        print("MSME profiles created.")

        print("Generating transaction data (this may take a moment)...")
        for msme, health_profile in msme_objects:
            gst_filings = generate_gst_filings(msme.id, months=24, health_profile=health_profile)
            for f in gst_filings:
                db.add(GSTFiling(**f))

            upi_txns = generate_upi_transactions(msme.id, days=180, health_profile=health_profile)
            for t in upi_txns:
                db.add(UPITransaction(**t))

            epfo = generate_epfo_contributions(msme.id, months=24, employee_count=msme.employee_count, health_profile=health_profile)
            for c in epfo:
                db.add(EPFOContribution(**c))

            bank = generate_bank_statements(msme.id, months=12, annual_turnover=msme.annual_turnover, health_profile=health_profile)
            for s in bank:
                db.add(BankStatement(**s))

        db.commit()
        print("Transaction data generated.")

        print("Computing health scores for all MSMEs...")
        from services.scoring_engine import ScoringEngine
        engine = ScoringEngine()

        for msme, _ in msme_objects:
            gst = db.query(GSTFiling).filter(GSTFiling.msme_id == msme.id).all()
            upi = db.query(UPITransaction).filter(UPITransaction.msme_id == msme.id).all()
            epfo = db.query(EPFOContribution).filter(EPFOContribution.msme_id == msme.id).all()
            bank = db.query(BankStatement).filter(BankStatement.msme_id == msme.id).all()

            result = engine.compute_health_score(msme, gst, upi, epfo, bank)

            score_record = HealthScore(
                msme_id=msme.id,
                composite_score=result.composite_score,
                revenue_stability=result.dimensions["revenue_stability"].score,
                cash_flow_health=result.dimensions["cash_flow_health"].score,
                compliance_score=result.dimensions["compliance_score"].score,
                growth_trajectory=result.dimensions["growth_trajectory"].score,
                repayment_capacity=result.dimensions["repayment_capacity"].score,
                category=result.category,
                risk_level=result.risk_level,
                ml_prediction_score=result.ml_prediction_score,
                recommendations=json.dumps(result.recommendations),
                computed_at=datetime.utcnow(),
            )
            db.add(score_record)

        db.commit()
        print("Health scores computed.")

        print("\n=== Seeding Complete ===")
        print(f"Users: 2 (demo@idbihealthscore.in / demo123)")
        print(f"MSMEs: 50")
        print(f"GST Filings: {50 * 24}")
        print(f"EPFO Contributions: {50 * 24}")
        print(f"Bank Statements: {50 * 12}")
        print(f"UPI Transactions: ~{50 * 180 * 5}")
        print(f"Health Scores: 50")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
