"""
LTS Quality Management Platform - Configuration
ML & Pattern Recognition Settings
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import os

# =============================================================================
# ML MODEL CONFIGURATION
# =============================================================================

@dataclass
class MLConfig:
    """Machine Learning Model Configuration"""
    
    # Risk Thresholds
    risk_threshold_high: int = 70      # Score >= 70 = High Risk
    risk_threshold_medium: int = 40    # Score >= 40 = Medium Risk
    
    # Training Settings
    train_test_split: float = 0.2
    cross_validation_folds: int = 5
    random_state: int = 42
    
    # Retraining Schedule
    retrain_frequency_days: int = 7
    min_training_samples: int = 500
    
    # XGBoost Parameters
    xgb_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.xgb_params is None:
            self.xgb_params = {
                "objective": "binary:logistic",
                "n_estimators": 200,
                "max_depth": 6,
                "learning_rate": 0.1,
                "min_child_weight": 3,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "gamma": 0.1,
                "reg_alpha": 0.1,
                "reg_lambda": 1.0,
                "scale_pos_weight": 1,
                "random_state": self.random_state,
                "n_jobs": -1,
                "verbosity": 0
            }


# =============================================================================
# FEATURE ENGINEERING CONFIGURATION
# =============================================================================

@dataclass
class FeatureConfig:
    """Feature Engineering Configuration"""
    
    # Time Windows for Rolling Features
    time_windows: List[int] = None  # days
    
    # Peak Hours Definition
    morning_peak: tuple = (6, 9)
    evening_peak: tuple = (17, 20)
    
    # Thresholds for Pattern Detection
    high_concession_threshold: float = 0.05  # 5%
    contact_success_threshold: float = 0.90  # 90%
    
    def __post_init__(self):
        if self.time_windows is None:
            self.time_windows = [7, 14, 30, 60, 90]


# =============================================================================
# PATTERN RECOGNITION CONFIGURATION
# =============================================================================

@dataclass
class PatternConfig:
    """Pattern Recognition Settings"""
    
    # Anomaly Detection
    anomaly_contamination: float = 0.1  # Expected outlier fraction
    
    # Clustering
    min_cluster_size: int = 5
    
    # Trend Detection
    trend_significance_level: float = 0.05
    min_trend_periods: int = 3
    
    # Seasonality
    detect_weekly_patterns: bool = True
    detect_monthly_patterns: bool = True
    
    # Change Point Detection
    change_point_penalty: int = 3


# =============================================================================
# DATA COLUMN MAPPINGS
# =============================================================================

class ColumnConfig:
    """Column name mappings for data processing"""
    
    # Required columns
    transporter_id = "transporter_id"
    DELIVERY_DATE = "delivery_date_time"
    CONCESSION_TYPE = "concession_type"
    
    # Optional columns (with fallbacks)
    TRACKING_ID = "tracking_id"
    CONTACT_MADE = "contact_made"
    CONCESSION_COST = "concession_cost"
    POSTAL_CODE = "postal_code"
    DELIVERY_DURATION = "delivery_duration"
    DNR_DATE = "dnr_date"
    
    # Concession type values
    CONCESSION_TYPES = [
        "neighbor",
        "safe_location", 
        "mailbox",
        "household_member",
        "receptionist",
        "other"
    ]


# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

@dataclass 
class AppConfig:
    """Application Settings"""
    
    # Display Settings
    page_title: str = "LTS Quality Management Platform"
    page_icon: str = "📊"
    layout: str = "wide"
    
    # Data Settings
    max_upload_size_mb: int = 200
    cache_ttl_seconds: int = 300
    
    # Export Settings
    export_formats: List[str] = None
    
    def __post_init__(self):
        if self.export_formats is None:
            self.export_formats = ["xlsx", "csv", "pdf"]


# =============================================================================
# INSTANTIATE CONFIGS
# =============================================================================

ml_config = MLConfig()
feature_config = FeatureConfig()
pattern_config = PatternConfig()
column_config = ColumnConfig()
app_config = AppConfig()
