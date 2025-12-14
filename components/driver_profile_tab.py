"""
Driver Profiles Tab Component
Renders detailed driver profile views.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Optional


def render_driver_profiles_tab(df: pd.DataFrame, features_df: Optional[pd.DataFrame] = None):
    """
    Render the Driver Profiles tab.
    
    Args:
        df: Delivery data DataFrame
        features_df: Pre-computed driver features
    """
    st.header("👤 Driver Profiles")
    
    # Depot filter
    if '_depot_id' in df.columns:
        col1, col2 = st.columns([1, 2])
        with col1:
            depot_filter = st.selectbox(
                "Filter by Depot",
                options=['All'] + list(df['_depot_id'].unique()),
                key="driver_depot_filter"
            )
        
        if depot_filter != 'All':
            driver_df_filtered = df[df['_depot_id'] == depot_filter]
        else:
            driver_df_filtered = df
    else:
        driver_df_filtered = df
    
    # Check if transporter_id column exists
    if 'transporter_id' not in driver_df_filtered.columns:
        st.warning("⚠️ Keine transporter_id Spalte in den Daten gefunden.")
        st.info("Erwartete Spaltenamen: transporter_id, driver, fahrer, driverid, fahrer_id")
        return
    
    # Driver selector
    drivers = sorted(driver_df_filtered['transporter_id'].dropna().unique())
    
    if len(drivers) == 0:
        st.warning("Keine Fahrer in den Daten gefunden.")
        return
        
    selected_driver = st.selectbox("Select Driver", drivers)
    
    if selected_driver:
        driver_df_single = driver_df_filtered[driver_df_filtered['transporter_id'] == selected_driver]
        
        # Driver metrics
        _render_driver_metrics(driver_df_single, selected_driver, features_df)
        
        st.divider()
        
        # Feature profile
        if features_df is not None and len(features_df) > 0 and selected_driver in features_df.index:
            _render_feature_profile(features_df.loc[selected_driver])
            st.divider()
        
        # Driver delivery timeline
        _render_driver_timeline(driver_df_single)


def _render_driver_metrics(driver_df: pd.DataFrame, driver_id: str, features_df: Optional[pd.DataFrame]):
    """Render driver metrics row."""
    col1, col2, col3, col4 = st.columns(4)
    
    driver_deliveries = len(driver_df)
    has_concession = 'concession_type' in driver_df.columns
    driver_concessions = driver_df['concession_type'].notna().sum() if has_concession else 0
    driver_rate = driver_concessions / driver_deliveries * 100 if driver_deliveries > 0 else 0
    
    col1.metric("Total Deliveries", driver_deliveries)
    col2.metric("Concessions", driver_concessions if has_concession else "N/A")
    col3.metric("Rate", f"{driver_rate:.2f}%" if has_concession else "N/A")
    
    if features_df is not None and len(features_df) > 0 and driver_id in features_df.index:
        if 'rate_trend_7d' in features_df.columns:
            trend = features_df.loc[driver_id, 'rate_trend_7d']
            col4.metric("7d Trend", f"{trend*100:+.2f}%", delta_color="inverse")


def _render_feature_profile(driver_features: pd.Series):
    """Render driver feature profile."""
    st.subheader("📊 Feature Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📈 Historical Rates**")
        st.write(f"• 7-day: {driver_features.get('concession_rate_7d', 0)*100:.2f}%")
        st.write(f"• 30-day: {driver_features.get('concession_rate_30d', 0)*100:.2f}%")
        st.write(f"• 90-day: {driver_features.get('concession_rate_90d', 0)*100:.2f}%")
    
    with col2:
        st.markdown("**📞 Contact Patterns**")
        st.write(f"• Success Rate: {driver_features.get('contact_success_rate', 0)*100:.1f}%")
        st.write(f"• No-contact Streak: {driver_features.get('no_contact_streak_max', 0):.0f}")
    
    with col3:
        st.markdown("**⏰ Time Patterns**")
        st.write(f"• Morning Peak: {driver_features.get('morning_peak_ratio', 0)*100:.1f}%")
        st.write(f"• Evening Peak: {driver_features.get('evening_peak_ratio', 0)*100:.1f}%")
        st.write(f"• Weekend: {driver_features.get('weekend_ratio', 0)*100:.1f}%")


def _render_driver_timeline(driver_df: pd.DataFrame):
    """Render driver delivery timeline chart."""
    st.subheader("📅 Delivery Timeline")
    
    if 'delivery_date_time' not in driver_df.columns:
        st.info("Keine Zeitdaten für Timeline verfügbar")
        return
    
    driver_df = driver_df.copy()
    driver_df['date'] = driver_df['delivery_date_time'].dt.date
    has_concession = 'concession_type' in driver_df.columns
    
    if has_concession:
        daily = driver_df.groupby('date').agg({
            'concession_type': lambda x: x.notna().sum(),
            'transporter_id': 'count'
        }).reset_index()
        daily.columns = ['date', 'concessions', 'total']
        daily['rate'] = daily['concessions'] / daily['total'] * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily['date'], y=daily['total'], name='Deliveries', marker_color='#90CAF9'))
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['rate'], name='Rate %', yaxis='y2', 
                                  mode='lines+markers', marker_color='#C62828'))
        
        fig.update_layout(
            yaxis=dict(title='Deliveries'),
            yaxis2=dict(title='Concession Rate %', overlaying='y', side='right'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            height=300
        )
    else:
        daily = driver_df.groupby('date').size().reset_index(name='total')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily['date'], y=daily['total'], name='Deliveries', marker_color='#1a237e'))
        fig.update_layout(
            yaxis=dict(title='Deliveries'),
            height=300
        )
    
    st.plotly_chart(fig, use_container_width=True)
