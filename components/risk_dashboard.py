"""
Risk Dashboard Component
Streamlit UI for displaying ML-based driver risk predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional
from datetime import datetime

import sys
sys.path.append('..')
from ml_engine.risk_model import DriverRiskModel, PredictionResult
from ml_engine.feature_engineering import FeatureEngineer


def render_risk_dashboard(df: pd.DataFrame, 
                          model: Optional[DriverRiskModel] = None,
                          features_df: Optional[pd.DataFrame] = None):
    """
    Render the risk analysis dashboard.
    
    Args:
        df: Raw delivery data
        model: Trained DriverRiskModel (optional, will train if None)
        features_df: Pre-computed features (optional)
    """
    st.header("🎯 Driver Risk Analysis")
    st.markdown("*ML-powered risk scoring and prediction*")
    
    # Initialize feature engineering if needed
    if features_df is None:
        with st.spinner("Computing driver features..."):
            fe = FeatureEngineer()
            features_df = fe.transform(df)
    
    # Train or load model if needed
    if model is None or not model.is_trained:
        with st.spinner("Training risk model..."):
            model = train_model_on_data(features_df)
    
    if model is None:
        st.warning("Unable to train model. Insufficient data.")
        return
    
    # Get predictions
    predictions = model.predict(features_df)
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_risk_distribution(predictions)
    
    with col2:
        render_risk_summary(predictions)
    
    st.divider()
    
    # High-risk drivers table
    render_high_risk_drivers(predictions, features_df)
    
    st.divider()
    
    # Feature importance
    render_feature_importance(model)
    
    st.divider()
    
    # Driver deep-dive
    render_driver_deep_dive(predictions, features_df, df)


def train_model_on_data(features_df: pd.DataFrame) -> Optional[DriverRiskModel]:
    """Train model using heuristic labels"""
    if len(features_df) < 10:
        return None
    
    # Remove non-numeric columns (like _depot_id)
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns.tolist()
    features_numeric = features_df[numeric_cols].copy()
    
    if len(features_numeric.columns) < 3:
        return None
    
    # Handle missing columns for labels
    if 'concession_rate_30d' not in features_numeric.columns:
        # Use any rate column available
        rate_cols = [c for c in features_numeric.columns if 'rate' in c.lower()]
        if rate_cols:
            label_col = rate_cols[0]
        else:
            # No rate columns - cannot create meaningful labels
            return None
    else:
        label_col = 'concession_rate_30d'
    
    # Create labels: high-risk if concession_rate > 5% or trending up
    rate_threshold = 0.05
    if 'rate_trend_7d' in features_numeric.columns:
        labels = (
            (features_numeric[label_col] > rate_threshold) | 
            (features_numeric['rate_trend_7d'] > 0.01)
        ).astype(int)
    else:
        labels = (features_numeric[label_col] > rate_threshold).astype(int)
    
    # Ensure we have both classes
    if labels.nunique() < 2:
        # Create synthetic labels if needed
        labels = (features_numeric[label_col] > features_numeric[label_col].median()).astype(int)
    
    if labels.nunique() < 2:
        return None
    
    model = DriverRiskModel()
    model.train(features_numeric, labels)
    
    return model


def render_risk_distribution(predictions: List[PredictionResult]):
    """Render risk score distribution chart"""
    st.subheader("Risk Score Distribution")
    
    scores = [p.risk_score for p in predictions]
    categories = [p.risk_category for p in predictions]
    
    # Create histogram with color by category
    df_plot = pd.DataFrame({
        'Risk Score': scores,
        'Category': categories
    })
    
    color_map = {
        'low': '#2E7D32',      # Green
        'medium': '#F9A825',   # Yellow/Orange
        'high': '#C62828'      # Red
    }
    
    fig = px.histogram(
        df_plot,
        x='Risk Score',
        color='Category',
        nbins=20,
        color_discrete_map=color_map,
        title="Distribution of Driver Risk Scores"
    )
    
    fig.update_layout(
        xaxis_title="Risk Score (0-100)",
        yaxis_title="Number of Drivers",
        legend_title="Risk Level",
        bargap=0.1
    )
    
    # Add threshold lines
    fig.add_vline(x=40, line_dash="dash", line_color="orange", annotation_text="Medium Threshold")
    fig.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="High Threshold")
    
    st.plotly_chart(fig, use_container_width=True)


def render_risk_summary(predictions: List[PredictionResult]):
    """Render risk summary metrics"""
    st.subheader("Summary")
    
    total = len(predictions)
    high = len([p for p in predictions if p.risk_category == "high"])
    medium = len([p for p in predictions if p.risk_category == "medium"])
    low = len([p for p in predictions if p.risk_category == "low"])
    
    avg_score = np.mean([p.risk_score for p in predictions])
    
    # Large metrics
    st.metric("Total Drivers", total)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 High Risk", high, f"{high/total*100:.0f}%")
    col2.metric("🟡 Medium", medium, f"{medium/total*100:.0f}%")
    col3.metric("🟢 Low Risk", low, f"{low/total*100:.0f}%")
    
    st.metric("Average Risk Score", f"{avg_score:.1f}/100")
    
    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Org Risk Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "#C8E6C9"},
                {'range': [40, 70], 'color': "#FFF9C4"},
                {'range': [70, 100], 'color': "#FFCDD2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_high_risk_drivers(predictions: List[PredictionResult], 
                             features_df: pd.DataFrame):
    """Render table of high-risk drivers"""
    st.subheader("🚨 High Risk Drivers - Immediate Attention Required")
    
    # Get high and medium risk drivers
    at_risk = [p for p in predictions if p.risk_category in ["high", "medium"]]
    at_risk.sort(key=lambda x: x.risk_score, reverse=True)
    
    if not at_risk:
        st.success("✅ No high-risk drivers detected!")
        return
    
    # Build table data
    table_data = []
    for p in at_risk[:15]:  # Top 15
        top_factor = p.top_factors[0] if p.top_factors else {"feature": "N/A", "direction": ""}
        
        # Get feature values
        driver_features = features_df.loc[p.transporter_id] if p.transporter_id in features_df.index else {}
        
        table_data.append({
            "Driver ID": p.transporter_id,
            "Risk Score": p.risk_score,
            "Category": p.risk_category.upper(),
            "30d Rate": f"{driver_features.get('concession_rate_30d', 0)*100:.1f}%" if isinstance(driver_features, pd.Series) else "N/A",
            "Trend": "📈" if driver_features.get('rate_trend_7d', 0) > 0 else "📉" if isinstance(driver_features, pd.Series) else "-",
            "Top Factor": top_factor.get("feature", "N/A"),
            "Confidence": f"{p.confidence*100:.0f}%"
        })
    
    df_table = pd.DataFrame(table_data)
    
    # Style the table
    def style_risk(val):
        if val == "HIGH":
            return "background-color: #FFCDD2; color: #C62828; font-weight: bold"
        elif val == "MEDIUM":
            return "background-color: #FFF9C4; color: #F57F17; font-weight: bold"
        return ""
    
    styled = df_table.style.applymap(style_risk, subset=["Category"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df_table.to_csv(index=False)
    st.download_button(
        label="📥 Download Risk Report",
        data=csv,
        file_name=f"risk_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def render_feature_importance(model: DriverRiskModel):
    """Render feature importance chart"""
    st.subheader("📊 Key Risk Factors")
    st.markdown("*Features that most influence risk predictions*")
    
    importance = model.get_feature_importance()
    
    # Take top 15
    top_features = importance.head(15)
    
    fig = px.bar(
        top_features,
        x='importance',
        y='feature',
        orientation='h',
        title="Feature Importance (Top 15)",
        color='importance',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanation
    with st.expander("📖 Understanding Feature Importance"):
        st.markdown("""
        **What this means:**
        - Features at the top have the strongest influence on risk predictions
        - Higher importance = more predictive of high-risk status
        
        **Key feature categories:**
        - `concession_rate_*d`: Historical concession rates over different time windows
        - `rate_trend_*d`: Whether rates are increasing or decreasing
        - `contact_success_rate`: How often customer contact is made
        - `volatility_index`: How consistent the driver's performance is
        - `pct_*`: Breakdown by concession type
        """)


def render_driver_deep_dive(predictions: List[PredictionResult],
                            features_df: pd.DataFrame,
                            raw_df: pd.DataFrame):
    """Render detailed view for a selected driver"""
    st.subheader("🔍 Driver Deep Dive")
    
    # Driver selector
    transporter_ids = [p.transporter_id for p in predictions]
    
    # Sort by risk score for easier selection
    sorted_predictions = sorted(predictions, key=lambda x: x.risk_score, reverse=True)
    
    options = [f"{p.transporter_id} (Risk: {p.risk_score:.0f})" for p in sorted_predictions]
    
    selected = st.selectbox("Select Driver", options)
    
    if not selected:
        return
    
    selected_id = selected.split(" (")[0]
    
    # Find prediction
    pred = next((p for p in predictions if p.transporter_id == selected_id), None)
    if pred is None:
        return
    
    # Display risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    color = "🔴" if pred.risk_category == "high" else "🟡" if pred.risk_category == "medium" else "🟢"
    
    col1.metric("Risk Score", f"{pred.risk_score:.0f}/100")
    col2.metric("Category", f"{color} {pred.risk_category.upper()}")
    col3.metric("Confidence", f"{pred.confidence*100:.0f}%")
    col4.metric("Probability", f"{pred.probability*100:.1f}%")
    
    # Contributing factors
    if pred.top_factors:
        st.markdown("#### Top Contributing Factors")
        
        factors_df = pd.DataFrame(pred.top_factors)
        factors_df['impact'] = factors_df['impact'].round(3)
        factors_df['value'] = factors_df['value'].round(4)
        
        # Color code by direction
        def style_direction(val):
            if "increases" in val:
                return "color: #C62828"
            return "color: #2E7D32"
        
        styled = factors_df.style.applymap(style_direction, subset=["direction"])
        st.dataframe(styled, use_container_width=True, hide_index=True)
    
    # Feature profile
    st.markdown("#### Feature Profile")
    
    if selected_id in features_df.index:
        driver_features = features_df.loc[selected_id]
        
        # Show key metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📊 Concession Rates**")
            st.write(f"• 7-day: {driver_features.get('concession_rate_7d', 0)*100:.2f}%")
            st.write(f"• 30-day: {driver_features.get('concession_rate_30d', 0)*100:.2f}%")
            st.write(f"• 90-day: {driver_features.get('concession_rate_90d', 0)*100:.2f}%")
        
        with col2:
            st.markdown("**📈 Trends**")
            trend_7d = driver_features.get('rate_trend_7d', 0)
            trend_30d = driver_features.get('rate_trend_30d', 0)
            st.write(f"• 7-day trend: {'📈' if trend_7d > 0 else '📉'} {trend_7d*100:.2f}%")
            st.write(f"• 30-day trend: {'📈' if trend_30d > 0 else '📉'} {trend_30d*100:.2f}%")
            st.write(f"• Volatility: {driver_features.get('volatility_index', 0)*100:.2f}")
        
        with col3:
            st.markdown("**⏰ Time Patterns**")
            st.write(f"• Morning peak: {driver_features.get('morning_peak_ratio', 0)*100:.1f}%")
            st.write(f"• Evening peak: {driver_features.get('evening_peak_ratio', 0)*100:.1f}%")
            st.write(f"• Weekend: {driver_features.get('weekend_ratio', 0)*100:.1f}%")


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '..')
    
    # Create sample data for testing
    np.random.seed(42)
    n_records = 1000
    
    sample_data = pd.DataFrame({
        'transporter_id': np.random.choice([f'DRV{str(i).zfill(3)}' for i in range(30)], n_records),
        'delivery_date_time': pd.date_range(end='2024-12-13', periods=n_records, freq='30min'),
        'concession_type': np.random.choice(
            [None]*10 + ['neighbor', 'safe_location', 'mailbox'], 
            n_records
        ),
        'contact_made': np.random.choice([True, False], n_records, p=[0.85, 0.15]),
    })
    
    print("Risk Dashboard component ready for Streamlit integration")
    print("Use: render_risk_dashboard(df) in your Streamlit app")
