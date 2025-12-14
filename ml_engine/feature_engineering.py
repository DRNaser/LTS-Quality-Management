"""
Feature Engineering Module
Transforms raw delivery data into ML-ready features for driver risk prediction.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append('..')
from config import feature_config, column_config


@dataclass
class DriverFeatures:
    """Container for computed driver features"""
    transporter_id: str
    features: Dict[str, float]
    computed_at: datetime
    data_quality_score: float


class FeatureEngineer:
    """
    Feature Engineering for Driver Risk Prediction
    
    Transforms raw delivery/concession data into ML features across categories:
    - Historical concession rates (multiple time windows)
    - Delivery performance metrics
    - Contact success patterns
    - Time-based patterns
    - Trend indicators
    - Coaching effectiveness
    """
    
    def __init__(self, config=None):
        self.config = config or feature_config
        self.column_config = column_config
        self._feature_names = None
    
    @property
    def feature_names(self) -> List[str]:
        """Get list of all feature names"""
        if self._feature_names is None:
            self._feature_names = self._get_all_feature_names()
        return self._feature_names
    
    def _get_all_feature_names(self) -> List[str]:
        """Generate complete list of feature names"""
        features = []
        
        # Historical rates for each time window
        for window in self.config.time_windows:
            features.extend([
                f"concession_rate_{window}d",
                f"concession_count_{window}d",
                f"delivery_count_{window}d",
            ])
        
        # Performance features
        features.extend([
            "avg_daily_deliveries",
            "delivery_count_variance",
            "active_days_ratio",
        ])
        
        # Contact features
        features.extend([
            "contact_success_rate",
            "no_contact_streak_max",
            "contact_improvement_trend",
        ])
        
        # Time pattern features
        features.extend([
            "morning_peak_ratio",
            "evening_peak_ratio",
            "weekend_ratio",
            "weekday_with_most_concessions",
            "hour_with_most_concessions",
        ])
        
        # Trend features
        features.extend([
            "rate_trend_7d",
            "rate_trend_30d",
            "volatility_index",
            "improving_flag",
        ])
        
        # Concession type features
        for ctype in self.column_config.CONCESSION_TYPES:
            features.append(f"pct_{ctype}")
        
        return features
    
    def transform(self, 
                  df: pd.DataFrame, 
                  reference_date: Optional[datetime] = None,
                  drivers: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Transform raw data into ML features for all/selected drivers.
        
        Args:
            df: Raw delivery data with required columns
            reference_date: Date to compute features as of (default: today)
            drivers: Optional list of driver IDs to process
            
        Returns:
            DataFrame with transporter_id as index and features as columns
        """
        # Validate and prepare data
        df = self._prepare_data(df)
        
        if reference_date is None:
            reference_date = df[self.column_config.DELIVERY_DATE].max()
        
        if drivers is None:
            drivers = df[self.column_config.transporter_id].unique()
        
        # Compute features for each driver
        features_list = []
        for transporter_id in drivers:
            driver_df = df[df[self.column_config.transporter_id] == transporter_id]
            features = self._compute_driver_features(driver_df, reference_date)
            features['transporter_id'] = transporter_id
            features_list.append(features)
        
        result = pd.DataFrame(features_list)
        result.set_index('transporter_id', inplace=True)
        
        # Fill missing values
        result = self._handle_missing_values(result)
        
        return result
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and prepare input data"""
        df = df.copy()
        
        # Check required columns - only transporter_id and date are truly required
        required = [self.column_config.transporter_id, self.column_config.DELIVERY_DATE]
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Parse dates
        df[self.column_config.DELIVERY_DATE] = pd.to_datetime(
            df[self.column_config.DELIVERY_DATE], errors='coerce'
        )
        
        # Add derived columns
        df['date'] = df[self.column_config.DELIVERY_DATE].dt.date
        df['hour'] = df[self.column_config.DELIVERY_DATE].dt.hour
        df['dayofweek'] = df[self.column_config.DELIVERY_DATE].dt.dayofweek
        df['is_weekend'] = df['dayofweek'].isin([5, 6])
        
        # Flag concessions - handle missing concession_type column
        if self.column_config.CONCESSION_TYPE in df.columns:
            df['is_concession'] = df[self.column_config.CONCESSION_TYPE].notna() & \
                                  (df[self.column_config.CONCESSION_TYPE] != '')
        else:
            # No concession type column - assume no concessions (for delivery-only data)
            df['is_concession'] = False
        
        return df
    
    def _compute_driver_features(self, 
                                  driver_df: pd.DataFrame, 
                                  reference_date: datetime) -> Dict[str, float]:
        """Compute all features for a single driver"""
        features = {}
        
        # Historical rate features
        features.update(self._compute_historical_rates(driver_df, reference_date))
        
        # Performance features
        features.update(self._compute_performance_features(driver_df, reference_date))
        
        # Contact features
        features.update(self._compute_contact_features(driver_df, reference_date))
        
        # Time pattern features
        features.update(self._compute_time_patterns(driver_df, reference_date))
        
        # Trend features
        features.update(self._compute_trend_features(driver_df, reference_date))
        
        # Concession type breakdown
        features.update(self._compute_concession_types(driver_df, reference_date))
        
        return features
    
    def _compute_historical_rates(self, 
                                   df: pd.DataFrame, 
                                   ref_date: datetime) -> Dict[str, float]:
        """Compute concession rates over multiple time windows"""
        features = {}
        
        for window in self.config.time_windows:
            start_date = ref_date - timedelta(days=window)
            window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date]
            
            total = len(window_df)
            concessions = window_df['is_concession'].sum()
            
            features[f"concession_rate_{window}d"] = (
                concessions / total if total > 0 else 0
            )
            features[f"concession_count_{window}d"] = concessions
            features[f"delivery_count_{window}d"] = total
        
        return features
    
    def _compute_performance_features(self, 
                                       df: pd.DataFrame, 
                                       ref_date: datetime) -> Dict[str, float]:
        """Compute delivery performance metrics"""
        features = {}
        
        # Use 30-day window for performance
        start_date = ref_date - timedelta(days=30)
        window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date]
        
        if len(window_df) == 0:
            return {
                "avg_daily_deliveries": 0,
                "delivery_count_variance": 0,
                "active_days_ratio": 0,
            }
        
        # Daily delivery counts
        daily_counts = window_df.groupby('date').size()
        
        features["avg_daily_deliveries"] = daily_counts.mean()
        features["delivery_count_variance"] = daily_counts.std() if len(daily_counts) > 1 else 0
        features["active_days_ratio"] = len(daily_counts) / 30
        
        return features
    
    def _compute_contact_features(self, 
                                   df: pd.DataFrame, 
                                   ref_date: datetime) -> Dict[str, float]:
        """Compute contact success patterns"""
        features = {
            "contact_success_rate": 0,
            "no_contact_streak_max": 0,
            "contact_improvement_trend": 0,
        }
        
        # Check if contact column exists
        if self.column_config.CONTACT_MADE not in df.columns:
            return features
        
        start_date = ref_date - timedelta(days=30)
        window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date].copy()
        
        if len(window_df) == 0:
            return features
        
        # Contact success rate
        contacts = window_df[self.column_config.CONTACT_MADE].fillna(False)
        features["contact_success_rate"] = contacts.mean()
        
        # Maximum streak of no contact
        no_contact = (~contacts).astype(int)
        streak = 0
        max_streak = 0
        for val in no_contact:
            if val == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        features["no_contact_streak_max"] = max_streak
        
        # Contact improvement trend (compare first half to second half)
        if len(contacts) >= 10:
            half = len(contacts) // 2
            first_half = contacts.iloc[:half].mean()
            second_half = contacts.iloc[half:].mean()
            features["contact_improvement_trend"] = second_half - first_half
        
        return features
    
    def _compute_time_patterns(self, 
                                df: pd.DataFrame, 
                                ref_date: datetime) -> Dict[str, float]:
        """Compute time-based concession patterns"""
        features = {
            "morning_peak_ratio": 0,
            "evening_peak_ratio": 0,
            "weekend_ratio": 0,
            "weekday_with_most_concessions": 0,
            "hour_with_most_concessions": 12,
        }
        
        start_date = ref_date - timedelta(days=30)
        window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date]
        concessions = window_df[window_df['is_concession']]
        
        if len(concessions) == 0:
            return features
        
        # Peak hour ratios
        morning_start, morning_end = self.config.morning_peak
        evening_start, evening_end = self.config.evening_peak
        
        morning_concessions = concessions[
            (concessions['hour'] >= morning_start) & 
            (concessions['hour'] < morning_end)
        ]
        evening_concessions = concessions[
            (concessions['hour'] >= evening_start) & 
            (concessions['hour'] < evening_end)
        ]
        
        features["morning_peak_ratio"] = len(morning_concessions) / len(concessions)
        features["evening_peak_ratio"] = len(evening_concessions) / len(concessions)
        
        # Weekend ratio
        weekend_concessions = concessions[concessions['is_weekend']]
        features["weekend_ratio"] = len(weekend_concessions) / len(concessions)
        
        # Most common weekday/hour for concessions
        weekday_counts = concessions['dayofweek'].value_counts()
        hour_counts = concessions['hour'].value_counts()
        
        features["weekday_with_most_concessions"] = weekday_counts.idxmax() if len(weekday_counts) > 0 else 0
        features["hour_with_most_concessions"] = hour_counts.idxmax() if len(hour_counts) > 0 else 12
        
        return features
    
    def _compute_trend_features(self, 
                                 df: pd.DataFrame, 
                                 ref_date: datetime) -> Dict[str, float]:
        """Compute trend and volatility indicators"""
        features = {
            "rate_trend_7d": 0,
            "rate_trend_30d": 0,
            "volatility_index": 0,
            "improving_flag": 0,
        }
        
        # Get 60-day window for trend calculation
        start_date = ref_date - timedelta(days=60)
        window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date].copy()
        
        if len(window_df) < 14:  # Need at least 2 weeks of data
            return features
        
        # Calculate daily rates
        daily_stats = window_df.groupby('date').agg({
            'is_concession': ['sum', 'count']
        }).reset_index()
        daily_stats.columns = ['date', 'concessions', 'total']
        daily_stats['rate'] = daily_stats['concessions'] / daily_stats['total']
        daily_stats['date'] = pd.to_datetime(daily_stats['date'])
        daily_stats = daily_stats.sort_values('date')
        
        if len(daily_stats) < 7:
            return features
        
        # 7-day trend (recent week vs previous week)
        recent_7d = daily_stats.tail(7)['rate'].mean()
        previous_7d = daily_stats.iloc[-14:-7]['rate'].mean() if len(daily_stats) >= 14 else recent_7d
        features["rate_trend_7d"] = recent_7d - previous_7d
        
        # 30-day trend (recent 30 vs previous 30)
        if len(daily_stats) >= 30:
            recent_30d = daily_stats.tail(30)['rate'].mean()
            if len(daily_stats) >= 60:
                previous_30d = daily_stats.iloc[-60:-30]['rate'].mean()
            else:
                previous_30d = daily_stats.iloc[:30]['rate'].mean()
            features["rate_trend_30d"] = recent_30d - previous_30d
        
        # Volatility (standard deviation of daily rates)
        features["volatility_index"] = daily_stats['rate'].std()
        
        # Improving flag (1 if rate is decreasing)
        features["improving_flag"] = 1 if features["rate_trend_7d"] < 0 else 0
        
        return features
    
    def _compute_concession_types(self, 
                                   df: pd.DataFrame, 
                                   ref_date: datetime) -> Dict[str, float]:
        """Compute percentage breakdown by concession type"""
        features = {}
        
        # Initialize all types to 0
        for ctype in self.column_config.CONCESSION_TYPES:
            features[f"pct_{ctype}"] = 0
        
        # Check if concession_type column exists
        if self.column_config.CONCESSION_TYPE not in df.columns:
            return features
        
        start_date = ref_date - timedelta(days=30)
        window_df = df[df[self.column_config.DELIVERY_DATE] >= start_date]
        concessions = window_df[window_df['is_concession']]
        
        if len(concessions) == 0:
            return features
        
        # Calculate percentages
        type_counts = concessions[self.column_config.CONCESSION_TYPE].value_counts()
        total = len(concessions)
        
        for ctype in self.column_config.CONCESSION_TYPES:
            if ctype in type_counts.index:
                features[f"pct_{ctype}"] = type_counts[ctype] / total
        
        return features
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in feature matrix"""
        # Fill NaN with 0 for counts and rates
        df = df.fillna(0)
        
        # Replace infinity values
        df = df.replace([np.inf, -np.inf], 0)
        
        return df
    
    def get_feature_importance_groups(self) -> Dict[str, List[str]]:
        """Get features grouped by category for interpretability"""
        return {
            "historical_rates": [f for f in self.feature_names if "rate_" in f or "count_" in f],
            "performance": ["avg_daily_deliveries", "delivery_count_variance", "active_days_ratio"],
            "contact": ["contact_success_rate", "no_contact_streak_max", "contact_improvement_trend"],
            "time_patterns": ["morning_peak_ratio", "evening_peak_ratio", "weekend_ratio", 
                            "weekday_with_most_concessions", "hour_with_most_concessions"],
            "trends": ["rate_trend_7d", "rate_trend_30d", "volatility_index", "improving_flag"],
            "concession_types": [f for f in self.feature_names if f.startswith("pct_")],
        }


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    n_records = 1000
    
    sample_data = pd.DataFrame({
        'transporter_id': np.random.choice(['DRV001', 'DRV002', 'DRV003'], n_records),
        'delivery_date_time': pd.date_range(end='2024-12-13', periods=n_records, freq='30min'),
        'concession_type': np.random.choice(
            [None, None, None, None, 'neighbor', 'safe_location', 'mailbox'], 
            n_records
        ),
        'contact_made': np.random.choice([True, False], n_records, p=[0.85, 0.15]),
    })
    
    # Test feature engineering
    fe = FeatureEngineer()
    features = fe.transform(sample_data)
    
    print("Feature Engineering Test Results:")
    print(f"Generated {len(fe.feature_names)} features for {len(features)} drivers")
    print("\nSample features for first driver:")
    print(features.iloc[0])
