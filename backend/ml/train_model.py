"""
Train the ML model for MSME creditworthiness prediction.
Run: python ml/train_model.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
from pathlib import Path

from models.database import init_db, SessionLocal, MSME, HealthScore, GSTFiling, UPITransaction, EPFOContribution, BankStatement


def extract_features(db, msme):
    features = {}
    features["annual_turnover"] = msme.annual_turnover or 0
    features["employee_count"] = msme.employee_count or 0
    features["years_in_business"] = 2026 - (msme.year_established or 2020)

    gst_filings = db.query(GSTFiling).filter(GSTFiling.msme_id == msme.id).all()
    if gst_filings:
        turnovers = [f.taxable_turnover for f in gst_filings if f.taxable_turnover]
        features["avg_monthly_revenue"] = np.mean(turnovers) if turnovers else 0
        features["revenue_volatility"] = (np.std(turnovers) / np.mean(turnovers)) if turnovers and np.mean(turnovers) > 0 else 0.5
        features["gst_compliance_rate"] = sum(1 for f in gst_filings if f.is_on_time) / len(gst_filings)
        features["avg_tax_paid"] = np.mean([f.tax_paid for f in gst_filings if f.tax_paid]) if gst_filings else 0
        features["num_gst_filings"] = len(gst_filings)
        if len(turnovers) >= 6:
            features["revenue_growth"] = (np.mean(turnovers[-3:]) - np.mean(turnovers[:3])) / max(np.mean(turnovers[:3]), 1)
        else:
            features["revenue_growth"] = 0
    else:
        features["avg_monthly_revenue"] = 0
        features["revenue_volatility"] = 0.5
        features["gst_compliance_rate"] = 0.5
        features["avg_tax_paid"] = 0
        features["num_gst_filings"] = 0
        features["revenue_growth"] = 0

    upi_txns = db.query(UPITransaction).filter(UPITransaction.msme_id == msme.id).all()
    if upi_txns:
        credits = [t.amount for t in upi_txns if t.is_credit]
        debits = [t.amount for t in upi_txns if not t.is_credit]
        features["avg_credit_amount"] = np.mean(credits) if credits else 0
        features["avg_debit_amount"] = np.mean(debits) if debits else 0
        features["credit_debit_ratio"] = sum(credits) / max(sum(debits), 1)
        features["transaction_frequency"] = len(upi_txns) / 180.0
        features["unique_counterparties"] = len(set(t.counterparty_vpa for t in upi_txns if t.counterparty_vpa))
    else:
        features["avg_credit_amount"] = 0
        features["avg_debit_amount"] = 0
        features["credit_debit_ratio"] = 1.0
        features["transaction_frequency"] = 0
        features["unique_counterparties"] = 0

    epfo = db.query(EPFOContribution).filter(EPFOContribution.msme_id == msme.id).all()
    if epfo:
        features["epfo_compliance_rate"] = sum(1 for c in epfo if c.is_on_time) / len(epfo)
        features["avg_epfo_contribution"] = np.mean([c.total_contribution for c in epfo if c.total_contribution])
        emp_counts = [c.num_employees for c in epfo if c.num_employees]
        if len(emp_counts) >= 3:
            features["workforce_growth"] = (np.mean(emp_counts[-3:]) - np.mean(emp_counts[:3])) / max(np.mean(emp_counts[:3]), 1)
        else:
            features["workforce_growth"] = 0
    else:
        features["epfo_compliance_rate"] = 0.5
        features["avg_epfo_contribution"] = 0
        features["workforce_growth"] = 0

    bank = db.query(BankStatement).filter(BankStatement.msme_id == msme.id).all()
    if bank:
        features["avg_daily_balance"] = np.mean([s.avg_daily_balance for s in bank if s.avg_daily_balance])
        features["avg_monthly_credits"] = np.mean([s.total_credits for s in bank if s.total_credits])
        features["avg_monthly_debits"] = np.mean([s.total_debits for s in bank if s.total_debits])
        emi_list = [s.emi_outflows for s in bank if s.emi_outflows is not None]
        avg_credits = features["avg_monthly_credits"]
        features["emi_to_income_ratio"] = np.mean(emi_list) / avg_credits if avg_credits > 0 and emi_list else 0
        closing = [s.closing_balance for s in bank if s.closing_balance]
        if len(closing) >= 3:
            features["balance_trend"] = (closing[-1] - closing[0]) / max(abs(closing[0]), 1)
        else:
            features["balance_trend"] = 0
    else:
        features["avg_daily_balance"] = 0
        features["avg_monthly_credits"] = 0
        features["avg_monthly_debits"] = 0
        features["emi_to_income_ratio"] = 0
        features["balance_trend"] = 0

    return features


def train():
    print("Initializing database connection...")
    init_db()
    db = SessionLocal()

    try:
        msmes = db.query(MSME).all()
        if not msmes:
            print("No MSMEs found. Run seed_data.py first.")
            return

        print(f"Extracting features for {len(msmes)} MSMEs...")
        feature_rows = []
        labels = []

        for msme in msmes:
            score = db.query(HealthScore).filter(HealthScore.msme_id == msme.id).order_by(HealthScore.computed_at.desc()).first()
            if not score:
                continue

            features = extract_features(db, msme)
            feature_rows.append(features)
            labels.append(score.composite_score / 1000.0)

        if len(feature_rows) < 10:
            print("Not enough data for training. Need at least 10 scored MSMEs.")
            return

        df = pd.DataFrame(feature_rows)
        feature_columns = sorted(df.columns.tolist())
        X = df[feature_columns].values
        y = np.array(labels)

        print(f"Training data shape: {X.shape}")
        print(f"Feature columns: {feature_columns}")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("\nTraining Random Forest model...")
        rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )
        rf_model.fit(X_train, y_train)

        y_pred = rf_model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"\n=== Model Performance ===")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"R² Score: {r2:.4f}")

        cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring="r2")
        print(f"Cross-validation R² (5-fold): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        print("\n=== Feature Importance (Top 10) ===")
        importances = rf_model.feature_importances_
        importance_df = pd.DataFrame({
            "feature": feature_columns,
            "importance": importances
        }).sort_values("importance", ascending=False)

        for _, row in importance_df.head(10).iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")

        artifacts_dir = Path("ml/model_artifacts")
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        joblib.dump(rf_model, artifacts_dir / "health_score_model.joblib")
        joblib.dump(feature_columns, artifacts_dir / "feature_columns.joblib")
        print(f"\nModel saved to {artifacts_dir}")

        metrics = {
            "rmse": float(rmse),
            "mae": float(mae),
            "r2": float(r2),
            "cv_r2_mean": float(cv_scores.mean()),
            "cv_r2_std": float(cv_scores.std()),
            "n_features": len(feature_columns),
            "n_samples": len(feature_rows),
            "feature_columns": feature_columns,
        }
        import json
        with open(artifacts_dir / "training_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        print("\nTraining complete!")

    finally:
        db.close()


if __name__ == "__main__":
    train()
