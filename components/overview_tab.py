"""
Overview Tab Component
Renders the main executive overview dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


def render_overview_tab(df: pd.DataFrame, features_df: Optional[pd.DataFrame] = None):
    """
    Render the Executive Overview tab.
    
    Args:
        df: Delivery data DataFrame
        features_df: Pre-computed driver features
    """
    st.header("📊 Executive Overview")
    
    # Helper functions
    def safe_col_sum(dataframe, col, condition_func=None):
        if col not in dataframe.columns:
            return 0
        if condition_func:
            return condition_func(dataframe[col]).sum()
        return dataframe[col].sum()
    
    def has_concession_type(dataframe):
        return 'concession_type' in dataframe.columns
    
    # Show depot badges if multi-depot
    if '_depot_id' in df.columns:
        depot_ids = df['_depot_id'].unique()
        if len(depot_ids) > 1:
            st.markdown("**Active Depots:** " + " ".join([f"📦 {d}" for d in depot_ids]))
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_deliveries = len(df)
    total_drivers = df['transporter_id'].nunique() if 'transporter_id' in df.columns else 0
    total_concessions = df['concession_type'].notna().sum() if has_concession_type(df) else 0
    concession_rate = total_concessions / total_deliveries * 100 if total_deliveries > 0 else 0
    
    # Calculate trend
    rate_delta = 0
    if has_concession_type(df) and 'delivery_date_time' in df.columns:
        df_sorted = df.sort_values('delivery_date_time')
        if len(df_sorted) > 100:
            recent = df_sorted.tail(len(df_sorted)//2)
            previous = df_sorted.head(len(df_sorted)//2)
            recent_rate = recent['concession_type'].notna().sum() / len(recent) * 100
            prev_rate = previous['concession_type'].notna().sum() / len(previous) * 100
            rate_delta = recent_rate - prev_rate
    
    col1.metric("Total Deliveries", f"{total_deliveries:,}")
    col2.metric("Active Drivers", total_drivers)
    col3.metric("Total Concessions", total_concessions)
    col4.metric("Concession Rate", f"{concession_rate:.2f}%",
                delta=f"{rate_delta:+.2f}%" if rate_delta != 0 else None, delta_color="inverse")
    
    if 'concession_cost' in df.columns:
        total_cost = df['concession_cost'].sum()
        col5.metric("Cost Impact", f"€{total_cost:,.0f}")
    else:
        col5.metric("Records", f"{total_deliveries:,}")
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Trend")
        _render_daily_trend(df, has_concession_type(df))
    
    with col2:
        st.subheader("🍩 Concession Type Distribution")
        _render_concession_distribution(df, has_concession_type(df))
    
    st.divider()
    
    # Top/Bottom drivers
    if features_df is not None and len(features_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top Performers")
            _render_top_performers(features_df)
        
        with col2:
            st.subheader("⚠️ Need Attention")
            _render_need_attention(features_df)


def _render_daily_trend(df: pd.DataFrame, has_concession: bool):
    """Render daily trend chart."""
    if 'delivery_date_time' not in df.columns:
        st.warning("No delivery_date_time column found")
        return
    
    df = df.copy()
    df['date'] = df['delivery_date_time'].dt.date
    
    if has_concession:
        daily = df.groupby('date').agg({
            'concession_type': lambda x: x.notna().sum(),
            'transporter_id': 'count'
        }).reset_index()
        daily.columns = ['date', 'concessions', 'total']
        daily['rate'] = daily['concessions'] / daily['total'] * 100
    else:
        daily = df.groupby('date').size().reset_index(name='total')
        daily['rate'] = 0
        daily['concessions'] = 0
    
    daily['date'] = pd.to_datetime(daily['date'])
    
    fig = go.Figure()
    
    if has_concession:
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['rate'],
            mode='lines+markers',
            name='Concession Rate',
            line=dict(color='#1a237e', width=2)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Concession Rate (%)",
            height=300
        )
    else:
        fig.add_trace(go.Bar(
            x=daily['date'], y=daily['total'],
            name='Deliveries',
            marker_color='#1a237e'
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Deliveries",
            height=300
        )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_concession_distribution(df: pd.DataFrame, has_concession: bool):
    """Render concession type pie chart."""
    if not has_concession:
        st.info("Concession type column not available in data")
        return
    
    type_counts = df[df['concession_type'].notna()]['concession_type'].value_counts()
    
    if len(type_counts) > 0:
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            hole=0.4
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No concessions in selected period")


def _render_top_performers(features_df: pd.DataFrame):
    """Render top performing drivers table."""
    if 'concession_rate_30d' not in features_df.columns:
        st.info("No rate data available")
        return
    
    top_drivers = features_df.nsmallest(5, 'concession_rate_30d')[['concession_rate_30d']]
    if '_depot_id' in features_df.columns:
        top_drivers['depot'] = features_df.loc[top_drivers.index, '_depot_id']
    top_drivers['rate'] = (top_drivers['concession_rate_30d'] * 100).round(2).astype(str) + '%'
    display_cols = ['depot', 'rate'] if 'depot' in top_drivers.columns else ['rate']
    st.dataframe(top_drivers[display_cols], use_container_width=True)


def _render_need_attention(features_df: pd.DataFrame):
    """Render drivers needing attention table."""
    if 'concession_rate_30d' not in features_df.columns:
        st.info("No rate data available")
        return
    
    bottom_drivers = features_df.nlargest(5, 'concession_rate_30d')[['concession_rate_30d', 'rate_trend_7d']]
    if '_depot_id' in features_df.columns:
        bottom_drivers['depot'] = features_df.loc[bottom_drivers.index, '_depot_id']
    bottom_drivers['rate'] = (bottom_drivers['concession_rate_30d'] * 100).round(2).astype(str) + '%'
    bottom_drivers['trend'] = bottom_drivers['rate_trend_7d'].apply(lambda x: '📈' if x > 0 else '📉')
    display_cols = ['depot', 'rate', 'trend'] if 'depot' in bottom_drivers.columns else ['rate', 'trend']
    st.dataframe(bottom_drivers[display_cols], use_container_width=True)
