"""
Driver Risk Prediction Model
XGBoost-based classifier for predicting high-risk drivers.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import joblib
import os

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import StandardScaler

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

import sys
sys.path.append('..')
from config import ml_config, column_config


@dataclass
class PredictionResult:
    """Container for risk prediction results"""
    transporter_id: str
    risk_score: float           # 0-100
    risk_category: str          # "high", "medium", "low"
    probability: float          # Raw probability
    top_factors: List[Dict]     # Top contributing factors
    confidence: float           # Model confidence


@dataclass
class ModelMetrics:
    """Container for model evaluation metrics"""
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    confusion_matrix: np.ndarray
    cross_val_scores: List[float]


class DriverRiskModel:
    """
    XGBoost-based Driver Risk Prediction Model
    
    Predicts probability of a driver being "high-risk" based on
    computed features from delivery/concession data.
    
    Usage:
        model = DriverRiskModel()
        model.train(features_df, labels)
        predictions = model.predict(new_features_df)
    """
    
    def __init__(self, config=None):
        self.config = config or ml_config
        self.model: Optional[XGBClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.feature_names: List[str] = []
        self.is_trained: bool = False
        self.training_date: Optional[datetime] = None
        self.model_version: str = "1.0.0"
        self.metrics: Optional[ModelMetrics] = None
        self._explainer = None
    
    def train(self, 
              X: pd.DataFrame, 
              y: pd.Series,
              eval_set: Optional[Tuple] = None) -> ModelMetrics:
        """
        Train the risk prediction model.
        
        Args:
            X: Feature matrix (from FeatureEngineer)
            y: Binary labels (1 = high-risk, 0 = normal)
            eval_set: Optional evaluation set for early stopping
            
        Returns:
            ModelMetrics with evaluation results
        """
        self.feature_names = list(X.columns)
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y,
            test_size=self.config.train_test_split,
            random_state=self.config.random_state,
            stratify=y
        )
        
        # Initialize model
        self.model = XGBClassifier(**self.config.xgb_params)
        
        # Train with early stopping if eval set available
        if eval_set is not None:
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_test, y_test)],
                early_stopping_rounds=20,
                verbose=False
            )
        else:
            self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        # Cross-validation
        cv = StratifiedKFold(n_splits=self.config.cross_validation_folds, 
                             shuffle=True, 
                             random_state=self.config.random_state)
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=cv, scoring='roc_auc')
        
        self.metrics = ModelMetrics(
            accuracy=accuracy_score(y_test, y_pred),
            precision=precision_score(y_test, y_pred, zero_division=0),
            recall=recall_score(y_test, y_pred, zero_division=0),
            f1=f1_score(y_test, y_pred, zero_division=0),
            roc_auc=roc_auc_score(y_test, y_prob),
            confusion_matrix=confusion_matrix(y_test, y_pred),
            cross_val_scores=cv_scores.tolist()
        )
        
        self.is_trained = True
        self.training_date = datetime.now()
        
        # Initialize SHAP explainer
        if SHAP_AVAILABLE:
            self._explainer = shap.TreeExplainer(self.model)
        
        return self.metrics
    
    def predict(self, X: pd.DataFrame) -> List[PredictionResult]:
        """
        Predict risk scores for drivers.
        
        Args:
            X: Feature matrix (must have same columns as training data)
            
        Returns:
            List of PredictionResult objects
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Ensure column order matches training
        X = X[self.feature_names]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)
        
        # Get predictions
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        # Get SHAP values for explanations
        shap_values = None
        if SHAP_AVAILABLE and self._explainer is not None:
            shap_values = self._explainer.shap_values(X_scaled)
        
        # Build results
        results = []
        for i, (transporter_id, prob) in enumerate(zip(X.index, probabilities)):
            # Convert probability to 0-100 score
            risk_score = prob * 100
            
            # Categorize risk
            if risk_score >= self.config.risk_threshold_high:
                risk_category = "high"
            elif risk_score >= self.config.risk_threshold_medium:
                risk_category = "medium"
            else:
                risk_category = "low"
            
            # Get top contributing factors
            top_factors = []
            if shap_values is not None:
                factor_importance = list(zip(self.feature_names, shap_values[i]))
                factor_importance.sort(key=lambda x: abs(x[1]), reverse=True)
                
                for fname, fvalue in factor_importance[:5]:
                    top_factors.append({
                        "feature": fname,
                        "impact": float(fvalue),
                        "direction": "increases risk" if fvalue > 0 else "decreases risk",
                        "value": float(X.loc[transporter_id, fname])
                    })
            
            # Calculate confidence based on probability distance from 0.5
            confidence = abs(prob - 0.5) * 2  # 0 at 50%, 1 at 0% or 100%
            
            results.append(PredictionResult(
                transporter_id=str(transporter_id),
                risk_score=round(risk_score, 1),
                risk_category=risk_category,
                probability=round(prob, 4),
                top_factors=top_factors,
                confidence=round(confidence, 3)
            ))
        
        return results
    
    def predict_single(self, X_single: pd.Series) -> PredictionResult:
        """Predict risk for a single driver"""
        X_df = pd.DataFrame([X_single])
        X_df.index = [X_single.name if X_single.name else "driver"]
        return self.predict(X_df)[0]
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance scores.
        
        Returns:
            DataFrame with features sorted by importance
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        })
        importance = importance.sort_values('importance', ascending=False)
        importance['cumulative'] = importance['importance'].cumsum()
        importance['rank'] = range(1, len(importance) + 1)
        
        return importance
    
    def save(self, path: str, version: Optional[str] = None):
        """
        Save model to disk.
        
        Args:
            path: Directory to save model files
            version: Optional version string
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Cannot save.")
        
        os.makedirs(path, exist_ok=True)
        
        version = version or self.model_version
        
        # Save model
        model_path = os.path.join(path, f"risk_model_v{version}.joblib")
        joblib.dump(self.model, model_path)
        
        # Save scaler
        scaler_path = os.path.join(path, f"scaler_v{version}.joblib")
        joblib.dump(self.scaler, scaler_path)
        
        # Save metadata
        metadata = {
            'version': version,
            'feature_names': self.feature_names,
            'training_date': self.training_date.isoformat(),
            'metrics': {
                'accuracy': self.metrics.accuracy,
                'precision': self.metrics.precision,
                'recall': self.metrics.recall,
                'f1': self.metrics.f1,
                'roc_auc': self.metrics.roc_auc,
                'cv_mean': np.mean(self.metrics.cross_val_scores),
                'cv_std': np.std(self.metrics.cross_val_scores)
            }
        }
        
        metadata_path = os.path.join(path, f"metadata_v{version}.joblib")
        joblib.dump(metadata, metadata_path)
        
        print(f"Model saved to {path}")
    
    def load(self, path: str, version: Optional[str] = None):
        """
        Load model from disk.
        
        Args:
            path: Directory containing model files
            version: Optional version string (loads latest if not specified)
        """
        if version is None:
            # Find latest version
            meta_files = [f for f in os.listdir(path) if f.startswith('metadata_v')]
            if not meta_files:
                raise ValueError(f"No model files found in {path}")
            version = meta_files[-1].replace('metadata_v', '').replace('.joblib', '')
        
        # Load model
        model_path = os.path.join(path, f"risk_model_v{version}.joblib")
        self.model = joblib.load(model_path)
        
        # Load scaler
        scaler_path = os.path.join(path, f"scaler_v{version}.joblib")
        self.scaler = joblib.load(scaler_path)
        
        # Load metadata
        metadata_path = os.path.join(path, f"metadata_v{version}.joblib")
        metadata = joblib.load(metadata_path)
        
        self.model_version = metadata['version']
        self.feature_names = metadata['feature_names']
        self.training_date = datetime.fromisoformat(metadata['training_date'])
        self.is_trained = True
        
        # Reinitialize SHAP explainer
        if SHAP_AVAILABLE:
            self._explainer = shap.TreeExplainer(self.model)
        
        print(f"Model v{version} loaded from {path}")
    
    def get_high_risk_drivers(self, 
                               predictions: List[PredictionResult],
                               top_n: int = 10) -> List[PredictionResult]:
        """Get top N high-risk drivers sorted by risk score"""
        sorted_predictions = sorted(predictions, key=lambda x: x.risk_score, reverse=True)
        return sorted_predictions[:top_n]
    
    def generate_risk_summary(self, predictions: List[PredictionResult]) -> Dict[str, Any]:
        """
        Generate summary statistics from predictions.
        
        Returns:
            Dictionary with risk distribution and key stats
        """
        risk_scores = [p.risk_score for p in predictions]
        categories = [p.risk_category for p in predictions]
        
        return {
            "total_drivers": len(predictions),
            "high_risk_count": categories.count("high"),
            "medium_risk_count": categories.count("medium"),
            "low_risk_count": categories.count("low"),
            "high_risk_pct": round(categories.count("high") / len(predictions) * 100, 1),
            "avg_risk_score": round(np.mean(risk_scores), 1),
            "median_risk_score": round(np.median(risk_scores), 1),
            "max_risk_score": round(max(risk_scores), 1),
            "min_risk_score": round(min(risk_scores), 1),
        }


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    from feature_engineering import FeatureEngineer
    
    # Create sample data
    np.random.seed(42)
    n_records = 2000
    
    sample_data = pd.DataFrame({
        'transporter_id': np.random.choice([f'DRV{str(i).zfill(3)}' for i in range(50)], n_records),
        'delivery_date_time': pd.date_range(end='2024-12-13', periods=n_records, freq='30min'),
        'concession_type': np.random.choice(
            [None, None, None, None, 'neighbor', 'safe_location', 'mailbox'], 
            n_records
        ),
        'contact_made': np.random.choice([True, False], n_records, p=[0.85, 0.15]),
    })
    
    # Feature engineering
    fe = FeatureEngineer()
    features = fe.transform(sample_data)
    
    # Create synthetic labels (high-risk if concession_rate_30d > 5%)
    labels = (features['concession_rate_30d'] > 0.05).astype(int)
    
    # Train model
    model = DriverRiskModel()
    metrics = model.train(features, labels)
    
    print("=" * 50)
    print("Driver Risk Model - Training Results")
    print("=" * 50)
    print(f"Accuracy:  {metrics.accuracy:.3f}")
    print(f"Precision: {metrics.precision:.3f}")
    print(f"Recall:    {metrics.recall:.3f}")
    print(f"F1 Score:  {metrics.f1:.3f}")
    print(f"ROC AUC:   {metrics.roc_auc:.3f}")
    print(f"CV Mean:   {np.mean(metrics.cross_val_scores):.3f} (+/- {np.std(metrics.cross_val_scores):.3f})")
    print("\nTop 10 Features:")
    print(model.get_feature_importance().head(10))
    
    # Test predictions
    predictions = model.predict(features.head(10))
    print("\nSample Predictions:")
    for p in predictions[:3]:
        print(f"  {p.transporter_id}: Score={p.risk_score}, Category={p.risk_category}")
        if p.top_factors:
            print(f"    Top Factor: {p.top_factors[0]['feature']} ({p.top_factors[0]['direction']})")
