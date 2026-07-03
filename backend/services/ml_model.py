import os
import numpy as np
from typing import Dict, Tuple, Optional, List
import joblib
from pathlib import Path


class MLModelService:
    """Service for ML-based predictive scoring using Random Forest."""

    def __init__(self):
        self.model = None
        self.feature_columns = None
        self._load_model()

    def _load_model(self):
        """Load trained model from artifacts directory."""
        model_path = Path("ml/model_artifacts/health_score_model.joblib")
        columns_path = Path("ml/model_artifacts/feature_columns.joblib")

        if model_path.exists() and columns_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.feature_columns = joblib.load(columns_path)
            except Exception:
                self.model = None
                self.feature_columns = None

    def predict(self, features: Dict[str, float]) -> Tuple[Optional[float], Optional[Dict[str, float]]]:
        """
        Predict creditworthiness score using the trained model.

        Returns:
            Tuple of (prediction_score 0-100, feature_importance_dict)
        """
        if self.model is None or self.feature_columns is None:
            return self._fallback_prediction(features)

        feature_vector = []
        for col in self.feature_columns:
            feature_vector.append(features.get(col, 0))

        feature_array = np.array([feature_vector])

        try:
            prediction = self.model.predict(feature_array)[0]
            prediction_score = float(np.clip(prediction * 100, 0, 100))

            importances = self.model.feature_importances_
            importance_dict = {
                col: round(float(imp), 4)
                for col, imp in zip(self.feature_columns, importances)
            }
            sorted_importance = dict(
                sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:10]
            )

            return round(prediction_score, 2), sorted_importance
        except Exception:
            return self._fallback_prediction(features)

    def _fallback_prediction(self, features: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Fallback heuristic prediction when ML model is not available.
        Uses a weighted formula based on key features.
        """
        score_components = []

        compliance = features.get("gst_compliance_rate", 0.5)
        score_components.append(compliance * 20)

        epfo = features.get("epfo_compliance_rate", 0.5)
        score_components.append(epfo * 15)

        cr_ratio = features.get("credit_debit_ratio", 1.0)
        ratio_score = min(cr_ratio / 2.0, 1.0) * 20
        score_components.append(ratio_score)

        volatility = features.get("revenue_volatility", 0.5)
        stability_score = (1 - min(volatility, 1.0)) * 15
        score_components.append(stability_score)

        emi_ratio = features.get("emi_to_income_ratio", 0.3)
        emi_score = (1 - min(emi_ratio, 1.0)) * 15
        score_components.append(emi_score)

        years = features.get("years_in_business", 3)
        experience_score = min(years / 10.0, 1.0) * 15
        score_components.append(experience_score)

        total_score = sum(score_components)

        importance = {
            "gst_compliance_rate": 0.20,
            "credit_debit_ratio": 0.20,
            "epfo_compliance_rate": 0.15,
            "revenue_volatility": 0.15,
            "emi_to_income_ratio": 0.15,
            "years_in_business": 0.15,
        }

        return round(total_score, 2), importance

    def retrain(self, training_data: List[Dict], labels: List[float]) -> bool:
        """
        Retrain the model with new data.

        Args:
            training_data: List of feature dictionaries
            labels: List of target scores (0-1)

        Returns:
            True if training successful
        """
        try:
            from sklearn.ensemble import RandomForestRegressor

            if not training_data:
                return False

            self.feature_columns = sorted(training_data[0].keys())

            X = []
            for record in training_data:
                row = [record.get(col, 0) for col in self.feature_columns]
                X.append(row)

            X = np.array(X)
            y = np.array(labels)

            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            )
            self.model.fit(X, y)

            os.makedirs("ml/model_artifacts", exist_ok=True)
            joblib.dump(self.model, "ml/model_artifacts/health_score_model.joblib")
            joblib.dump(self.feature_columns, "ml/model_artifacts/feature_columns.joblib")

            return True
        except Exception as e:
            print(f"Model training failed: {e}")
            return False
