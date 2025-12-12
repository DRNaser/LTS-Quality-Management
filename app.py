"""
LTS Quality Management
Google-DNA Design & Behavioral Coaching
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
# Page Configuration
st.set_page_config(
    page_title="LTS Quality",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Google-DNA CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    :root {
        --google-blue: #1a73e8;
        --google-blue-hover: #1557b0;
        --google-red: #d93025;
        --google-green: #1e8e3d;
        --google-yellow: #f9ab00;
        --gray-50: #f8f9fa;
        --gray-100: #f1f3f4;
        --gray-200: #e8eaed;
        --gray-300: #dadce0;
        --gray-500: #9aa0a6;
        --gray-700: #5f6368;
        --gray-900: #202124;
        --font-stack: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    html, body, [class*="css"] {
        font-family: var(--font-stack);
        color: var(--gray-900);
    }
    
    .stApp {
        background-color: white;
    }
    
    /* Header Navigation */
    header[data-testid="stHeader"] {
        background: white;
        border-bottom: 1px solid var(--gray-200);
        height: 60px;
    }
    
    #MainMenu, footer, .stDeployButton { display: none; }
    
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    /* Tabs - Google Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid var(--gray-200);
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 4px;
        background: transparent;
        border: none;
        color: var(--gray-700);
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--google-blue) !important;
        border-bottom: 2px solid var(--google-blue) !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Google Sans', 'Roboto', sans-serif;
        font-weight: 400;
        color: var(--gray-900);
    }
    
    h1 { font-size: 1.75rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.25rem; margin-bottom: 1rem; color: var(--gray-900); }
    h3 { font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem; color: var(--gray-900); }
    
    .meta-text {
        font-size: 0.75rem;
        color: var(--gray-700);
    }
    
    /* Global Header */
    .global-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 24px;
        margin-bottom: 0;
    }
    
    .header-logo {
        font-size: 1.25rem;
        font-weight: 500;
        color: var(--gray-700);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .header-stats {
        font-size: 0.875rem;
        color: var(--gray-700);
        background: var(--gray-100);
        padding: 6px 12px;
        border-radius: 16px;
    }
    
    /* Cards - Flat & Functional */
    .g-card {
        border-bottom: 1px solid var(--gray-200);
        padding: 16px 0;
        margin-bottom: 8px;
    }
    
    .g-card:last-child { border-bottom: none; }
    
    .g-card-title {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 4px;
        color: var(--google-blue);
    }
    
    .g-card-stat {
        font-size: 0.875rem;
        color: var(--gray-700);
        margin-bottom: 8px;
    }
    
    /* Driver List Item */
    .driver-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        border-bottom: 1px solid var(--gray-200);
        cursor: pointer;
        transition: background 0.1s;
    }
    
    .driver-item:hover {
        background: var(--gray-50);
    }
    
    .driver-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--google-blue);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 12px;
    }
    
    /* Risk Tags */
    .risk-tag {
        font-size: 0.75rem;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: 4px;
    }
    
    .risk-critical { background: #fce8e6; color: #c5221f; }
    .risk-warning { background: #ffeec2; color: #b06000; }
    .risk-ok { background: #e6f4ea; color: #137333; }
    
    /* Coaching UI */
    .coaching-step {
        margin-bottom: 24px;
    }
    
    .step-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--gray-700);
        text-transform: uppercase;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    
    .step-content {
        font-size: 1rem;
        color: var(--gray-900);
        line-height: 1.5;
    }
    
    /* Primary Action Button */
    .stButton button {
        background-color: var(--google-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
        box-shadow: 0 1px 2px rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15) !important;
        transition: background .2s, box-shadow .2s;
    }
    
    .stButton button:hover {
        background-color: var(--google-blue-hover) !important;
        box-shadow: 0 1px 3px rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15) !important;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 48px 0;
        color: var(--gray-700);
    }
    
    .empty-icon {
        font-size: 24px;
        margin-bottom: 12px;
        opacity: 0.5;
    }
    
    /* Mobile Responsive */
    @media (max-width: 600px) {
        .main .block-container {
            padding: 1rem;
        }
        .global-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
        }
    }
    
    /* High Value Alert */
    .hv-alert {
        background: linear-gradient(135deg, #fce8e6 0%, #f8d7da 100%);
        border-left: 4px solid #c5221f;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    
    .hv-alert-title {
        font-size: 1rem;
        font-weight: 500;
        color: #c5221f;
        margin-bottom: 8px;
    }
    
    .hv-alert-detail {
        font-size: 0.875rem;
        color: #5f6368;
    }
    
    /* Time Analysis Card */
    .time-card {
        background: var(--gray-50);
        padding: 16px;
        border-radius: 8px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 16px;
    }
    
    .time-stat {
        text-align: center;
    }
    
    .time-stat-value {
        font-size: 1.25rem;
        font-weight: 500;
        color: var(--google-blue);
    }
    
    .time-stat-label {
        font-size: 0.75rem;
        color: var(--gray-700);
        margin-top: 4px;
    }
    
    /* Mismatch Detector */
    .mismatch-card {
        background: #fef7e0;
        border-left: 4px solid #f9ab00;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 8px;
    }
    
    .mismatch-critical {
        background: #fce8e6;
        border-left-color: #c5221f;
    }
    
    /* Concession Type Badge */
    .type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .type-household { background: #e8f0fe; color: #1967d2; }
    .type-mailslot { background: #e6f4ea; color: #137333; }
    .type-neighbor { background: #fef7e0; color: #b06000; }
    .type-receptionist { background: #f3e8fd; color: #7627bb; }
    .type-safelocation { background: #fce8e6; color: #c5221f; }
</style>
""", unsafe_allow_html=True)
# ============================================================================
# UTILS & DATA
# ============================================================================
def load_file_data(uploaded_file):
    try:
        if uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        
        # Clean Columns
        df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', '')
        
        # Y/N to Numeric
        yn_cols = ['High Value Item (Y/N)', 'Feedback False Scan Indicator', 'Attended DNR Deliveries']
        for col in yn_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: 1 if str(x).upper().strip() in ['Y', 'YES', '1', 'TRUE'] else 0)
        
        # Numeric Conversion
        num_cols = ['Concession Cost', 'Geo Distance > 25m', 'Delivered to Household Member / Customer',
                    'Delivery preferences not followed', 'Unattended Delivery & No Photo on Delivery']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
        # Fill missing critical columns
        if 'zip_code' not in df.columns: df['zip_code'] = 'Unknown'
        if 'year_week' not in df.columns: df['year_week'] = 'Unknown'
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
def get_driver_problem(df):
    problems = {
        'Geo >25m': df.get('Geo Distance > 25m', 0).sum(),
        'Household': df.get('Delivered to Household Member / Customer', 0).sum(),
        'Lieferpräferenz': df.get('Delivery preferences not followed', 0).sum(),
        'Kein Foto': df.get('Unattended Delivery & No Photo on Delivery', 0).sum(),
        'False Scan': df.get('Feedback False Scan Indicator', 0).sum(),
    }
    if sum(problems.values()) == 0: return "Keine", problems
    return max(problems, key=problems.get), problems
def get_trend(df, driver_id):
    if 'year_week' not in df.columns: return []
    return df[df['transporter_id'] == driver_id].groupby('year_week').size().sort_index().tolist()[-4:]
def get_time_analysis(df, driver_id=None):
    """Analyze delivery time patterns from timestamp columns."""
    result = {
        'peak_hour': None,
        'peak_hour_pct': 0,
        'peak_day': None,
        'peak_day_pct': 0,
        'days_since_last': None,
        'hourly_dist': {},
        'daily_dist': {}
    }
    
    # Find timestamp column
    time_cols = ['shipment_delivered_date', 'shipment_created_timestamp', 'delivered_date', 
                 'delivery_timestamp', 'created_at', 'timestamp']
    time_col = None
    for col in time_cols:
        if col in df.columns:
            time_col = col
            break
    
    if time_col is None:
        return result
    
    # Filter by driver if specified
    data = df[df['transporter_id'] == driver_id] if driver_id else df
    if len(data) == 0:
        return result
    
    try:
        # Parse timestamps
        timestamps = pd.to_datetime(data[time_col], errors='coerce')
        valid_ts = timestamps.dropna()
        
        if len(valid_ts) == 0:
            return result
        
        # Hourly distribution
        hours = valid_ts.dt.hour
        hourly_counts = hours.value_counts().sort_index()
        result['hourly_dist'] = hourly_counts.to_dict()
        
        if len(hourly_counts) > 0:
            peak_hour = hourly_counts.idxmax()
            result['peak_hour'] = f"{peak_hour:02d}:00-{(peak_hour+1)%24:02d}:00"
            result['peak_hour_pct'] = (hourly_counts.max() / len(valid_ts)) * 100
        
        # Daily distribution (weekday)
        days = valid_ts.dt.dayofweek
        day_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        daily_counts = days.value_counts().sort_index()
        result['daily_dist'] = {day_names[i]: c for i, c in daily_counts.items()}
        
        if len(daily_counts) > 0:
            peak_day_idx = daily_counts.idxmax()
            result['peak_day'] = day_names[peak_day_idx]
            result['peak_day_pct'] = (daily_counts.max() / len(valid_ts)) * 100
        
        # Days since last incident
        latest = valid_ts.max()
        result['days_since_last'] = (datetime.now() - latest).days
        
    except Exception:
        pass
    
    return result
def detect_mailbox_mismatches(df):
    """Detect suspicious booking patterns."""
    mismatches = []
    
    # Type 1: Mailbox-eligible marked as Household
    # Check for Delivery Preference Type or similar columns
    pref_cols = ['Delivery Preference Type', 'delivery_preference', 'pref_type']
    pref_col = None
    for col in pref_cols:
        if col in df.columns:
            pref_col = col
            break
    
    household_col = 'Delivered to Household Member / Customer'
    
    if pref_col and household_col in df.columns:
        # Find where preference is mailslot/mailbox but marked as household
        mailbox_keywords = ['mailslot', 'mailbox', 'briefkasten', 'postfach']
        for idx, row in df.iterrows():
            pref_val = str(row.get(pref_col, '')).lower()
            is_mailbox_pref = any(kw in pref_val for kw in mailbox_keywords)
            is_household = row.get(household_col, 0) == 1
            
            if is_mailbox_pref and is_household:
                mismatches.append({
                    'tracking_id': row.get('tracking_id', 'Unknown'),
                    'transporter_id': row.get('transporter_id', 'Unknown'),
                    'mismatch_type': 'Briefkasten als Household',
                    'severity': 'warning',
                    'detail': f"Präferenz: {row.get(pref_col, 'N/A')}"
                })
    
    # Type 2: Safe Location without photo
    no_photo_col = 'Unattended Delivery & No Photo on Delivery'
    if no_photo_col in df.columns:
        no_photo_df = df[df[no_photo_col] == 1]
        for idx, row in no_photo_df.iterrows():
            mismatches.append({
                'tracking_id': row.get('tracking_id', 'Unknown'),
                'transporter_id': row.get('transporter_id', 'Unknown'),
                'mismatch_type': 'Safe Location ohne Foto',
                'severity': 'critical',
                'detail': f"PLZ: {row.get('zip_code', 'N/A')}"
            })
    
    return pd.DataFrame(mismatches) if mismatches else pd.DataFrame()
def get_concession_type_distribution(df):
    """Get distribution of concession/delivery types."""
    types = {
        'Household Member': 0,
        'Mailslot': 0,
        'Neighbor': 0,
        'Receptionist': 0,
        'Safe Location': 0,
        'Other': 0
    }
    
    # Check for explicit type column
    type_cols = ['Delivered to Type', 'Concession_type_of_delivery', 'delivery_type', 'concession_type']
    type_col = None
    for col in type_cols:
        if col in df.columns:
            type_col = col
            break
    
    if type_col:
        # Use explicit type column
        type_counts = df[type_col].value_counts()
        for t, c in type_counts.items():
            t_lower = str(t).lower()
            if 'household' in t_lower or 'member' in t_lower:
                types['Household Member'] += c
            elif 'mail' in t_lower or 'slot' in t_lower or 'brief' in t_lower:
                types['Mailslot'] += c
            elif 'neighbor' in t_lower or 'nachbar' in t_lower:
                types['Neighbor'] += c
            elif 'recep' in t_lower or 'empfang' in t_lower:
                types['Receptionist'] += c
            elif 'safe' in t_lower or 'ablage' in t_lower:
                types['Safe Location'] += c
            else:
                types['Other'] += c
    else:
        # Derive from existing flags
        if 'Delivered to Household Member / Customer' in df.columns:
            types['Household Member'] = int(df['Delivered to Household Member / Customer'].sum())
        if 'Unattended Delivery & No Photo on Delivery' in df.columns:
            types['Safe Location'] = int(df['Unattended Delivery & No Photo on Delivery'].sum())
        # Remaining go to Other
        total_flags = types['Household Member'] + types['Safe Location']
        types['Other'] = max(0, len(df) - total_flags)
    
    return {k: v for k, v in types.items() if v > 0}
def get_high_value_summary(df):
    """Get summary of high-value item concessions."""
    hv_col = 'High Value Item (Y/N)'
    cost_col = 'Concession Cost'
    
    if hv_col not in df.columns:
        return {'total_count': 0, 'total_cost': 0, 'by_driver': [], 'records': pd.DataFrame()}
    
    hv_df = df[df[hv_col] == 1]
    
    if len(hv_df) == 0:
        return {'total_count': 0, 'total_cost': 0, 'by_driver': [], 'records': pd.DataFrame()}
    
    total_count = len(hv_df)
    total_cost = hv_df[cost_col].sum() if cost_col in hv_df.columns else 0
    
    # Group by driver
    by_driver = []
    driver_groups = hv_df.groupby('transporter_id')
    for driver_id, group in driver_groups:
        driver_cost = group[cost_col].sum() if cost_col in group.columns else 0
        by_driver.append({
            'transporter_id': driver_id,
            'count': len(group),
            'cost': driver_cost
        })
    
    by_driver = sorted(by_driver, key=lambda x: x['count'], reverse=True)
    
    return {
        'total_count': total_count,
        'total_cost': total_cost,
        'by_driver': by_driver[:5],  # Top 5
        'records': hv_df
    }
# ============================================================================
# MAIN
# ============================================================================
def main():
    # --- Header ---
    if 'data' not in st.session_state:
        st.session_state.data = None
    with st.container():
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div class="header-logo">📊 LTS Quality</div>', unsafe_allow_html=True)
    
    # --- Data Loading (Hidden in Drawer usually, but Expander here) ---
    if st.session_state.data is None:
        with st.expander("Importer", expanded=True):
            uploaded = st.file_uploader("Upload Concession Data (CSV/Excel)", label_visibility="collapsed")
            if uploaded:
                st.session_state.data = load_file_data(uploaded)
                st.rerun()
        
        # Empty State
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📂</div>
            <div>No data loaded yet.</div>
            <div style="font-size:0.75rem; margin-top:8px;">Please upload your Concession Report to start.</div>
        </div>
        """, unsafe_allow_html=True)
        return
    df = st.session_state.data
    
    # --- Global Stats (Neutral) ---
    weeks = sorted([str(w) for w in df['year_week'].unique()])
    week_range = f"{weeks[0]} - {weeks[-1]}" if weeks else "All time"
    total_dnr = len(df)
    
    st.markdown(f'<div class="header-stats" style="margin-bottom: 24px;">{week_range} &nbsp; • &nbsp; {total_dnr} Concessions</div>', unsafe_allow_html=True)
    # --- Navigation ---
    tab_overview, tab_drivers, tab_insights, tab_actions = st.tabs(["Overview", "Drivers", "Insights", "Actions"])
    # 1. OVERVIEW (Roadmap transformed)
    with tab_overview:
        st.markdown("### Focus Areas")
        
        buckets = {
            'Household ohne Übergabe': df.get('Delivered to Household Member / Customer', pd.Series([0])).sum(),
            'Lieferpräferenz nicht eingehalten': df.get('Delivery preferences not followed', pd.Series([0])).sum(),
            'Geo-Verstoß (>25m)': df.get('Geo Distance > 25m', pd.Series([0])).sum(),
            'Kein Foto bei Ablage': df.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum(),
            'False Scans': df.get('Feedback False Scan Indicator', pd.Series([0])).sum(),
        }
        
        sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)
        total_issues = sum(buckets.values())
        
        if total_issues == 0:
            st.info("No issues detected in the uploaded data.")
        else:
            for reason, count in sorted_buckets:
                if count == 0: continue
                pct = (count / total_issues) * 100
                st.markdown(f"""
                <div class="g-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div class="g-card-title" style="color: var(--gray-900); font-weight: 500;">{reason}</div>
                        <div style="color: var(--gray-500); font-size: 0.875rem;">{pct:.0f}%</div>
                    </div>
                    <div class="g-card-stat">{int(count)} Fälle &nbsp;·&nbsp; Kritisch</div>
                    <div style="height: 4px; background: var(--gray-100); border-radius: 2px; width: 100%; margin-top: 4px;">
                        <div style="height: 4px; background: var(--google-blue); border-radius: 2px; width: {pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # --- HIGH VALUE ALERT ---
        hv_summary = get_high_value_summary(df)
        if hv_summary['total_count'] > 0:
            st.markdown("---")
            top_driver = hv_summary['by_driver'][0] if hv_summary['by_driver'] else None
            top_info = f"Top-Fahrer: {top_driver['transporter_id']} ({top_driver['count']} Fälle)" if top_driver else ""
            
            st.markdown(f"""
            <div class="hv-alert">
                <div class="hv-alert-title">⚠️ {hv_summary['total_count']} High-Value Concessions</div>
                <div class="hv-alert-detail">
                    {top_info} | Gesamt: €{hv_summary['total_cost']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("High-Value Details anzeigen"):
                hv_table = []
                for d in hv_summary['by_driver']:
                    hv_table.append({
                        'Fahrer': d['transporter_id'],
                        'Anzahl': d['count'],
                        'Kosten': f"€{d['cost']:,.2f}"
                    })
                if hv_table:
                    st.dataframe(pd.DataFrame(hv_table), use_container_width=True, hide_index=True)
        
        # --- CONCESSION TYPE DISTRIBUTION ---
        st.markdown("---")
        st.markdown("### 📊 Zustellart-Verteilung")
        
        type_dist = get_concession_type_distribution(df)
        if type_dist:
            # Create horizontal bar chart
            type_df = pd.DataFrame([
                {'Typ': k, 'Anzahl': v} for k, v in sorted(type_dist.items(), key=lambda x: x[1], reverse=True)
            ])
            
            fig = px.bar(type_df, x='Anzahl', y='Typ', orientation='h', text='Anzahl',
                        color='Typ', color_discrete_sequence=['#1a73e8', '#34a853', '#fbbc04', '#ea4335', '#9aa0a6', '#5f6368'])
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor='white',
                margin=dict(t=10, l=0, r=40, b=0),
                xaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None),
                yaxis=dict(showgrid=False, title=None),
                showlegend=False,
                height=max(150, len(type_dist) * 40)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Type badges
            badge_html = ""
            type_classes = {
                'Household Member': 'type-household',
                'Mailslot': 'type-mailslot',
                'Neighbor': 'type-neighbor',
                'Receptionist': 'type-receptionist',
                'Safe Location': 'type-safelocation'
            }
            for t, c in type_dist.items():
                badge_class = type_classes.get(t, '')
                badge_html += f'<span class="type-badge {badge_class}">{t}: {c}</span>'
            st.markdown(f'<div style="margin-top: 8px;">{badge_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Keine Zustellart-Daten verfügbar.")
    # 2. DRIVERS (People-first)
    with tab_drivers:
        searched = st.text_input("Find driver", placeholder="Search ID...", label_visibility="collapsed")
        
        drivers = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_problem(dd)
            drivers.append({'id': did, 'count': len(dd), 'problem': mp})
        
        drivers = sorted(drivers, key=lambda x: x['count'], reverse=True)
        if searched:
            drivers = [d for d in drivers if searched.lower() in d['id'].lower()]
            
        st.markdown(f"<div class='meta-text' style='margin-bottom:16px'>{len(drivers)} drivers found</div>", unsafe_allow_html=True)
        for d in drivers[:20]: # Limit list for performance
            risk_class = "risk-critical" if d['count'] > 10 else "risk-warning" if d['count'] > 5 else "risk-ok"
            risk_label = "Kritisch" if d['count'] > 10 else "Risiko" if d['count'] > 5 else "Beobachten"
            
            # Simple clickable mechanic using columns/buttons
            with st.container():
                c1, c2, c3 = st.columns([4, 2, 1])
                with c1:
                    st.markdown(f"**{d['id']}**<br><span style='font-size:0.8rem; color:#5f6368'>{d['problem']}</span>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<span class='risk-tag {risk_class}'>{risk_label}</span>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"**{d['count']}**", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 8px 0; border:none; border-bottom:1px solid #f1f3f4;'>", unsafe_allow_html=True)
    # 3. INSIGHTS (Trends)
    with tab_insights:
        st.markdown("### Weekly Trend")
        if 'year_week' in df.columns:
            weekly = df.groupby('year_week').size().reset_index(name='count')
            fig = px.bar(weekly, x='year_week', y='count', text='count')
            fig.update_traces(marker_color='#1a73e8', textposition='outside')
            fig.update_layout(
                plot_bgcolor='white',
                margin=dict(t=20, l=0, r=0, b=0),
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None, showticklabels=False),
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Top Zip Codes")
        if 'zip_code' in df.columns:
            top_zips = df['zip_code'].value_counts().head(5)
            for z, c in top_zips.items():
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding: 8px 0; border-bottom:1px solid #f1f3f4;">
                    <span>{z}</span>
                    <span style="font-weight:500;">{c}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # --- MISMATCH DETECTOR ---
        st.markdown("---")
        st.markdown("### 🔍 Mismatch-Erkennung")
        
        mismatches = detect_mailbox_mismatches(df)
        if len(mismatches) > 0:
            # Summary counts
            critical_count = len(mismatches[mismatches['severity'] == 'critical']) if 'severity' in mismatches.columns else 0
            warning_count = len(mismatches[mismatches['severity'] == 'warning']) if 'severity' in mismatches.columns else 0
            
            col1, col2 = st.columns(2)
            with col1:
                if critical_count > 0:
                    st.markdown(f"""
                    <div class="mismatch-card mismatch-critical">
                        <strong>🚨 {critical_count} Kritische Mismatches</strong><br>
                        <span style="font-size: 0.875rem;">Safe Location ohne Foto</span>
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                if warning_count > 0:
                    st.markdown(f"""
                    <div class="mismatch-card">
                        <strong>⚠️ {warning_count} Warnungen</strong><br>
                        <span style="font-size: 0.875rem;">Briefkasten als Household</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with st.expander(f"Alle {len(mismatches)} Mismatches anzeigen"):
                # Group by type
                for mtype in mismatches['mismatch_type'].unique():
                    type_df = mismatches[mismatches['mismatch_type'] == mtype]
                    st.markdown(f"**{mtype}** ({len(type_df)} Fälle)")
                    display_cols = ['transporter_id', 'tracking_id', 'detail']
                    available_cols = [c for c in display_cols if c in type_df.columns]
                    st.dataframe(type_df[available_cols].head(20), use_container_width=True, hide_index=True)
        else:
            st.success("✓ Keine verdächtigen Muster erkannt")
    # 4. ACTIONS (Coaching)
    with tab_actions:
        # Build driver list with details for dropdown
        driver_opts = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_problem(dd)
            cnt = len(dd)
            # Risk status
            if cnt > 10:
                status = "🔴"
                risk = "Kritisch"
            elif cnt > 5:
                status = "🟠"
                risk = "Risiko"
            else:
                status = "🟢"
                risk = "Beobachten"
            driver_opts.append({
                'id': did,
                'count': cnt,
                'problem': mp,
                'status': status,
                'risk': risk,
                'label': f"{status} {did} · {cnt} concessions · {mp}"
            })
        driver_opts = sorted(driver_opts, key=lambda x: x['count'], reverse=True)
        
        # Prominent Driver Selection Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%); color: white; padding: 16px 20px; border-radius: 8px; margin-bottom: 16px;">
            <div style="font-size: 0.75rem; opacity: 0.8; margin-bottom: 4px;">FAHRER FÜR COACHING AUSWÄHLEN</div>
            <div style="font-size: 1rem;">Wähle einen Fahrer aus, um den Maßnahmenplan zu sehen</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Driver Selection with details
        sel_driver = st.selectbox(
            "Select Driver",
            options=[d['id'] for d in driver_opts],
            format_func=lambda x: next((d['label'] for d in driver_opts if d['id'] == x), x),
            label_visibility="collapsed"
        )
        
        if sel_driver:
            dd = df[df['transporter_id'] == sel_driver]
            driver_info = next((d for d in driver_opts if d['id'] == sel_driver), None)
            mp = driver_info['problem'] if driver_info else "Unknown"
            total = driver_info['count'] if driver_info else len(dd)
            status = driver_info['status'] if driver_info else ""
            risk = driver_info['risk'] if driver_info else ""
            
            # Calculate percentile
            rank = next((i+1 for i, d in enumerate(driver_opts) if d['id'] == sel_driver), 1)
            percentile = (rank / len(driver_opts)) * 100
            
            # Get weeks active
            weeks_active = dd['year_week'].nunique() if 'year_week' in dd.columns else 1
            
            # Get top ZIP
            top_zip = ""
            zip_pct = 0
            if 'zip_code' in dd.columns and len(dd) > 0:
                zc = dd['zip_code'].value_counts()
                if len(zc) > 0:
                    top_zip = str(zc.index[0])
                    zip_pct = (zc.iloc[0] / total) * 100
            
            # High value items
            hv_count = int(dd.get('High Value Item (Y/N)', pd.Series([0])).sum()) if 'High Value Item (Y/N)' in dd.columns else 0
            
            # -- Driver Header Card with Risk Status --
            risk_bg = "#fce8e6" if risk == "Critical" else "#ffeec2" if risk == "At Risk" else "#e6f4ea"
            risk_color = "#c5221f" if risk == "Critical" else "#b06000" if risk == "At Risk" else "#137333"
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #dadce0; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 500; color: #202124; margin-bottom: 4px;">{status} {sel_driver}</div>
                        <div style="font-size: 0.875rem; color: #5f6368;">Top {percentile:.0f}% Risiko-Fahrer</div>
                    </div>
                    <div style="background: {risk_bg}; color: {risk_color}; padding: 6px 12px; border-radius: 16px; font-size: 0.75rem; font-weight: 500;">
                        {risk}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; text-align: center;">
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 500; color: #202124;">{total}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">Concessions</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 500; color: #202124;">{weeks_active}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">Wochen aktiv</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 500; color: #1a73e8;">{mp}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">#1 Problem</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 500; color: {'#c5221f' if hv_count > 0 else '#202124'};">{hv_count if hv_count > 0 else '—'}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">High Value</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ZIP Warning if significant
            if top_zip and zip_pct > 40:
                st.markdown(f"""
                <div style="background: #fef7e0; border-left: 4px solid #f9ab00; padding: 12px 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                    <strong>📍 Standort-Muster:</strong> {zip_pct:.0f}% der Probleme aus PLZ {top_zip}
                </div>
                """, unsafe_allow_html=True)
            
            # -- Internal Tabs --
            subtab_coach, subtab_details, subtab_history = st.tabs(["Maßnahmenplan", "Analyse", "Verlauf"])
            
            with subtab_coach:
                # Enhanced 5-Step Coaching
                
                # Get problem counts for details
                _, counts = get_driver_problem(dd)
                
                # Build week string
                try:
                    weeks = sorted([str(w) for w in dd['year_week'].unique()])
                    week_str = f"{weeks[0]} to {weeks[-1]}" if weeks else "recent period"
                except:
                    week_str = "recent period"
                
                st.markdown("### Coaching-Skript")
                
                # 1. Observation (Fact)
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-size: 0.7rem; color: #5f6368; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">1. FESTSTELLUNG</div>
                    <div style="font-size: 1rem; color: #202124; line-height: 1.6;">
                        Im Zeitraum <strong>{week_str}</strong> hattest du <strong>{total} Concessions</strong>.
                        Dein Hauptproblem ist <strong>{mp}</strong> ({int(max(counts.values()) if counts else 0)} Fälle).
                        {f'Zusätzlich: {zip_pct:.0f}% der Fälle in PLZ {top_zip}.' if top_zip and zip_pct > 30 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Specific Behavior
                if "Household" in mp:
                    behavior = f"Du hast {int(counts.get('Household', 0))} Pakete als 'Haushaltsmitglied' markiert, ohne persönliche Übergabe. Das passiert, wenn du Household wählst, aber das Paket nicht persönlich übergibst."
                elif "Geo" in mp:
                    behavior = f"Das System hat {int(counts.get('Geo >25m', 0))} Scans erkannt, bei denen GPS >25 Meter von der Lieferadresse entfernt war. Das passiert meist, wenn du im Fahrzeug scannst, bevor du zur Tür gehst."
                elif "Kein Foto" in mp:
                    behavior = f"Du hattest {int(counts.get('Kein Foto', 0))} unbeaufsichtigte Zustellungen ohne Foto. Ohne Fotobeweis können Kunden leicht Nicht-Zustellung behaupten."
                elif "False Scan" in mp:
                    behavior = f"Das System hat {int(counts.get('False Scan', 0))} Scans als verdächtig markiert. GPS zeigt, dass du nicht am Zustellort warst, als gescannt wurde."
                elif "Lieferpräferenz" in mp:
                    behavior = f"Bei {int(counts.get('Lieferpräferenz', 0))} Zustellungen wurden Kundenpräferenzen nicht beachtet. Kunden hinterlegen spezifische Wünsche, die du befolgen musst."
                else:
                    behavior = "Mehrere Compliance-Probleme in verschiedenen Kategorien erkannt."
                
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-size: 0.7rem; color: #5f6368; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">2. ERKANNTES VERHALTEN</div>
                    <div style="font-size: 1rem; color: #202124; line-height: 1.6;">{behavior}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. Impact/Risk
                if risk == "Kritisch":
                    impact = f"Du bist in den <strong>Top {percentile:.0f}%</strong> der Fahrer nach Concession-Volumen. Dieses Muster löst automatische Überprüfung aus. Ohne sofortige Verbesserung folgen: Routen-Neuzuweisung oder Ride-Along-Begleitung."
                elif risk == "Risiko":
                    impact = f"Du bewegst dich auf kritischen Status zu. Wenn das aktuelle Muster 2 weitere Wochen anhält, erfolgt automatische Eskalation an den Manager."
                else:
                    impact = "Noch nicht kritisch, aber proaktives Handeln verhindert zukünftige Eskalation."
                
                st.markdown(f"""
                <div style="background: #fce8e6; padding: 16px; border-radius: 8px; margin-bottom: 16px; border-left: 4px solid #c5221f;">
                    <div style="font-size: 0.7rem; color: #c5221f; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">3. AUSWIRKUNG</div>
                    <div style="font-size: 1rem; color: #202124; line-height: 1.6;">{impact}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 4. Required Actions
                if "Household" in mp:
                    actions = ["✅ 'Haushaltsmitglied' NUR bei persönlicher Übergabe wählen",
                              "✅ Wenn niemand öffnet: Safe Location + Foto machen",
                              "❌ Niemals Household für abgelegte Pakete nutzen"]
                elif "Geo" in mp:
                    actions = ["✅ Zur Tür gehen BEVOR du scannst",
                              "✅ Bei Group Stops: Jedes Paket an seiner Tür scannen",
                              "❌ Niemals im Fahrzeug scannen"]
                elif "Kein Foto" in mp:
                    actions = ["✅ Klares Foto mit Paket und Tür/Adresse machen",
                              "✅ Foto ist PFLICHT bei allen unbeaufsichtigten Zustellungen",
                              "❌ Niemals ohne Fotobeweis als zugestellt markieren"]
                elif "False Scan" in mp:
                    actions = ["✅ Nur scannen, wenn du physisch am Zustellort bist",
                              "✅ Bei GPS-Problemen sofort melden",
                              "⚠️ False Scans können zur sofortigen Kündigung führen"]
                elif "Lieferpräferenz" in mp:
                    actions = ["✅ Kundenpräferenzen VOR jeder Zustellung lesen",
                              "✅ Ablageort und Anweisungen genau befolgen",
                              "❌ Niemals Präferenzen ignorieren"]
                else:
                    actions = ["✅ Alle Standard-Lieferverfahren befolgen",
                              "✅ Bei Unsicherheit: 'Nicht zustellbar' wählen",
                              "✅ Dispatcher fragen wenn unklar"]
                
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-size: 0.7rem; color: #5f6368; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">4. ERFORDERLICHE MASSNAHMEN</div>
                    <div style="font-size: 1rem; color: #202124; line-height: 1.8;">
                        {'<br>'.join(actions)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: #e6f4ea; padding: 16px; border-radius: 8px; margin-bottom: 16px; border: 2px solid #34a853;">
                    <div style="font-size: 0.7rem; color: #137333; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">5. VERPFLICHTUNG</div>
                </div>
                """, unsafe_allow_html=True)
                
                commitment_text = f"Ich verstehe das Problem mit {mp} und verpflichte mich, ab heute das korrekte Verfahren zu befolgen."
                st.markdown(f"**Erklärung:** *\"{commitment_text}\"*")
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Fahrer bestätigt", use_container_width=True):
                        st.success("✓ Verpflichtung erfasst")
                with col_btn2:
                    protocol = f"""COACHING-PROTOKOLL
═══════════════════════════════════
Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Fahrer: {sel_driver}
Status: {status} {risk} (Top {percentile:.0f}%)
Zeitraum: {week_str}
KENNZAHLEN
───────
Concessions: {total}
#1 Problem: {mp}
Top PLZ: {top_zip} ({zip_pct:.0f}%)
COACHING-PUNKTE
───────────────
1. FESTSTELLUNG
{total} Concessions mit Hauptproblem: {mp}
2. VERHALTEN
{behavior}
3. AUSWIRKUNG
{"Kritisch - sofortiges Handeln erforderlich" if risk == "Kritisch" else "Risiko - Verbesserung nötig" if risk == "Risiko" else "Beobachtungsstatus"}
4. MASSNAHMEN
{chr(10).join(actions)}
5. VERPFLICHTUNG
"{commitment_text}"
UNTERSCHRIFTEN
───────────
Fahrer: _________________________ Datum: _________
Manager: ________________________ Datum: _________
"""
                    st.download_button("📥 Protokoll herunterladen", protocol, f"coaching_{sel_driver[:10]}.txt", use_container_width=True)
            
            with subtab_details:
                st.markdown("### Problemaufschlüsselung")
                
                # Problem breakdown
                breakdown = []
                for col, label in [
                    ('Geo Distance > 25m', 'Geo-Verstoß'),
                    ('Delivered to Household Member / Customer', 'Household-Problem'),
                    ('Delivery preferences not followed', 'Lieferpräferenz nicht eingehalten'),
                    ('Unattended Delivery & No Photo on Delivery', 'Kein Foto'),
                    ('Feedback False Scan Indicator', 'False Scan')
                ]:
                    if col in dd.columns:
                        cnt = int(dd[col].sum())
                        if cnt > 0:
                            breakdown.append({'Issue': label, 'Count': cnt, '%': f"{(cnt/total)*100:.0f}%"})
                
                if breakdown:
                    st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)
                
                # ZIP breakdown
                st.markdown("### PLZ-Analyse")
                if 'zip_code' in dd.columns:
                    zc = dd['zip_code'].value_counts().head(5)
                    for z, c in zc.items():
                        pct = (c / total) * 100
                        st.markdown(f"**{z}**: {c} Fälle ({pct:.0f}%)")
                
                # --- TIME ANALYSIS ---
                st.markdown("### ⏰ Zeitanalyse")
                time_data = get_time_analysis(df, sel_driver)
                
                if time_data['peak_hour'] or time_data['peak_day']:
                    st.markdown(f"""
                    <div class="time-card">
                        <div class="time-stat">
                            <div class="time-stat-value">{time_data['peak_hour'] or '—'}</div>
                            <div class="time-stat-label">Peak-Stunde ({time_data['peak_hour_pct']:.0f}%)</div>
                        </div>
                        <div class="time-stat">
                            <div class="time-stat-value">{time_data['peak_day'] or '—'}</div>
                            <div class="time-stat-label">Risiko-Tag ({time_data['peak_day_pct']:.0f}%)</div>
                        </div>
                        <div class="time-stat">
                            <div class="time-stat-value">{time_data['days_since_last'] if time_data['days_since_last'] is not None else '—'}</div>
                            <div class="time-stat-label">Tage seit letztem</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hourly distribution chart if data exists
                    if time_data['hourly_dist']:
                        hourly_df = pd.DataFrame([
                            {'Stunde': f"{h:02d}:00", 'Anzahl': c} 
                            for h, c in sorted(time_data['hourly_dist'].items())
                        ])
                        fig = px.bar(hourly_df, x='Stunde', y='Anzahl', text='Anzahl')
                        fig.update_traces(marker_color='#1a73e8', textposition='outside')
                        fig.update_layout(
                            plot_bgcolor='white', height=180,
                            margin=dict(t=10, l=0, r=0, b=0),
                            xaxis=dict(showgrid=False, title=None),
                            yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None, showticklabels=False)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Keine Zeitstempel-Daten verfügbar für Zeitanalyse.")
                
                # Weekly trend
                st.markdown("### Wöchentlicher Verlauf")
                if 'year_week' in dd.columns:
                    weekly = dd.groupby('year_week').size().reset_index(name='count')
                    fig = px.bar(weekly, x='year_week', y='count', text='count')
                    fig.update_traces(marker_color='#1a73e8', textposition='outside')
                    fig.update_layout(
                        plot_bgcolor='white', height=200,
                        margin=dict(t=10, l=0, r=0, b=0),
                        xaxis=dict(showgrid=False, title=None),
                        yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with subtab_history:
                cols_to_show = ['year_week', 'tracking_id', 'zip_code']
                if 'Concession Cost' in dd.columns:
                    cols_to_show.append('Concession Cost')
                st.dataframe(dd[cols_to_show], use_container_width=True, hide_index=True)
if __name__ == "__main__":
    main()
