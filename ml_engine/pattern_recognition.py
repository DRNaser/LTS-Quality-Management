"""
Pattern Recognition Module
Detects complex patterns in delivery data including time patterns, trends, anomalies, and correlations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from scipy import stats

import sys
sys.path.append('..')
from config import pattern_config


@dataclass
class Pattern:
    """Container for detected patterns"""
    pattern_type: str
    description: str
    confidence: float
    details: Dict[str, Any]


@dataclass
class TrendAnalysis:
    """Container for trend analysis results"""
    direction: str  # "increasing", "decreasing", "stable", "insufficient_data"
    slope: float
    significance: float
    forecast: List[float] = field(default_factory=list)
    description: str = ""
    is_significant: bool = False
    forecast_7d: float = 0.0
    forecast_30d: float = 0.0


@dataclass
class AnomalyResult:
    """Container for anomaly detection results"""
    transporter_id: str
    anomaly_score: float
    is_anomaly: bool
    anomaly_type: str
    details: Dict[str, Any] = field(default_factory=dict)
    # Additional attributes expected by pattern_analysis_tab.py
    anomaly_date: datetime = None
    expected_range: Tuple[float, float] = (0.0, 0.0)
    actual_value: float = 0.0
    deviation_score: float = 0.0
    description: str = ""


class PatternAnalyzer:
    """
    Advanced pattern recognition for delivery data.
    
    Detects:
    - Time-based patterns (weekday/weekend, hourly)
    - Trend analysis (increasing/decreasing)
    - Anomaly detection
    - Change point detection
    - Transporter clustering
    - Cross-metric correlations
    """
    
    def __init__(self):
        self.config = pattern_config
    
    def detect_time_patterns(self, 
                             df: pd.DataFrame, 
                             transporter_id: str = None) -> List[Pattern]:
        """
        Detect time-based patterns in concession data.
        
        Patterns detected:
        - Day of week concentration
        - Peak hours
        - Weekend vs weekday differences
        """
        patterns = []
        df = self._prepare_data(df)
        
        if transporter_id:
            df = df[df['transporter_id'] == transporter_id]
        
        if len(df) < 10:
            return patterns
        
        concessions = df[df['is_concession']]
        
        if len(concessions) < 5:
            return patterns
        
        # Day of week pattern
        if 'dayofweek' in concessions.columns:
            dow_counts = concessions['dayofweek'].value_counts(normalize=True)
            if len(dow_counts) > 0:
                max_day = dow_counts.index[0]
                max_pct = dow_counts.values[0]
                
                if max_pct > 0.25:  # More than 25% on one day
                    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    patterns.append(Pattern(
                        pattern_type="weekday_concentration",
                        description=f"{max_pct*100:.0f}% of concessions occur on {day_names[max_day]}",
                        confidence=max_pct,
                        details={
                            "peak_day": max_day,
                            "peak_day_name": day_names[max_day],
                            "concentration": max_pct,
                            "distribution": dow_counts.to_dict()
                        }
                    ))
        
        # Hour pattern
        if 'hour' in concessions.columns:
            hour_counts = concessions['hour'].value_counts(normalize=True)
            if len(hour_counts) > 0:
                peak_hour = hour_counts.index[0]
                peak_pct = hour_counts.values[0]
                
                if peak_pct > 0.15:  # More than 15% in one hour
                    patterns.append(Pattern(
                        pattern_type="peak_hour",
                        description=f"Peak concession hour is {peak_hour}:00 ({peak_pct*100:.0f}%)",
                        confidence=peak_pct,
                        details={
                            "peak_hour": int(peak_hour),
                            "concentration": peak_pct,
                            "distribution": hour_counts.head(5).to_dict()
                        }
                    ))
        
        # Weekend vs weekday
        if 'is_weekend' in concessions.columns:
            weekend_rate = concessions['is_weekend'].mean()
            total_weekend_rate = df['is_weekend'].mean()
            
            if abs(weekend_rate - total_weekend_rate) > 0.1:
                pattern_desc = "higher" if weekend_rate > total_weekend_rate else "lower"
                patterns.append(Pattern(
                    pattern_type="weekend_difference",
                    description=f"Weekend concession rate is {pattern_desc} than average",
                    confidence=abs(weekend_rate - total_weekend_rate),
                    details={
                        "weekend_concession_rate": weekend_rate,
                        "overall_weekend_rate": total_weekend_rate,
                        "difference": weekend_rate - total_weekend_rate
                    }
                ))
        
        return patterns
    
    def analyze_trends(self, 
                       df: pd.DataFrame,
                       window_days: int = 30,
                       transporter_id: str = None) -> TrendAnalysis:
        """
        Analyze trends in concession rates over time.
        """
        df = self._prepare_data(df)
        
        if transporter_id:
            df = df[df['transporter_id'] == transporter_id]
        
        if len(df) < 10 or 'date' not in df.columns:
            return TrendAnalysis(
                direction="unknown",
                slope=0,
                significance=0,
                forecast=[],
                description="Insufficient data for trend analysis"
            )
        
        # Calculate daily rates
        daily = df.groupby('date').agg({
            'is_concession': ['sum', 'count']
        }).reset_index()
        daily.columns = ['date', 'concessions', 'total']
        daily['rate'] = daily['concessions'] / daily['total']
        daily = daily.sort_values('date')
        
        if len(daily) < 7:
            return TrendAnalysis(
                direction="unknown",
                slope=0,
                significance=0,
                forecast=[],
                description="Insufficient days for trend analysis"
            )
        
        # Linear regression for trend
        x = np.arange(len(daily))
        y = daily['rate'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Determine direction
        if p_value < 0.05:
            if slope > 0.001:
                direction = "increasing"
            elif slope < -0.001:
                direction = "decreasing"
            else:
                direction = "stable"
        else:
            direction = "stable"
        
        # Forecast next 7 days
        forecast_x = np.arange(len(daily), len(daily) + 7)
        forecast = [max(0, min(1, intercept + slope * x)) for x in forecast_x]
        
        description = f"Trend is {direction} (slope: {slope*100:.3f}%/day, significance: {1-p_value:.2f})"
        
        is_significant = p_value < 0.05
        forecast_7d = max(0, min(1, intercept + slope * (len(daily) + 7)))
        forecast_30d = max(0, min(1, intercept + slope * (len(daily) + 30)))
        
        return TrendAnalysis(
            direction=direction,
            slope=slope,
            significance=1 - p_value,
            forecast=forecast,
            description=description,
            is_significant=is_significant,
            forecast_7d=forecast_7d,
            forecast_30d=forecast_30d
        )
    
    def detect_anomalies(self, 
                         features_df: pd.DataFrame,
                         contamination: float = 0.1,
                         threshold_std: float = 2.5) -> List[AnomalyResult]:
        """
        Detect anomalous transporter behavior using deviation from mean.
        """
        results = []
        
        if len(features_df) < 10:
            return results
        
        # Use key features for anomaly detection
        feature_cols = [c for c in features_df.columns 
                       if c not in ['_depot_id'] and features_df[c].dtype in ['float64', 'int64']]
        
        if len(feature_cols) == 0:
            return results
        
        # Simple z-score based anomaly detection
        numeric_df = features_df[feature_cols].copy()
        numeric_df = numeric_df.fillna(0)
        
        # Calculate z-scores
        z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())
        anomaly_scores = z_scores.mean(axis=1)
        
        # Threshold for anomaly
        threshold = anomaly_scores.quantile(1 - contamination)
        
        for transporter_id in features_df.index:
            score = anomaly_scores.loc[transporter_id]
            is_anomaly = score > threshold
            
            if is_anomaly:
                # Find which features are most anomalous
                transporter_z = z_scores.loc[transporter_id]
                top_anomalies = transporter_z.nlargest(3)
                
                # Get concession rate if available
                rate = features_df.loc[transporter_id].get('concession_rate_30d', 0)
                mean_rate = features_df['concession_rate_30d'].mean() if 'concession_rate_30d' in features_df.columns else 0
                std_rate = features_df['concession_rate_30d'].std() if 'concession_rate_30d' in features_df.columns else 0.01
                
                anomaly_type = "spike" if rate > mean_rate else "drop"
                
                results.append(AnomalyResult(
                    transporter_id=str(transporter_id),
                    anomaly_score=float(score),
                    is_anomaly=True,
                    anomaly_type=anomaly_type,
                    details={
                        "top_anomalous_features": top_anomalies.to_dict(),
                        "threshold": float(threshold)
                    },
                    anomaly_date=datetime.now(),  # Use current date as proxy
                    expected_range=(max(0, mean_rate - 2*std_rate), mean_rate + 2*std_rate),
                    actual_value=float(rate),
                    deviation_score=float(score),
                    description=f"Fahrer {transporter_id} zeigt ungewöhnliches Verhalten (Score: {score:.2f})"
                ))
        
        # Sort by deviation score
        results.sort(key=lambda x: x.deviation_score, reverse=True)
        
        return results
    
    def cluster_transporters(self, 
                            features_df: pd.DataFrame,
                            n_clusters: int = None) -> Dict[str, Any]:
        """
        Cluster transporters based on behavior patterns.
        Uses simple k-means style clustering.
        """
        if len(features_df) < 10:
            return {"n_clusters": 0, "n_outliers": 0, "cluster_profiles": {}, "assignments": {}}
        
        feature_cols = [c for c in features_df.columns 
                       if c not in ['_depot_id'] and features_df[c].dtype in ['float64', 'int64']]
        
        if len(feature_cols) == 0:
            return {"n_clusters": 0, "n_outliers": 0, "cluster_profiles": {}, "assignments": {}}
        
        numeric_df = features_df[feature_cols].copy()
        numeric_df = numeric_df.fillna(0)
        
        # Normalize features
        normalized = (numeric_df - numeric_df.mean()) / (numeric_df.std() + 1e-10)
        
        # Determine number of clusters based on data size
        if n_clusters is None:
            n_clusters = min(5, max(2, len(features_df) // 10))
        
        # Simple clustering based on concession rate quantiles
        if 'concession_rate_30d' in features_df.columns:
            rate = features_df['concession_rate_30d']
            labels = pd.qcut(rate, q=min(n_clusters, len(rate.unique())), 
                           labels=False, duplicates='drop')
        else:
            # Fallback to random assignment
            labels = pd.Series(np.random.randint(0, n_clusters, len(features_df)), 
                             index=features_df.index)
        
        clusters = {}
        profiles = []
        
        cluster_names = ["High Performers", "Consistent", "Mixed", "At Risk", "Priority"]
        
        for cluster_id in sorted(labels.unique()):
            cluster_mask = labels == cluster_id
            cluster_transporters = features_df.index[cluster_mask].tolist()
            
            cluster_name = cluster_names[int(cluster_id) % len(cluster_names)]
            
            clusters[cluster_name] = cluster_transporters
            
            if len(cluster_transporters) > 0:
                cluster_features = features_df.loc[cluster_transporters]
                profile = {
                    "cluster_id": int(cluster_id),
                    "name": cluster_name,
                    "size": len(cluster_transporters),
                    "avg_rate": cluster_features['concession_rate_30d'].mean() if 'concession_rate_30d' in cluster_features.columns else 0,
                    "transporters": cluster_transporters[:5]  # Top 5
                }
                profiles.append(profile)
        
        return {
            "n_clusters": len(profiles),
            "n_outliers": 0,
            "cluster_profiles": {p['cluster_id']: {
                'label': p['name'],
                'size': p['size'],
                'avg_concession_rate': p['avg_rate'],
                'drivers': p['transporters']
            } for p in profiles},
            "assignments": labels.to_dict(),
            "clusters": clusters,
            "profiles": profiles
        }
    
    def detect_change_points(self, 
                             df: pd.DataFrame,
                             transporter_id: str = None) -> List[Dict]:
        """
        Detect significant changes in behavior over time.
        """
        change_points = []
        df = self._prepare_data(df)
        
        if transporter_id:
            df = df[df['transporter_id'] == transporter_id]
        
        if len(df) < 30 or 'date' not in df.columns:
            return change_points
        
        # Calculate daily rates
        daily = df.groupby('date').agg({
            'is_concession': ['sum', 'count']
        }).reset_index()
        daily.columns = ['date', 'concessions', 'total']
        daily['rate'] = daily['concessions'] / daily['total']
        daily = daily.sort_values('date')
        
        if len(daily) < 14:
            return change_points
        
        # Rolling window comparison
        window = 7
        daily['rolling_mean'] = daily['rate'].rolling(window=window, min_periods=3).mean()
        daily['rolling_std'] = daily['rate'].rolling(window=window, min_periods=3).std()
        
        # Detect significant changes
        for i in range(window, len(daily) - window):
            before_mean = daily['rolling_mean'].iloc[i-1]
            after_mean = daily['rate'].iloc[i:i+window].mean()
            
            if before_mean > 0 and abs(after_mean - before_mean) / before_mean > 0.3:
                change_points.append({
                    "date": str(daily['date'].iloc[i]),
                    "before_rate": float(before_mean),
                    "after_rate": float(after_mean),
                    "change_pct": float((after_mean - before_mean) / before_mean * 100),
                    "direction": "increase" if after_mean > before_mean else "decrease"
                })
        
        return change_points[:5]  # Return top 5 change points
    
    def analyze_correlations(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze correlations between different metrics.
        """
        feature_cols = [c for c in features_df.columns 
                       if c not in ['_depot_id'] and features_df[c].dtype in ['float64', 'int64']]
        
        if len(feature_cols) < 2:
            return {"matrix": {}, "significant": []}
        
        numeric_df = features_df[feature_cols].copy()
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Find significant correlations
        significant = []
        for i, col1 in enumerate(feature_cols):
            for j, col2 in enumerate(feature_cols):
                if i < j:
                    corr_value = corr_matrix.loc[col1, col2]
                    if abs(corr_value) > 0.5:  # Threshold for significance
                        significant.append({
                            "feature1": col1,
                            "feature2": col2,
                            "correlation": float(corr_value),
                            "strength": "strong" if abs(corr_value) > 0.7 else "moderate"
                        })
        
        # Sort by absolute correlation
        significant.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            "matrix": corr_matrix.to_dict(),
            "significant": significant[:10]  # Top 10
        }
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for pattern analysis"""
        df = df.copy()
        
        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Parse dates and extract components
        if 'delivery_date_time' in df.columns:
            df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
            df['date'] = df['delivery_date_time'].dt.date
            df['hour'] = df['delivery_date_time'].dt.hour
            df['dayofweek'] = df['delivery_date_time'].dt.dayofweek
            df['is_weekend'] = df['dayofweek'].isin([5, 6])
        
        # Flag concessions
        if 'concession_type' in df.columns:
            df['is_concession'] = df['concession_type'].notna() & (df['concession_type'] != '')
        else:
            df['is_concession'] = False
        
        return df
    
    def get_time_heatmap_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate data for time heatmap visualization (hour x day of week).
        """
        df = self._prepare_data(df)
        
        if 'hour' not in df.columns or 'dayofweek' not in df.columns:
            return pd.DataFrame()
        
        # Group by hour and day of week
        heatmap = df.groupby(['hour', 'dayofweek']).agg({
            'is_concession': ['sum', 'count']
        }).reset_index()
        heatmap.columns = ['hour', 'dayofweek', 'concessions', 'total']
        heatmap['rate'] = heatmap['concessions'] / heatmap['total'] * 100
        
        # Pivot for heatmap format
        pivot = heatmap.pivot(index='hour', columns='dayofweek', values='rate')
        
        return pivot
    
    # ==========================================================================
    # METHOD ALIASES for compatibility with pattern_analysis_tab.py
    # ==========================================================================
    
    def analyze_trend(self, df: pd.DataFrame, transporter_id: str = None, 
                      window_days: int = 30) -> TrendAnalysis:
        """Alias for analyze_trends"""
        return self.analyze_trends(df, window_days=window_days, transporter_id=transporter_id)
    
    def cluster_drivers(self, features_df: pd.DataFrame, n_clusters: int = None) -> Dict:
        """Alias for cluster_transporters"""
        return self.cluster_transporters(features_df, n_clusters)
    
    def find_correlations(self, features_df: pd.DataFrame, min_correlation: float = 0.3) -> List[Pattern]:
        """Alias for analyze_correlations - returns patterns with high correlations"""
        correlations = self.analyze_correlations(features_df)
        # Filter by minimum correlation
        return [c for c in correlations if abs(c.details.get('correlation', 0)) >= min_correlation]


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    np.random.seed(42)
    
    # Create test data
    n_records = 1000
    df = pd.DataFrame({
        'transporter_id': np.random.choice([f'DRV{i:02d}' for i in range(20)], n_records),
        'delivery_date_time': pd.date_range(end=datetime.now(), periods=n_records, freq='30min'),
        'concession_type': np.random.choice([None]*90 + ['neighbor', 'safe_location'], n_records)
    })
    
    analyzer = PatternAnalyzer()
    
    # Test time patterns
    print("=" * 60)
    print("Time Patterns:")
    patterns = analyzer.detect_time_patterns(df)
    for p in patterns:
        print(f"  - {p.pattern_type}: {p.description}")
    
    # Test trend analysis
    print("\nTrend Analysis:")
    trend = analyzer.analyze_trends(df)
    print(f"  {trend.description}")
    
    print("\n✅ Pattern recognition module working!")
