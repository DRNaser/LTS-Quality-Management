"""
LTS Quality Management Platform - ML Edition
Main Streamlit Application with Multi-Depot Support
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
from pathlib import Path

# Page config
st.set_page_config(
    page_title="LTS Qualitätsmanagement",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
from data_manager import DataManager, render_data_management_sidebar, render_data_upload_tab, render_depot_comparison

# Import UI components
from components.ui_components import (
    load_custom_css,
    render_page_header,
    render_kpi_card,
    render_empty_state,
    render_status_badge,
    render_section_header,
    render_action_card,
    t
)
from components.overview_tab import render_overview_tab
from components.driver_profile_tab import render_driver_profiles_tab

@st.cache_resource
def get_data_manager():
    """Get singleton data manager instance"""
    return DataManager(data_dir="data")

data_manager = get_data_manager()

# Load custom CSS theme
load_custom_css()

# Additional minimal inline styles for specific overrides
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
">
    <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700;">🎯 LTS Qualitätsmanagement</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
        KI-gestützte Analytik & Mustererkennung | Multi-Depot Edition
    </p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# SIDEBAR - DEPOT MANAGEMENT
# =============================================================================

with st.sidebar:
    st.markdown("### 🏢 LTS Qualitätsplattform")
    st.markdown("---")
    
    # Depot management section
    depots = render_data_management_sidebar(data_manager)
    
    st.markdown("---")
    
    # Data source selection
    st.header("📊 Datenquelle")
    
    if depots:
        data_source = st.radio(
            "Datenquelle auswählen",
            ["📦 Depot-Daten", "📁 Schnell-Upload"],
            index=0,
            label_visibility="collapsed"
        )
        
        if data_source == "📦 Depot-Daten":
            # Select which depots to analyze
            selected_depots = st.multiselect(
                "Depots auswählen",
                options=depots,
                default=depots,
                format_func=lambda x: f"{x} ({data_manager.metadata['depots'][x].get('name', x)})"
            )
        else:
            selected_depots = []
    else:
        data_source = st.radio(
            "Datenquelle auswählen",
            ["📁 Schnell-Upload"],
            index=0,
            label_visibility="collapsed"
        )
        selected_depots = []
    
    st.markdown("---")
    
    # Date filter
    st.header("🔍 Filter")
    
    date_range = st.date_input(
        "Date Range",
        value=(datetime(2024, 1, 1), datetime.now()),
        help="Filter data to this date range"
    )
    
    st.markdown("---")
    
    # System info
    st.markdown("### ℹ️ Systeminfo")
    total_records = data_manager.metadata.get("total_records", 0)
    st.caption(f"Total Records: {total_records:,}")
    st.caption(f"Depots: {len(depots)}")
    st.caption(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()


# =============================================================================
# DATA LOADING
# =============================================================================

# Demo data removed - use real depot data or quick upload only


@st.cache_data
def load_uploaded_data(file):
    """Load data from uploaded file"""
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def detect_depot_from_data(df: pd.DataFrame) -> str:
    """Auto-detect depot/station from uploaded data"""
    # Check common depot/station columns
    depot_columns = ['station', 'dsp', 'depot', 'depot_id', 'station_id', 'standort']
    
    for col in depot_columns:
        if col in df.columns:
            # Get most common value
            values = df[col].dropna().astype(str)
            if len(values) > 0:
                detected = values.mode().iloc[0] if len(values.mode()) > 0 else values.iloc[0]
                return str(detected).upper()
    
    return None


# Determine which data to use
if data_source == "📦 Depot-Daten" and selected_depots:
    df = data_manager.get_all_data(selected_depots)
    if df.empty:
        st.warning("⚠️ Keine Daten in den ausgewählten Depots. Laden Sie zuerst Daten hoch.")
        st.stop()
    else:
        st.sidebar.success(f"✅ {len(df):,} Datensätze aus {len(selected_depots)} Depot(s) geladen")
        
elif data_source == "📁 Schnell-Upload":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📤 Daten hochladen")
    
    uploaded_file = st.sidebar.file_uploader(
        "CSV oder Excel Datei",
        type=['csv', 'xlsx'],
        help="Daten werden automatisch analysiert",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        df = load_uploaded_data(uploaded_file)
        
        # Auto-detect depot
        detected_depot = detect_depot_from_data(df)
        
        if detected_depot:
            st.sidebar.success(f"🔍 Depot erkannt: **{detected_depot}**")
            df['_depot_id'] = detected_depot
            
            # Offer to save to depot
            if st.sidebar.checkbox(f"Zu Depot '{detected_depot}' hinzufügen", value=False):
                if detected_depot not in data_manager.get_depots():
                    data_manager.add_depot(detected_depot, detected_depot)
                result = data_manager.append_data(detected_depot, df)
                st.sidebar.info(f"💾 {result['new_records']} neue Datensätze gespeichert")
        else:
            st.sidebar.info("ℹ️ Kein Depot erkannt (station/dsp Spalte fehlt)")
            df['_depot_id'] = 'UPLOAD'
        
        st.sidebar.success(f"✅ {len(df):,} Datensätze geladen")
    else:
        st.warning("📤 Bitte laden Sie eine CSV oder Excel Datei hoch.")
        st.stop()

else:
    # No data selected
    st.warning("📤 Bitte wählen Sie eine Datenquelle aus oder laden Sie Daten hoch.")
    st.stop()

# Apply date filter
if 'delivery_date_time' in df.columns:
    df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
    if date_range and len(date_range) == 2:
        df = df[(df['delivery_date_time'].dt.date >= date_range[0]) & 
                (df['delivery_date_time'].dt.date <= date_range[1])]


# =============================================================================
# FEATURE ENGINEERING (cached)
# =============================================================================

@st.cache_data
def compute_features(data):
    """Compute ML features for all drivers"""
    from ml_engine.feature_engineering import FeatureEngineer
    fe = FeatureEngineer()
    return fe.transform(data)


# Compute features
with st.spinner("Computing driver features..."):
    try:
        features_df = compute_features(df)
        # Add depot info to features
        if '_depot_id' in df.columns:
            driver_depot = df.groupby('transporter_id')['_depot_id'].first()
            features_df['_depot_id'] = features_df.index.map(driver_depot)
    except Exception as e:
        st.error(f"Error computing features: {e}")
        features_df = pd.DataFrame()


# =============================================================================
# MAIN TABS
# =============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Überblick",
    "🏭 Depot-Vergleich",
    "🎯 Risikoanalyse",
    "🔬 Mustererkennung",
    "🚨 Missbrauchserkennung",
    "👤 Fahrerprofile",
    "📤 Datenverwaltung"
])


# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================

with tab1:
    st.header("📊 Executive Overview")
    
    # Helper function for safe column access
    def safe_col_sum(dataframe, col, condition_func=None):
        """Safely sum a column, return 0 if column doesn't exist"""
        if col not in dataframe.columns:
            return 0
        if condition_func:
            return condition_func(dataframe[col]).sum()
        return dataframe[col].sum()
    
    def has_concession_type(dataframe):
        """Check if concession_type column exists and has data"""
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
        
        if 'delivery_date_time' in df.columns:
            df['date'] = df['delivery_date_time'].dt.date
            
            if has_concession_type(df):
                daily = df.groupby('date').agg({
                    'concession_type': lambda x: x.notna().sum(),
                    'transporter_id': 'count'
                }).reset_index()
                daily.columns = ['date', 'concessions', 'total']
                daily['rate'] = daily['concessions'] / daily['total'] * 100
            else:
                # Just show delivery counts if no concession data
                daily = df.groupby('date').size().reset_index(name='total')
                daily['rate'] = 0
                daily['concessions'] = 0
            
            daily['date'] = pd.to_datetime(daily['date'])
            
            import plotly.graph_objects as go
            fig = go.Figure()
            
            if has_concession_type(df):
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
        else:
            st.warning("No delivery_date_time column found")
    
    with col2:
        st.subheader("🍩 Concession Type Distribution")
        
        if has_concession_type(df):
            type_counts = df[df['concession_type'].notna()]['concession_type'].value_counts()
            
            import plotly.express as px
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
        else:
            st.info("Concession type column not available in data")
    
    st.divider()
    
    # Top/Bottom drivers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performers")
        if len(features_df) > 0:
            top_drivers = features_df.nsmallest(5, 'concession_rate_30d')[['concession_rate_30d']]
            if '_depot_id' in features_df.columns:
                top_drivers['depot'] = features_df.loc[top_drivers.index, '_depot_id']
            top_drivers['rate'] = (top_drivers['concession_rate_30d'] * 100).round(2).astype(str) + '%'
            display_cols = ['depot', 'rate'] if 'depot' in top_drivers.columns else ['rate']
            st.dataframe(top_drivers[display_cols], use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Need Attention")
        if len(features_df) > 0:
            bottom_drivers = features_df.nlargest(5, 'concession_rate_30d')[['concession_rate_30d', 'rate_trend_7d']]
            if '_depot_id' in features_df.columns:
                bottom_drivers['depot'] = features_df.loc[bottom_drivers.index, '_depot_id']
            bottom_drivers['rate'] = (bottom_drivers['concession_rate_30d'] * 100).round(2).astype(str) + '%'
            bottom_drivers['trend'] = bottom_drivers['rate_trend_7d'].apply(lambda x: '📈' if x > 0 else '📉')
            display_cols = ['depot', 'rate', 'trend'] if 'depot' in bottom_drivers.columns else ['rate', 'trend']
            st.dataframe(bottom_drivers[display_cols], use_container_width=True)


# =============================================================================
# TAB 2: DEPOT COMPARISON
# =============================================================================

with tab2:
    st.header("🏭 Depot Comparison")
    
    if '_depot_id' not in df.columns or df['_depot_id'].nunique() < 2:
        st.info("📊 Depot comparison requires data from at least 2 depots. Upload data to multiple depots to see comparisons.")
        
        # Show how to add depots
        st.markdown("""
        ### How to use Multi-Depot:
        1. **Add Depots** in the sidebar (e.g., DVI2, MUC1, FRA3)
        2. **Go to Data Management tab** to upload data for each depot
        3. **Return here** to compare performance across depots
        """)
    else:
        # Depot summary cards
        depot_ids = df['_depot_id'].unique()
        has_concession_col = 'concession_type' in df.columns
        
        cols = st.columns(len(depot_ids))
        for i, depot_id in enumerate(depot_ids):
            depot_df = df[df['_depot_id'] == depot_id]
            depot_rate = depot_df['concession_type'].notna().sum() / len(depot_df) * 100 if has_concession_col else 0
            depot_drivers = depot_df['transporter_id'].nunique() if 'transporter_id' in depot_df.columns else 0
            
            with cols[i]:
                st.metric(
                    f"📦 {depot_id}",
                    f"{depot_rate:.2f}%" if has_concession_col else f"{len(depot_df):,}",
                    help=f"Deliveries: {len(depot_df):,} | Drivers: {depot_drivers}"
                )
                st.caption(f"{depot_drivers} drivers | {len(depot_df):,} deliveries")
        
        st.divider()
        
        # Comparison bar chart
        if has_concession_col:
            st.subheader("📊 Concession Rate Comparison")
            
            depot_stats = df.groupby('_depot_id').agg({
                'transporter_id': 'nunique',
                'concession_type': lambda x: x.notna().sum(),
                'delivery_date_time': 'count'
            }).reset_index()
            depot_stats.columns = ['Depot', 'Drivers', 'Concessions', 'Deliveries']
            depot_stats['Rate'] = depot_stats['Concessions'] / depot_stats['Deliveries'] * 100
            
            fig = px.bar(
                depot_stats,
                x='Depot',
                y='Rate',
                color='Depot',
                text=depot_stats['Rate'].round(2).astype(str) + '%',
                title="Concession Rate by Depot"
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, yaxis_title="Concession Rate (%)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("📊 Delivery Volume Comparison")
            depot_stats = df.groupby('_depot_id').size().reset_index(name='Deliveries')
            depot_stats.columns = ['Depot', 'Deliveries']
            
            fig = px.bar(
                depot_stats,
                x='Depot',
                y='Deliveries',
                color='Depot',
                text='Deliveries',
                title="Deliveries by Depot"
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Weekly trend by depot
        st.subheader("📈 Weekly Trend by Depot")
        
        if 'delivery_date_time' in df.columns:
            df['week'] = df['delivery_date_time'].dt.isocalendar().week
            df['year'] = df['delivery_date_time'].dt.year
            df['year_week'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
            
            if has_concession_col:
                weekly = df.groupby(['_depot_id', 'year_week']).agg({
                    'concession_type': lambda x: x.notna().sum(),
                    'transporter_id': 'count'
                }).reset_index()
                weekly.columns = ['Depot', 'Week', 'Concessions', 'Deliveries']
                weekly['Rate'] = weekly['Concessions'] / weekly['Deliveries'] * 100
                y_col = 'Rate'
                y_title = "Concession Rate (%)"
            else:
                weekly = df.groupby(['_depot_id', 'year_week']).size().reset_index(name='Deliveries')
                weekly.columns = ['Depot', 'Week', 'Deliveries']
                y_col = 'Deliveries'
                y_title = "Deliveries"
            
            fig = px.line(
                weekly,
                x='Week',
                y=y_col,
                color='Depot',
                markers=True,
                title=f"Weekly {y_title} Trend"
            )
            fig.update_layout(xaxis_title="Week", yaxis_title=y_title)
            st.plotly_chart(fig, use_container_width=True)
        
        # Driver distribution by depot
        st.divider()
        st.subheader("👥 Driver Performance by Depot")
        
        if len(features_df) > 0 and '_depot_id' in features_df.columns and 'concession_rate_30d' in features_df.columns:
            fig = px.box(
                features_df.reset_index(),
                x='_depot_id',
                y='concession_rate_30d',
                color='_depot_id',
                title="Driver Concession Rate Distribution by Depot",
                labels={'_depot_id': 'Depot', 'concession_rate_30d': '30-Day Concession Rate'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Driver performance data not available")


# =============================================================================
# TAB 3: RISK ANALYSIS
# =============================================================================

with tab3:
    if len(features_df) > 0:
        # Depot filter for risk analysis
        if '_depot_id' in features_df.columns:
            depot_filter = st.multiselect(
                "Filter by Depot",
                options=features_df['_depot_id'].unique(),
                default=features_df['_depot_id'].unique(),
                key="risk_depot_filter"
            )
            filtered_features = features_df[features_df['_depot_id'].isin(depot_filter)]
            filtered_df = df[df['_depot_id'].isin(depot_filter)] if '_depot_id' in df.columns else df
        else:
            filtered_features = features_df
            filtered_df = df
        
        from components.risk_dashboard import render_risk_dashboard
        render_risk_dashboard(filtered_df, features_df=filtered_features)
    else:
        st.warning("Unable to compute features. Please check your data.")


# =============================================================================
# TAB 4: PATTERN RECOGNITION
# =============================================================================

with tab4:
    if len(features_df) > 0:
        # Depot filter for pattern analysis
        if '_depot_id' in features_df.columns:
            depot_filter = st.multiselect(
                "Filter by Depot",
                options=features_df['_depot_id'].unique(),
                default=features_df['_depot_id'].unique(),
                key="pattern_depot_filter"
            )
            filtered_features = features_df[features_df['_depot_id'].isin(depot_filter)]
            filtered_df = df[df['_depot_id'].isin(depot_filter)] if '_depot_id' in df.columns else df
        else:
            filtered_features = features_df
            filtered_df = df
        
        from components.pattern_analysis_tab import render_pattern_analysis
        render_pattern_analysis(filtered_df, filtered_features)
    else:
        st.warning("Unable to compute features. Please check your data.")


# =============================================================================
# TAB 5: CUSTOMER ABUSE DETECTION
# =============================================================================

with tab5:
    # Depot filter for abuse detection
    if '_depot_id' in df.columns:
        depot_filter = st.multiselect(
            "Filter by Depot",
            options=df['_depot_id'].unique(),
            default=df['_depot_id'].unique(),
            key="abuse_depot_filter"
        )
        filtered_df = df[df['_depot_id'].isin(depot_filter)]
    else:
        filtered_df = df
    
    from ml_engine.customer_abuse_detection import render_abuse_detection_tab
    render_abuse_detection_tab(filtered_df)


# =============================================================================
# TAB 6: DRIVER PROFILES
# =============================================================================

with tab6:
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
        st.warning("⚠️ Keine transporter_id Spalte in den Daten gefunden. Bitte laden Sie Daten mit Fahrer-Identifikation hoch.")
        st.info("Erwartete Spaltenamen: transporter_id, driver, fahrer, driverid, fahrer_id")
    else:
        # Driver selector
        drivers = sorted(driver_df_filtered['transporter_id'].dropna().unique())
        
        if len(drivers) == 0:
            st.warning("Keine Fahrer in den Daten gefunden.")
        else:
            selected_driver = st.selectbox("Select Driver", drivers)
            
            if selected_driver:
                driver_df_single = driver_df_filtered[driver_df_filtered['transporter_id'] == selected_driver]
                
                # Driver metrics
                col1, col2, col3, col4 = st.columns(4)
                
                driver_deliveries = len(driver_df_single)
                has_concession = 'concession_type' in driver_df_single.columns
                driver_concessions = driver_df_single['concession_type'].notna().sum() if has_concession else 0
                driver_rate = driver_concessions / driver_deliveries * 100 if driver_deliveries > 0 else 0
                
                col1.metric("Total Deliveries", driver_deliveries)
                col2.metric("Concessions", driver_concessions if has_concession else "N/A")
                col3.metric("Rate", f"{driver_rate:.2f}%" if has_concession else "N/A")
                
                if len(features_df) > 0 and selected_driver in features_df.index and 'rate_trend_7d' in features_df.columns:
                    trend = features_df.loc[selected_driver, 'rate_trend_7d']
                    col4.metric("7d Trend", f"{trend*100:+.2f}%", delta_color="inverse")
                
                st.divider()
                
                # Feature profile
                if len(features_df) > 0 and selected_driver in features_df.index:
                    st.subheader("📊 Feature Profile")
                    
                    driver_features = features_df.loc[selected_driver]
                    
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
                
                st.divider()
        
                # Driver delivery timeline
                st.subheader("📅 Delivery Timeline")
                
                if 'delivery_date_time' in driver_df_single.columns:
                    driver_df_single = driver_df_single.copy()
                    driver_df_single['date'] = driver_df_single['delivery_date_time'].dt.date
                    
                    if has_concession:
                        daily = driver_df_single.groupby('date').agg({
                            'concession_type': lambda x: x.notna().sum(),
                            'transporter_id': 'count'
                        }).reset_index()
                        daily.columns = ['date', 'concessions', 'total']
                        daily['rate'] = daily['concessions'] / daily['total'] * 100
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=daily['date'], y=daily['total'], name='Deliveries', marker_color='#90CAF9'))
                        fig.add_trace(go.Scatter(x=daily['date'], y=daily['rate'], name='Rate %', yaxis='y2', mode='lines+markers', marker_color='#C62828'))
                        
                        fig.update_layout(
                            yaxis=dict(title='Deliveries'),
                            yaxis2=dict(title='Concession Rate %', overlaying='y', side='right'),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02),
                            height=300
                        )
                    else:
                        daily = driver_df_single.groupby('date').size().reset_index(name='total')
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=daily['date'], y=daily['total'], name='Deliveries', marker_color='#1a237e'))
                        fig.update_layout(
                            yaxis=dict(title='Deliveries'),
                            height=300
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Keine Zeitdaten für Timeline verfügbar")


# =============================================================================
# TAB 7: DATA MANAGEMENT
# =============================================================================

with tab7:
    render_data_upload_tab(data_manager)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🎯 LTS Quality Management Platform - ML Edition</p>
    <p>Powered by XGBoost, SHAP, and Advanced Pattern Recognition | Multi-Depot Support</p>
</div>
""", unsafe_allow_html=True)
