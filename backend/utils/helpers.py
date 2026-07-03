import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np


def generate_gstin(state_code: str, pan: str) -> str:
    """Generate a valid-format GSTIN: 2-digit state + 10-char PAN + 1 entity + 1 check + Z"""
    entity_code = random.choice(string.digits[1:])
    return f"{state_code}{pan}{entity_code}Z" + random.choice(string.ascii_uppercase + string.digits)


def generate_pan() -> str:
    """Generate a valid-format PAN number."""
    first_three = ''.join(random.choices(string.ascii_uppercase, k=3))
    fourth = random.choice(['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G'])
    fifth = random.choice(string.ascii_uppercase)
    digits = ''.join(random.choices(string.digits, k=4))
    last = random.choice(string.ascii_uppercase)
    return f"{first_three}{fourth}{fifth}{digits}{last}"


def generate_udyam_number(state_code: str) -> str:
    """Generate Udyam registration number format: UDYAM-XX-00-0000000"""
    district = f"{random.randint(1, 50):02d}"
    serial = f"{random.randint(1, 9999999):07d}"
    return f"UDYAM-{state_code}-{district}-{serial}"


def generate_upi_id(business_name: str) -> str:
    """Generate a realistic UPI VPA."""
    clean_name = business_name.lower().replace(" ", "").replace(".", "")[:15]
    suffix = random.choice(["@ybl", "@paytm", "@ibl", "@axl", "@oksbi", "@upi"])
    return f"{clean_name}{suffix}"


def generate_epfo_id() -> str:
    """Generate EPFO establishment ID."""
    region = random.choice(["MH", "KA", "TN", "GJ", "DL", "RJ", "UP", "TG"])
    code = f"{random.randint(10000, 99999)}"
    sub = f"{random.randint(100, 999)}"
    return f"{region}/{code}/{sub}"


def generate_bank_account() -> str:
    """Generate a realistic bank account number."""
    return ''.join(random.choices(string.digits, k=random.choice([11, 12, 14])))


def generate_ifsc(bank_prefix: str) -> str:
    """Generate IFSC code."""
    branch = f"{random.randint(1000, 9999):04d}"
    return f"{bank_prefix}0{branch}"


def calculate_cagr(start_value: float, end_value: float, years: float) -> float:
    """Calculate Compound Annual Growth Rate."""
    if start_value <= 0 or years <= 0:
        return 0.0
    return (pow(end_value / start_value, 1 / years) - 1) * 100


def calculate_coefficient_of_variation(values: List[float]) -> float:
    """Calculate coefficient of variation (std/mean * 100)."""
    if not values or np.mean(values) == 0:
        return 0.0
    return (np.std(values) / np.mean(values)) * 100


def calculate_trend_slope(values: List[float]) -> float:
    """Calculate linear trend slope using least squares."""
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values))
    coefficients = np.polyfit(x, values, 1)
    return coefficients[0]


def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to 0-100 scale."""
    if max_val == min_val:
        return 50.0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0.0, min(100.0, normalized))


def calculate_dscr(net_operating_income: float, total_debt_service: float) -> float:
    """Calculate Debt Service Coverage Ratio."""
    if total_debt_service == 0:
        return 3.0
    return net_operating_income / total_debt_service


def format_indian_currency(amount: float) -> str:
    """Format amount in Indian currency notation (lakhs/crores)."""
    if amount >= 10000000:
        return f"Rs. {amount / 10000000:.2f} Cr"
    elif amount >= 100000:
        return f"Rs. {amount / 100000:.2f} L"
    else:
        return f"Rs. {amount:,.0f}"


def get_financial_year(date: datetime) -> str:
    """Get Indian financial year string for a date."""
    if date.month >= 4:
        return f"FY{date.year}-{(date.year + 1) % 100:02d}"
    else:
        return f"FY{date.year - 1}-{date.year % 100:02d}"


def calculate_moving_average(values: List[float], window: int = 3) -> List[float]:
    """Calculate simple moving average."""
    if len(values) < window:
        return values
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        result.append(np.mean(values[start:i + 1]))
    return result


def detect_seasonality(values: List[float], period: int = 12) -> float:
    """Detect seasonality strength (0-1) in a time series."""
    if len(values) < period * 2:
        return 0.0
    seasonal_avgs = []
    for i in range(period):
        season_values = [values[j] for j in range(i, len(values), period)]
        seasonal_avgs.append(np.mean(season_values))
    overall_avg = np.mean(values)
    if overall_avg == 0:
        return 0.0
    seasonal_strength = np.std(seasonal_avgs) / overall_avg
    return min(1.0, seasonal_strength)


def generate_consent_id() -> str:
    """Generate AA consent artifact ID."""
    return f"CONSENT-{datetime.now().strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"


def calculate_percentile(value: float, values: List[float]) -> float:
    """Calculate percentile rank of a value within a distribution."""
    if not values:
        return 50.0
    sorted_vals = sorted(values)
    count_below = sum(1 for v in sorted_vals if v < value)
    return (count_below / len(sorted_vals)) * 100
