"""
Pattern Analysis Tab Component
Streamlit UI for displaying pattern recognition results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

import sys
sys.path.append('..')
from ml_engine.pattern_recognition import PatternAnalyzer, Pattern, AnomalyResult, TrendAnalysis
from ml_engine.feature_engineering import FeatureEngineer


def render_pattern_analysis(df: pd.DataFrame,
                            features_df: Optional[pd.DataFrame] = None):
    """
    Render the pattern analysis tab.
    
    Args:
        df: Raw delivery data
        features_df: Pre-computed features (optional)
    """
    st.header("🔬 Advanced Pattern Recognition")
    st.markdown("*AI-powered detection of patterns, trends, and anomalies*")
    
    # Initialize analyzers
    pa = PatternAnalyzer()
    
    if features_df is None:
        with st.spinner("Computing features..."):
            fe = FeatureEngineer()
            features_df = fe.transform(df)
    
    # Tab layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Time Patterns",
        "📈 Trend Analysis",
        "🚨 Anomalies",
        "👥 Driver Clusters",
        "🔗 Correlations"
    ])
    
    with tab1:
        render_time_patterns(df, pa)
    
    with tab2:
        render_trend_analysis(df, pa, features_df)
    
    with tab3:
        render_anomalies(df, pa)
    
    with tab4:
        render_clustering(features_df, pa)
    
    with tab5:
        render_correlations(features_df, pa)


def render_time_patterns(df: pd.DataFrame, pa: PatternAnalyzer):
    """Render time-based pattern analysis"""
    st.subheader("Time-Based Patterns")
    
    # Driver selector
    col1, col2 = st.columns([1, 2])
    
    with col1:
        analysis_scope = st.radio(
            "Analysis Scope",
            ["Organization-wide", "Single Driver"]
        )
    
    transporter_id = None
    if analysis_scope == "Single Driver":
        with col2:
            drivers = df['transporter_id'].unique().tolist()
            transporter_id = st.selectbox("Select Driver", drivers)
    
    # Get patterns
    with st.spinner("Analyzing time patterns..."):
        patterns = pa.detect_time_patterns(df, transporter_id)
    
    if not patterns:
        st.info("No significant time patterns detected in the data.")
    else:
        st.success(f"Found {len(patterns)} time-based patterns")
        
        for p in patterns:
            severity_color = {
                "critical": "🔴",
                "warning": "🟡",
                "info": "🔵"
            }
            
            with st.expander(f"{severity_color.get(p.severity, '⚪')} {p.description}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Pattern Type:** {p.pattern_type}")
                    st.markdown(f"**Confidence:** {p.confidence*100:.0f}%")
                    st.markdown(f"**Affected:** {p.affected_entity}")
                    
                    if p.recommendations:
                        st.markdown("**Recommendations:**")
                        for rec in p.recommendations:
                            st.markdown(f"• {rec}")
                
                with col2:
                    # Visualize pattern details
                    if p.pattern_type == "weekday_concentration":
                        rates = p.details.get("all_weekday_rates", {})
                        if rates:
                            fig = px.bar(
                                x=list(rates.keys()),
                                y=list(rates.values()),
                                labels={'x': 'Weekday', 'y': 'Concession Rate'},
                                color=list(rates.values()),
                                color_continuous_scale='Reds'
                            )
                            fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    elif p.pattern_type == "peak_hours":
                        rates = p.details.get("all_hour_rates", {})
                        if rates:
                            fig = px.line(
                                x=list(rates.keys()),
                                y=list(rates.values()),
                                labels={'x': 'Hour', 'y': 'Rate'},
                                markers=True
                            )
                            fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
                            st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap visualization
    st.markdown("---")
    st.subheader("📊 Time Heatmap")
    
    render_time_heatmap(df, transporter_id)


def render_time_heatmap(df: pd.DataFrame, transporter_id: Optional[str] = None):
    """Render heatmap of concessions by hour and weekday"""
    df = df.copy()
    
    if transporter_id:
        df = df[df['transporter_id'] == transporter_id]
    
    # Check for required columns
    if 'delivery_date_time' not in df.columns:
        st.info("Keine Zeitdaten für Heatmap verfügbar")
        return
    
    df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
    df['hour'] = df['delivery_date_time'].dt.hour
    df['dayofweek'] = df['delivery_date_time'].dt.dayofweek
    
    # Handle missing concession_type column
    if 'concession_type' in df.columns:
        df['is_concession'] = df['concession_type'].notna() & (df['concession_type'] != '')
    else:
        st.info("Keine Konzessionstyp-Spalte vorhanden. Zeige Zustellvolumen.")
        # Show delivery volume instead
        heatmap_data = df.groupby(['dayofweek', 'hour']).size().reset_index(name='count')
        pivot = heatmap_data.pivot(index='dayofweek', columns='hour', values='count').fillna(0)
        weekday_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        
        fig = px.imshow(
            pivot.values,
            labels=dict(x="Stunde", y="Wochentag", color="Zustellungen"),
            x=[f"{h}:00" for h in pivot.columns],
            y=[weekday_names[i] for i in pivot.index],
            color_continuous_scale='Blues',
            aspect='auto'
        )
        fig.update_layout(title="Zustellvolumen nach Zeit", height=300)
        st.plotly_chart(fig, use_container_width=True)
        return
    
    # Calculate rates
    heatmap_data = df.groupby(['dayofweek', 'hour']).agg({
        'is_concession': ['sum', 'count']
    }).reset_index()
    heatmap_data.columns = ['dayofweek', 'hour', 'concessions', 'total']
    heatmap_data['rate'] = heatmap_data['concessions'] / heatmap_data['total']
    
    # Pivot for heatmap
    pivot = heatmap_data.pivot(index='dayofweek', columns='hour', values='rate')
    
    weekday_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    
    fig = px.imshow(
        pivot.values,
        labels=dict(x="Stunde", y="Wochentag", color="Konzessionsrate"),
        x=[f"{h}:00" for h in pivot.columns],
        y=[weekday_names[i] for i in pivot.index],
        color_continuous_scale='RdYlGn_r',
        aspect='auto'
    )
    
    fig.update_layout(
        title="Konzessionsrate nach Zeit (Rot = Hoch, Grün = Niedrig)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_trend_analysis(df: pd.DataFrame, 
                          pa: PatternAnalyzer,
                          features_df: pd.DataFrame):
    """Render trend analysis section"""
    st.subheader("Trend Analysis")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scope = st.radio("Scope", ["Organization", "Driver"], horizontal=True)
    
    transporter_id = None
    if scope == "Driver":
        with col2:
            drivers = df['transporter_id'].unique().tolist()
            transporter_id = st.selectbox("Select Driver", drivers, key="trend_driver")
    
    with col3:
        window = st.selectbox("Analysis Window", [30, 60, 90], index=0)
    
    # Get trend
    trend = pa.analyze_trend(df, transporter_id, window_days=window)
    
    # Display trend metrics
    col1, col2, col3, col4 = st.columns(4)
    
    direction_icon = "📈" if trend.direction == "increasing" else "📉" if trend.direction == "decreasing" else "➡️"
    
    col1.metric("Direction", f"{direction_icon} {trend.direction.title()}")
    col2.metric("Significant", "✅ Yes" if trend.is_significant else "❌ No")
    col3.metric("7-Day Forecast", f"{trend.forecast_7d*100:.2f}%")
    col4.metric("30-Day Forecast", f"{trend.forecast_30d*100:.2f}%")
    
    # Trend visualization
    render_trend_chart(df, transporter_id, window)
    
    # Multi-driver comparison
    if scope == "Organization":
        st.markdown("---")
        st.subheader("📊 Driver Trend Comparison")
        render_driver_trend_comparison(df, pa, features_df)


def render_trend_chart(df: pd.DataFrame, 
                       transporter_id: Optional[str], 
                       window_days: int):
    """Render trend line chart with forecast"""
    df = df.copy()
    
    if transporter_id:
        df = df[df['transporter_id'] == transporter_id]
    
    df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
    df['date'] = df['delivery_date_time'].dt.date
    
    # Handle missing concession_type
    if 'concession_type' in df.columns:
        df['is_concession'] = df['concession_type'].notna() & (df['concession_type'] != '')
    else:
        st.info("Keine Konzessionstyp-Spalte vorhanden")
        return
    
    # Calculate daily rates
    daily = df.groupby('date').agg({
        'is_concession': ['sum', 'count']
    }).reset_index()
    daily.columns = ['date', 'concessions', 'total']
    daily['rate'] = daily['concessions'] / daily['total']
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.sort_values('date')
    
    # Get recent window
    cutoff = daily['date'].max() - timedelta(days=window_days)
    daily = daily[daily['date'] >= cutoff]
    
    # Add rolling average
    daily['rolling_7d'] = daily['rate'].rolling(7, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Daily rate
    fig.add_trace(go.Scatter(
        x=daily['date'],
        y=daily['rate']*100,
        name='Daily Rate',
        mode='markers',
        marker=dict(size=5, opacity=0.5)
    ))
    
    # Rolling average
    fig.add_trace(go.Scatter(
        x=daily['date'],
        y=daily['rolling_7d']*100,
        name='7-Day Avg',
        mode='lines',
        line=dict(width=3, color='blue')
    ))
    
    fig.update_layout(
        title=f"Concession Rate Trend (Last {window_days} Days)",
        xaxis_title="Date",
        yaxis_title="Concession Rate (%)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_driver_trend_comparison(df: pd.DataFrame, 
                                   pa: PatternAnalyzer,
                                   features_df: pd.DataFrame):
    """Compare trends across drivers"""
    
    # Get trends for all drivers
    trends_data = []
    
    for transporter_id in df['transporter_id'].unique():
        trend = pa.analyze_trend(df, transporter_id, window_days=30)
        
        rate_30d = features_df.loc[transporter_id, 'concession_rate_30d'] if transporter_id in features_df.index else 0
        
        trends_data.append({
            'transporter_id': transporter_id,
            'direction': trend.direction,
            'slope': trend.slope * 100,  # Convert to percentage points per day
            'significant': trend.is_significant,
            'current_rate': rate_30d * 100,
            'forecast_7d': trend.forecast_7d * 100
        })
    
    trends_df = pd.DataFrame(trends_data)
    
    # Sort by slope (worst trends first)
    trends_df = trends_df.sort_values('slope', ascending=False)
    
    # Plot
    fig = px.scatter(
        trends_df,
        x='current_rate',
        y='slope',
        color='direction',
        size=abs(trends_df['slope']) + 0.1,
        hover_data=['transporter_id', 'forecast_7d'],
        color_discrete_map={
            'increasing': 'red',
            'decreasing': 'green',
            'stable': 'gray',
            'insufficient_data': 'lightgray'
        },
        title="Driver Trends: Current Rate vs Trend Slope"
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        xaxis_title="Current 30-Day Rate (%)",
        yaxis_title="Daily Rate Change (%)",
        legend_title="Trend Direction"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Table of concerning trends
    concerning = trends_df[
        (trends_df['direction'] == 'increasing') & 
        (trends_df['significant'] == True)
    ].head(10)
    
    if len(concerning) > 0:
        st.warning(f"⚠️ {len(concerning)} drivers showing significant upward trends:")
        st.dataframe(concerning[['transporter_id', 'current_rate', 'slope', 'forecast_7d']], 
                     use_container_width=True, hide_index=True)


def render_anomalies(df: pd.DataFrame, pa: PatternAnalyzer):
    """Render anomaly detection results"""
    st.subheader("🚨 Anomaly Detection")
    st.markdown("*Unusual driver behavior that deviates from normal patterns*")
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        threshold = st.slider("Sensitivity (lower = more sensitive)", 1.5, 4.0, 2.5, 0.5)
    with col2:
        top_n = st.slider("Show Top N", 5, 30, 15)
    
    # Detect anomalies
    with st.spinner("Detecting anomalies..."):
        anomalies = pa.detect_anomalies(df, threshold_std=threshold)
    
    if not anomalies:
        st.success("✅ No significant anomalies detected!")
        return
    
    st.error(f"Found {len(anomalies)} anomalies (showing top {min(top_n, len(anomalies))})")
    
    # Display anomalies
    anomalies_top = anomalies[:top_n]
    
    # Timeline chart
    fig = go.Figure()
    
    for a in anomalies_top:
        color = 'red' if a.anomaly_type == 'spike' else 'blue'
        
        fig.add_trace(go.Scatter(
            x=[a.anomaly_date],
            y=[a.deviation_score],
            mode='markers+text',
            text=[a.transporter_id],
            textposition='top center',
            marker=dict(size=a.deviation_score * 5, color=color),
            name=a.transporter_id,
            showlegend=False
        ))
    
    fig.update_layout(
        title="Anomaly Timeline",
        xaxis_title="Date",
        yaxis_title="Deviation Score",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Table
    anomaly_table = pd.DataFrame([{
        'Driver': a.transporter_id,
        'Date': a.anomaly_date.strftime('%Y-%m-%d'),
        'Type': '📈 Spike' if a.anomaly_type == 'spike' else '📉 Drop',
        'Actual': f"{a.actual_value*100:.1f}%",
        'Expected': f"{a.expected_range[0]*100:.1f}% - {a.expected_range[1]*100:.1f}%",
        'Deviation': f"{a.deviation_score:.1f}σ",
        'Description': a.description
    } for a in anomalies_top])
    
    st.dataframe(anomaly_table, use_container_width=True, hide_index=True)


def render_clustering(features_df: pd.DataFrame, pa: PatternAnalyzer):
    """Render driver clustering analysis"""
    st.subheader("👥 Driver Behavior Clusters")
    st.markdown("*Grouping drivers by similar behavior patterns*")
    
    # Run clustering
    with st.spinner("Clustering drivers..."):
        clusters = pa.cluster_drivers(features_df)
    
    if "error" in clusters:
        st.error(clusters["error"])
        return
    
    # Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Clusters Found", clusters['n_clusters'])
    col2.metric("Drivers Analyzed", len(features_df))
    col3.metric("Outliers", clusters['n_outliers'])
    
    # Cluster profiles
    st.markdown("### Cluster Profiles")
    
    for cluster_id, profile in clusters.get("cluster_profiles", {}).items():
        label = profile.get("label", f"Cluster {cluster_id}")
        size = profile.get("size", 0)
        avg_rate = profile.get("avg_concession_rate", 0)
        
        color = "🟢" if "High Performers" in label else "🟡" if "Average" in label else "🔴"
        
        with st.expander(f"{color} {label} ({size} drivers)", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("Drivers", size)
                st.metric("Avg Concession Rate", f"{avg_rate*100:.2f}%")
            
            with col2:
                # Show driver list
                drivers = profile.get("drivers", [])[:10]
                st.markdown("**Sample Drivers:**")
                st.write(", ".join(drivers) + ("..." if len(profile.get("drivers", [])) > 10 else ""))
    
    # Visualize clusters
    if 'concession_rate_30d' in features_df.columns and 'contact_success_rate' in features_df.columns:
        st.markdown("### Cluster Visualization")
        
        plot_df = features_df[['concession_rate_30d', 'contact_success_rate']].copy()
        plot_df['cluster'] = [clusters['assignments'].get(idx, -1) for idx in plot_df.index]
        plot_df['transporter_id'] = plot_df.index
        
        fig = px.scatter(
            plot_df,
            x='concession_rate_30d',
            y='contact_success_rate',
            color='cluster',
            hover_data=['transporter_id'],
            title="Driver Clusters (2D Projection)",
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            xaxis_title="Concession Rate (30d)",
            yaxis_title="Contact Success Rate"
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_correlations(features_df: pd.DataFrame, pa: PatternAnalyzer):
    """Render correlation analysis"""
    st.subheader("🔗 Feature Correlations")
    st.markdown("*Understanding relationships between metrics*")
    
    # Get correlations with concession rate
    correlations = pa.find_correlations(features_df, min_correlation=0.3)
    
    if correlations:
        st.success(f"Found {len(correlations)} significant correlations")
        
        for c in correlations:
            corr = c.details.get('correlation', 0)
            direction = c.details.get('direction', '')
            feature = c.details.get('feature', '')
            
            icon = "📈" if corr > 0 else "📉"
            color = "#C62828" if corr > 0 else "#2E7D32"
            
            with st.expander(f"{icon} {feature}: r = {corr:.3f}"):
                st.markdown(f"**{c.description}**")
                
                if c.recommendations:
                    st.markdown("**Actionable Insights:**")
                    for rec in c.recommendations:
                        st.markdown(f"• {rec}")
    
    # Full correlation heatmap
    st.markdown("### Correlation Matrix")
    
    # Select key features
    key_features = [
        'concession_rate_30d', 'concession_rate_7d',
        'contact_success_rate', 'volatility_index',
        'rate_trend_7d', 'morning_peak_ratio', 'evening_peak_ratio',
        'avg_daily_deliveries', 'weekend_ratio'
    ]
    
    available = [f for f in key_features if f in features_df.columns]
    
    if len(available) >= 4:
        corr_matrix = features_df[available].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            aspect='auto'
        )
        
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📖 How to read this"):
            st.markdown("""
            - **Red**: Positive correlation (when one increases, the other tends to increase)
            - **Blue**: Negative correlation (when one increases, the other tends to decrease)
            - **White**: No correlation
            
            **Key insights to look for:**
            - What factors correlate with concession_rate?
            - Are there unexpected relationships?
            - Can we use one metric to predict another?
            """)
    else:
        st.info("Not enough features available for correlation matrix")


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    print("Pattern Analysis Tab component ready for Streamlit integration")
    print("Use: render_pattern_analysis(df) in your Streamlit app")
