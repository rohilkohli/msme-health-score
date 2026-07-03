"""Feature engineering utilities for the ML pipeline."""
import numpy as np
from typing import List, Dict
from collections import defaultdict


def compute_temporal_features(values: List[float], window: int = 3) -> Dict[str, float]:
    if not values or len(values) < 3:
        return {"trend": 0, "volatility": 0, "momentum": 0, "acceleration": 0}

    x = np.arange(len(values))
    coeffs = np.polyfit(x, values, 1)
    trend = coeffs[0]

    mean_val = np.mean(values)
    volatility = np.std(values) / mean_val if mean_val > 0 else 0

    recent = np.mean(values[-window:])
    earlier = np.mean(values[:window])
    momentum = (recent - earlier) / max(abs(earlier), 1)

    if len(values) >= 6:
        mid = len(values) // 2
        first_half_growth = np.mean(values[mid:mid+window]) - np.mean(values[:window])
        second_half_growth = np.mean(values[-window:]) - np.mean(values[mid:mid+window])
        acceleration = second_half_growth - first_half_growth
    else:
        acceleration = 0

    return {
        "trend": float(trend),
        "volatility": float(volatility),
        "momentum": float(momentum),
        "acceleration": float(acceleration),
    }


def compute_concentration_features(amounts: Dict[str, float]) -> Dict[str, float]:
    if not amounts:
        return {"hhi": 0, "top1_share": 0, "top5_share": 0, "diversity": 0}

    total = sum(amounts.values())
    if total == 0:
        return {"hhi": 0, "top1_share": 0, "top5_share": 0, "diversity": 0}

    shares = sorted([v / total for v in amounts.values()], reverse=True)
    hhi = sum(s ** 2 for s in shares)
    top1 = shares[0] if shares else 0
    top5 = sum(shares[:5])
    diversity = len([s for s in shares if s > 0.01])

    return {
        "hhi": float(hhi),
        "top1_share": float(top1),
        "top5_share": float(top5),
        "diversity": float(diversity),
    }


def compute_seasonality_features(monthly_values: Dict[str, float]) -> Dict[str, float]:
    if len(monthly_values) < 12:
        return {"seasonality_strength": 0, "peak_month": 0, "trough_month": 0}

    month_avgs = defaultdict(list)
    for period, value in monthly_values.items():
        month = int(period.split("-")[1])
        month_avgs[month].append(value)

    month_means = {m: np.mean(vals) for m, vals in month_avgs.items()}
    overall_mean = np.mean(list(month_means.values()))

    if overall_mean == 0:
        return {"seasonality_strength": 0, "peak_month": 1, "trough_month": 1}

    strength = np.std(list(month_means.values())) / overall_mean
    peak = max(month_means, key=month_means.get)
    trough = min(month_means, key=month_means.get)

    return {
        "seasonality_strength": float(strength),
        "peak_month": int(peak),
        "trough_month": int(trough),
    }


def compute_payment_behavior_features(payment_dates: List[Dict]) -> Dict[str, float]:
    if not payment_dates:
        return {"avg_delay_days": 0, "delay_volatility": 0, "improving_trend": 0}

    delays = []
    for p in payment_dates:
        due = p.get("due_date")
        actual = p.get("payment_date")
        if due and actual:
            delay = (actual - due).days
            delays.append(delay)

    if not delays:
        return {"avg_delay_days": 0, "delay_volatility": 0, "improving_trend": 0}

    avg_delay = np.mean(delays)
    delay_vol = np.std(delays)

    if len(delays) >= 6:
        recent_avg = np.mean(delays[-3:])
        earlier_avg = np.mean(delays[:3])
        improving = 1 if recent_avg < earlier_avg else -1
    else:
        improving = 0

    return {
        "avg_delay_days": float(avg_delay),
        "delay_volatility": float(delay_vol),
        "improving_trend": float(improving),
    }
