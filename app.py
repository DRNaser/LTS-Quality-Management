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
        
        # Y/N to Numeric - expanded list
        yn_cols = ['High Value Item (Y/N)', 'High Value Item', 'Feedback False Scan Indicator', 
                   'Attended DNR Deliveries', 'Mailbox Eligible, Delivered Elsewhere',
                   'pod_eligible', 'PHR Honoured', 'No Photo On Delivery', 'Photo On Delivery',
                   'Successful Contact Opportunity', 'Unsuccessful Contact Opportunity']
        for col in yn_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: 1 if str(x).upper().strip() in ['Y', 'YES', '1', 'TRUE'] else 0)
        
        # Numeric Conversion - expanded list
        num_cols = ['Concession Cost', 'Geo Distance > 25m', 'Delivered to Household Member / Customer',
                    'Delivery preferences not followed', 'Unattended Delivery & No Photo on Delivery',
                    'Delivered to Neighbour', 'Delivered to Maislot', 'Delivered to Receptionist',
                    'Simultaneous Group Stops', 'Multiple Concessions Reasons',
                    'Package Length', 'Package Height', 'Package Width',
                    'geo_dist', 'total_call_duration_seconds', 'call_event', 'text_event']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Parse date columns
        date_cols = ['delivery_date_time', 'dnr_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
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
    
    # Find timestamp column - prioritize delivery_date_time and dnr_date
    time_cols = ['delivery_date_time', 'dnr_date', 'shipment_delivered_date', 'shipment_created_timestamp', 
                 'delivered_date', 'delivery_timestamp', 'created_at', 'timestamp']
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
# Mailbox max dimension in cm (standard German mailbox slot)
MAILBOX_MAX_CM = 2.5
def detect_oversized_mailbox_packages(df):
    """Detect mailbox misbookings:
    1. Packages >2.5cm marked as mailslot (too large)
    2. Packages ≤2.5cm marked as Household (should be Briefkasten)
    3. Mailbox Eligible, Delivered Elsewhere flag
    """
    mismatches = []
    
    # Check if we have the required columns
    has_dimensions = all(col in df.columns for col in ['Package Height', 'Package Width'])
    has_mailslot = 'Delivered to Maislot' in df.columns
    has_household = 'Delivered to Household Member / Customer' in df.columns
    has_mailbox_elsewhere = 'Mailbox Eligible, Delivered Elsewhere' in df.columns
    
    if has_dimensions:
        for idx, row in df.iterrows():
            height = row.get('Package Height', 0)
            width = row.get('Package Width', 0)
            
            # Package fits in mailbox if BOTH height AND width ≤ 2.5cm
            fits_mailbox = (height <= MAILBOX_MAX_CM) and (width <= MAILBOX_MAX_CM) and (height > 0) and (width > 0)
            
            # Package is too large for mailbox
            is_oversized = (height > MAILBOX_MAX_CM) or (width > MAILBOX_MAX_CM)
            
            # Check flags
            is_mailslot = row.get('Delivered to Maislot', 0) == 1 if has_mailslot else False
            is_household = row.get('Delivered to Household Member / Customer', 0) == 1 if has_household else False
            
            # Type 1: Oversized package marked as mailslot
            if is_mailslot and is_oversized:
                mismatches.append({
                    'tracking_id': row.get('tracking_id', 'Unknown'),
                    'transporter_id': row.get('transporter_id', 'Unknown'),
                    'height_cm': height,
                    'width_cm': width,
                    'length_cm': row.get('Package Length', 0),
                    'zip_code': row.get('zip_code', 'Unknown'),
                    'mismatch_type': 'Übergroß für Briefkasten',
                    'severity': 'critical',
                    'detail': f'{height}x{width}cm > {MAILBOX_MAX_CM}cm'
                })
            
            # Type 2: Small package (fits mailbox) but booked as Household
            if fits_mailbox and is_household and not is_mailslot:
                mismatches.append({
                    'tracking_id': row.get('tracking_id', 'Unknown'),
                    'transporter_id': row.get('transporter_id', 'Unknown'),
                    'height_cm': height,
                    'width_cm': width,
                    'length_cm': row.get('Package Length', 0),
                    'zip_code': row.get('zip_code', 'Unknown'),
                    'mismatch_type': 'Briefkasten-fähig als Household',
                    'severity': 'warning',
                    'detail': f'{height}x{width}cm passt in Briefkasten'
                })
    
    # Type 3: Existing flag for Mailbox Eligible, Delivered Elsewhere
    if has_mailbox_elsewhere:
        elsewhere_df = df[df['Mailbox Eligible, Delivered Elsewhere'] == 1]
        for idx, row in elsewhere_df.iterrows():
            # Avoid duplicates - only add if not already flagged
            tracking = row.get('tracking_id', 'Unknown')
            if not any(m['tracking_id'] == tracking for m in mismatches):
                mismatches.append({
                    'tracking_id': tracking,
                    'transporter_id': row.get('transporter_id', 'Unknown'),
                    'height_cm': row.get('Package Height', 0),
                    'width_cm': row.get('Package Width', 0),
                    'length_cm': row.get('Package Length', 0),
                    'zip_code': row.get('zip_code', 'Unknown'),
                    'mismatch_type': 'Briefkasten-fähig, woanders zugestellt',
                    'severity': 'warning',
                    'detail': 'System-Flag'
                })
    
    return pd.DataFrame(mismatches) if mismatches else pd.DataFrame()
def get_driver_enhanced_stats(df, driver_id):
    """Get enhanced stats for a driver including cost, trend, repeat offender status."""
    dd = df[df['transporter_id'] == driver_id]
    
    stats = {
        'total_cost': 0,
        'avg_cost': 0,
        'trend_direction': '→',  # ↑ ↓ →
        'trend_change': 0,
        'is_repeat_offender': False,
        'consecutive_weeks': 0,
        'dimension_misbookings': 0,
        'contact_attempts': 0,
        'contact_success_rate': 0,
        'avg_geo_distance': 0,
        'delivery_types': {}
    }
    
    if len(dd) == 0:
        return stats
    
    # Cost analysis
    if 'Concession Cost' in dd.columns:
        stats['total_cost'] = dd['Concession Cost'].sum()
        stats['avg_cost'] = dd['Concession Cost'].mean()
    
    # Trend analysis (week-over-week)
    if 'year_week' in dd.columns:
        weekly = dd.groupby('year_week').size().sort_index()
        if len(weekly) >= 2:
            last_week = weekly.iloc[-1]
            prev_week = weekly.iloc[-2]
            change = last_week - prev_week
            stats['trend_change'] = change
            if change > 0:
                stats['trend_direction'] = '↑'
            elif change < 0:
                stats['trend_direction'] = '↓'
        
        # Repeat offender: issues in 3+ consecutive weeks
        stats['consecutive_weeks'] = len(weekly)
        if len(weekly) >= 3:
            stats['is_repeat_offender'] = True
    
    # Dimension misbookings
    if 'Delivered to Maislot' in dd.columns and 'Package Height' in dd.columns:
        mailslot = dd[dd['Delivered to Maislot'] == 1]
        oversized = mailslot[(mailslot['Package Height'] > MAILBOX_MAX_CM) | (mailslot['Package Width'] > MAILBOX_MAX_CM)]
        stats['dimension_misbookings'] = len(oversized)
    
    if 'Mailbox Eligible, Delivered Elsewhere' in dd.columns:
        stats['dimension_misbookings'] += int(dd['Mailbox Eligible, Delivered Elsewhere'].sum())
    
    # Contact attempts
    if 'call_event' in dd.columns:
        stats['contact_attempts'] = int(dd['call_event'].sum())
    if 'Successful Contact Opportunity' in dd.columns and 'Unsuccessful Contact Opportunity' in dd.columns:
        success = dd['Successful Contact Opportunity'].sum()
        total = success + dd['Unsuccessful Contact Opportunity'].sum()
        if total > 0:
            stats['contact_success_rate'] = (success / total) * 100
    
    # Geo distance
    if 'geo_dist' in dd.columns:
        stats['avg_geo_distance'] = dd['geo_dist'].mean()
    
    # Delivery types breakdown
    type_cols = {
        'Household': 'Delivered to Household Member / Customer',
        'Nachbar': 'Delivered to Neighbour',
        'Briefkasten': 'Delivered to Maislot',
        'Rezeption': 'Delivered to Receptionist'
    }
    for label, col in type_cols.items():
        if col in dd.columns:
            count = int(dd[col].sum())
            if count > 0:
                stats['delivery_types'][label] = count
    
    return stats
def get_zip_risk_scores(df):
    """Calculate risk scores for ZIP codes based on issue density."""
    if 'zip_code' not in df.columns:
        return []
    
    zip_stats = []
    for zip_code in df['zip_code'].unique():
        zd = df[df['zip_code'] == zip_code]
        count = len(zd)
        
        # Calculate issue counts
        issues = 0
        if 'Geo Distance > 25m' in zd.columns:
            issues += zd['Geo Distance > 25m'].sum()
        if 'Unattended Delivery & No Photo on Delivery' in zd.columns:
            issues += zd['Unattended Delivery & No Photo on Delivery'].sum()
        if 'Delivery preferences not followed' in zd.columns:
            issues += zd['Delivery preferences not followed'].sum()
        
        # Cost
        cost = zd['Concession Cost'].sum() if 'Concession Cost' in zd.columns else 0
        
        # Risk score (0-100)
        risk_score = min(100, (issues / count * 50) + (count / 10)) if count > 0 else 0
        
        zip_stats.append({
            'zip_code': zip_code,
            'count': count,
            'issues': int(issues),
            'cost': cost,
            'risk_score': round(risk_score, 1)
        })
    
    return sorted(zip_stats, key=lambda x: x['risk_score'], reverse=True)[:10]
def get_week_comparison(df):
    """Compare current week vs previous week."""
    if 'year_week' not in df.columns:
        return None
    
    weeks = sorted(df['year_week'].unique())
    if len(weeks) < 2:
        return None
    
    current_week = weeks[-1]
    prev_week = weeks[-2]
    
    curr_df = df[df['year_week'] == current_week]
    prev_df = df[df['year_week'] == prev_week]
    
    return {
        'current_week': current_week,
        'prev_week': prev_week,
        'current_count': len(curr_df),
        'prev_count': len(prev_df),
        'change': len(curr_df) - len(prev_df),
        'change_pct': ((len(curr_df) - len(prev_df)) / len(prev_df) * 100) if len(prev_df) > 0 else 0,
        'current_cost': curr_df['Concession Cost'].sum() if 'Concession Cost' in curr_df.columns else 0,
        'prev_cost': prev_df['Concession Cost'].sum() if 'Concession Cost' in prev_df.columns else 0
    }
# ============================================================================
# EXTENDED ANALYTICS FUNCTIONS
# ============================================================================
def get_delivery_type_mismatches(df):
    """Compare actual_delivery_type vs promised_delivery_type."""
    mismatches = []
    
    if 'actual_delivery_type' not in df.columns or 'promised_delivery_type' not in df.columns:
        return pd.DataFrame()
    
    for idx, row in df.iterrows():
        actual = str(row.get('actual_delivery_type', '')).strip()
        promised = str(row.get('promised_delivery_type', '')).strip()
        
        if actual and promised and actual.lower() != promised.lower():
            mismatches.append({
                'tracking_id': row.get('tracking_id', 'Unknown'),
                'transporter_id': row.get('transporter_id', 'Unknown'),
                'promised': promised,
                'actual': actual,
                'zip_code': row.get('zip_code', 'Unknown'),
                'cost': row.get('Concession Cost', 0)
            })
    
    return pd.DataFrame(mismatches) if mismatches else pd.DataFrame()
def get_contact_analysis(df):
    """Analyze contact attempts and success rates."""
    result = {
        'total_calls': 0,
        'total_texts': 0,
        'successful_contacts': 0,
        'unsuccessful_contacts': 0,
        'success_rate': 0,
        'avg_call_duration': 0,
        'no_contact_count': 0,
        'by_driver': []
    }
    
    if 'call_event' in df.columns:
        result['total_calls'] = int(df['call_event'].sum())
    if 'text_event' in df.columns:
        result['total_texts'] = int(df['text_event'].sum())
    if 'Successful Contact Opportunity' in df.columns:
        result['successful_contacts'] = int(df['Successful Contact Opportunity'].sum())
    if 'Unsuccessful Contact Opportunity' in df.columns:
        result['unsuccessful_contacts'] = int(df['Unsuccessful Contact Opportunity'].sum())
    
    total_contacts = result['successful_contacts'] + result['unsuccessful_contacts']
    if total_contacts > 0:
        result['success_rate'] = (result['successful_contacts'] / total_contacts) * 100
    
    if 'total_call_duration_seconds' in df.columns:
        calls_with_duration = df[df['total_call_duration_seconds'] > 0]
        if len(calls_with_duration) > 0:
            result['avg_call_duration'] = calls_with_duration['total_call_duration_seconds'].mean()
    
    # No contact attempts
    if 'call_event' in df.columns and 'text_event' in df.columns:
        no_contact = df[(df['call_event'] == 0) & (df['text_event'] == 0)]
        result['no_contact_count'] = len(no_contact)
    
    # By driver
    if 'transporter_id' in df.columns:
        for driver in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == driver]
            calls = int(dd['call_event'].sum()) if 'call_event' in dd.columns else 0
            success = int(dd['Successful Contact Opportunity'].sum()) if 'Successful Contact Opportunity' in dd.columns else 0
            total = success + (int(dd['Unsuccessful Contact Opportunity'].sum()) if 'Unsuccessful Contact Opportunity' in dd.columns else 0)
            rate = (success / total * 100) if total > 0 else 0
            
            if calls > 0 or total > 0:
                result['by_driver'].append({
                    'driver': driver,
                    'calls': calls,
                    'success_rate': round(rate, 1)
                })
        
        result['by_driver'] = sorted(result['by_driver'], key=lambda x: x['success_rate'])[:10]
    
    return result
def get_photo_compliance(df):
    """Analyze photo compliance rates."""
    result = {
        'with_photo': 0,
        'without_photo': 0,
        'pod_eligible': 0,
        'pod_missing': 0,
        'compliance_rate': 0,
        'by_driver': []
    }
    
    if 'Photo On Delivery' in df.columns:
        result['with_photo'] = int(df['Photo On Delivery'].sum())
    if 'No Photo On Delivery' in df.columns:
        result['without_photo'] = int(df['No Photo On Delivery'].sum())
    if 'pod_eligible' in df.columns:
        result['pod_eligible'] = int(df['pod_eligible'].sum())
    
    # POD missing = pod_eligible but no photo
    if 'pod_eligible' in df.columns and 'Photo On Delivery' in df.columns:
        pod_required = df[df['pod_eligible'] == 1]
        pod_missing = pod_required[pod_required['Photo On Delivery'] == 0]
        result['pod_missing'] = len(pod_missing)
    
    total = result['with_photo'] + result['without_photo']
    if total > 0:
        result['compliance_rate'] = (result['with_photo'] / total) * 100
    
    # By driver
    if 'transporter_id' in df.columns and 'Photo On Delivery' in df.columns:
        for driver in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == driver]
            with_photo = int(dd['Photo On Delivery'].sum()) if 'Photo On Delivery' in dd.columns else 0
            without_photo = int(dd['No Photo On Delivery'].sum()) if 'No Photo On Delivery' in dd.columns else 0
            total = with_photo + without_photo
            rate = (with_photo / total * 100) if total > 0 else 100
            
            if without_photo > 0:
                result['by_driver'].append({
                    'driver': driver,
                    'missing': without_photo,
                    'rate': round(rate, 1)
                })
        
        result['by_driver'] = sorted(result['by_driver'], key=lambda x: x['missing'], reverse=True)[:10]
    
    return result
def get_group_stop_analysis(df):
    """Analyze correlation between group stops and issues."""
    result = {
        'total_group_stops': 0,
        'group_stop_concessions': 0,
        'non_group_concessions': 0,
        'group_stop_rate': 0,
        'correlation': 'Keine Daten'
    }
    
    if 'Simultaneous Group Stops' not in df.columns:
        return result
    
    group_stops = df[df['Simultaneous Group Stops'] > 0]
    non_group = df[df['Simultaneous Group Stops'] == 0]
    
    result['total_group_stops'] = int(df['Simultaneous Group Stops'].sum())
    result['group_stop_concessions'] = len(group_stops)
    result['non_group_concessions'] = len(non_group)
    
    if len(df) > 0:
        result['group_stop_rate'] = (len(group_stops) / len(df)) * 100
    
    # Simple correlation indicator
    if result['group_stop_rate'] > 30:
        result['correlation'] = '⚠️ Hoch - Group Stops korrelieren mit Concessions'
    elif result['group_stop_rate'] > 15:
        result['correlation'] = '📊 Mittel - Einige Korrelation sichtbar'
    else:
        result['correlation'] = '✅ Niedrig - Kaum Zusammenhang'
    
    return result
def get_phr_analysis(df):
    """Analyze Preference Honoured Rate."""
    result = {
        'total_with_pref': 0,
        'phr_honoured': 0,
        'phr_not_honoured': 0,
        'honour_rate': 0,
        'by_driver': []
    }
    
    if 'PHR Honoured' not in df.columns:
        return result
    
    result['phr_honoured'] = int(df['PHR Honoured'].sum())
    result['total_with_pref'] = len(df)  # Assuming all rows have preferences
    result['phr_not_honoured'] = result['total_with_pref'] - result['phr_honoured']
    
    if result['total_with_pref'] > 0:
        result['honour_rate'] = (result['phr_honoured'] / result['total_with_pref']) * 100
    
    # By driver
    if 'transporter_id' in df.columns:
        for driver in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == driver]
            honoured = int(dd['PHR Honoured'].sum())
            total = len(dd)
            rate = (honoured / total * 100) if total > 0 else 0
            not_honoured = total - honoured
            
            if not_honoured > 0:
                result['by_driver'].append({
                    'driver': driver,
                    'not_honoured': not_honoured,
                    'rate': round(rate, 1)
                })
        
        result['by_driver'] = sorted(result['by_driver'], key=lambda x: x['not_honoured'], reverse=True)[:10]
    
    return result
def get_reason_code_analysis(df):
    """Parse and analyze reason codes."""
    result = {
        'app_reasons': {},
        'shipment_reasons': {},
        'top_combinations': []
    }
    
    if 'app_presented_reason_codes' in df.columns:
        reasons = df['app_presented_reason_codes'].dropna()
        for r in reasons:
            r_str = str(r).strip()
            if r_str and r_str.lower() != 'nan':
                result['app_reasons'][r_str] = result['app_reasons'].get(r_str, 0) + 1
        result['app_reasons'] = dict(sorted(result['app_reasons'].items(), key=lambda x: x[1], reverse=True)[:10])
    
    if 'shipment_reason' in df.columns:
        reasons = df['shipment_reason'].dropna()
        for r in reasons:
            r_str = str(r).strip()
            if r_str and r_str.lower() != 'nan':
                result['shipment_reasons'][r_str] = result['shipment_reasons'].get(r_str, 0) + 1
        result['shipment_reasons'] = dict(sorted(result['shipment_reasons'].items(), key=lambda x: x[1], reverse=True)[:10])
    
    return result
def get_geo_distance_distribution(df):
    """Get distribution of actual geo distances."""
    result = {
        'avg_distance': 0,
        'max_distance': 0,
        'over_25m': 0,
        'over_50m': 0,
        'over_100m': 0,
        'distribution': []
    }
    
    if 'geo_dist' not in df.columns:
        return result
    
    geo = df['geo_dist'].dropna()
    if len(geo) == 0:
        return result
    
    result['avg_distance'] = round(geo.mean(), 1)
    result['max_distance'] = round(geo.max(), 1)
    result['over_25m'] = int((geo > 25).sum())
    result['over_50m'] = int((geo > 50).sum())
    result['over_100m'] = int((geo > 100).sum())
    
    # Distribution buckets
    buckets = [(0, 10), (10, 25), (25, 50), (50, 100), (100, float('inf'))]
    labels = ['0-10m', '10-25m', '25-50m', '50-100m', '>100m']
    
    for (low, high), label in zip(buckets, labels):
        count = int(((geo >= low) & (geo < high)).sum())
        result['distribution'].append({'range': label, 'count': count})
    
    return result
def get_multi_issue_drivers(df):
    """Identify drivers with multiple concurrent issues."""
    result = []
    
    if 'Multiple Concessions Reasons' not in df.columns:
        return result
    
    multi = df[df['Multiple Concessions Reasons'] > 0]
    
    if 'transporter_id' in multi.columns:
        driver_counts = multi.groupby('transporter_id').size().sort_values(ascending=False)
        
        for driver, count in driver_counts.head(10).items():
            dd = multi[multi['transporter_id'] == driver]
            cost = dd['Concession Cost'].sum() if 'Concession Cost' in dd.columns else 0
            result.append({
                'driver': driver,
                'multi_issues': int(count),
                'cost': cost
            })
    
    return result
def get_executive_summary(df):
    """Generate executive summary with pattern recognition and key insights."""
    summary = {
        'total_concessions': len(df),
        'total_cost': df['Concession Cost'].sum() if 'Concession Cost' in df.columns else 0,
        'total_drivers': df['transporter_id'].nunique() if 'transporter_id' in df.columns else 0,
        'avg_per_driver': 0,
        'top_issue': None,
        'top_issue_count': 0,
        'critical_drivers': 0,
        'patterns': [],
        'recommendations': [],
        'time_patterns': {},
        'risk_score': 0
    }
    
    if summary['total_drivers'] > 0:
        summary['avg_per_driver'] = summary['total_concessions'] / summary['total_drivers']
    
    # Identify top issue
    issues = {
        'Geo-Verstoß': df.get('Geo Distance > 25m', pd.Series([0])).sum(),
        'Household': df.get('Delivered to Household Member / Customer', pd.Series([0])).sum(),
        'Lieferpräferenz': df.get('Delivery preferences not followed', pd.Series([0])).sum(),
        'Kein Foto': df.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum(),
        'False Scan': df.get('Feedback False Scan Indicator', pd.Series([0])).sum(),
    }
    if issues:
        top = max(issues.items(), key=lambda x: x[1])
        summary['top_issue'] = top[0]
        summary['top_issue_count'] = int(top[1])
    
    # Critical drivers (>10 concessions)
    if 'transporter_id' in df.columns:
        driver_counts = df.groupby('transporter_id').size()
        summary['critical_drivers'] = int((driver_counts > 10).sum())
    
    # Time patterns
    time_analysis = get_time_analysis(df)
    summary['time_patterns'] = {
        'peak_hour': time_analysis.get('peak_hour'),
        'peak_day': time_analysis.get('peak_day'),
        'peak_hour_pct': time_analysis.get('peak_hour_pct', 0),
        'peak_day_pct': time_analysis.get('peak_day_pct', 0)
    }
    
    # Pattern Recognition
    patterns = []
    
    # Pattern 1: Time concentration
    if summary['time_patterns']['peak_hour_pct'] > 25:
        patterns.append(f"⏰ {summary['time_patterns']['peak_hour_pct']:.0f}% der Concessions in Peak-Stunde ({summary['time_patterns']['peak_hour']})")
    
    # Pattern 2: Day concentration
    if summary['time_patterns']['peak_day_pct'] > 25:
        patterns.append(f"📅 {summary['time_patterns']['peak_day_pct']:.0f}% der Concessions am {summary['time_patterns']['peak_day']}")
    
    # Pattern 3: Pareto (80/20 rule)
    if 'transporter_id' in df.columns:
        driver_counts = df.groupby('transporter_id').size().sort_values(ascending=False)
        top_20_pct = int(len(driver_counts) * 0.2) or 1
        top_20_concessions = driver_counts.head(top_20_pct).sum()
        pareto_pct = (top_20_concessions / len(df)) * 100 if len(df) > 0 else 0
        if pareto_pct > 60:
            patterns.append(f"📊 Pareto: Top {top_20_pct} Fahrer verursachen {pareto_pct:.0f}% der Concessions")
    
    # Pattern 4: High no-contact rate
    if 'call_event' in df.columns and 'text_event' in df.columns:
        no_contact = len(df[(df['call_event'] == 0) & (df['text_event'] == 0)])
        no_contact_pct = (no_contact / len(df)) * 100 if len(df) > 0 else 0
        if no_contact_pct > 30:
            patterns.append(f"📞 {no_contact_pct:.0f}% ohne Kontaktversuch")
    
    # Pattern 5: Photo compliance issue
    if 'No Photo On Delivery' in df.columns:
        no_photo = int(df['No Photo On Delivery'].sum())
        no_photo_pct = (no_photo / len(df)) * 100 if len(df) > 0 else 0
        if no_photo_pct > 20:
            patterns.append(f"📸 {no_photo_pct:.0f}% ohne Foto-Nachweis")
    
    # Pattern 6: Geo distance issues
    if 'geo_dist' in df.columns:
        high_geo = len(df[df['geo_dist'] > 50])
        high_geo_pct = (high_geo / len(df)) * 100 if len(df) > 0 else 0
        if high_geo_pct > 15:
            patterns.append(f"📍 {high_geo_pct:.0f}% mit Geo-Abstand >50m")
    
    summary['patterns'] = patterns
    
    # Recommendations based on patterns
    recommendations = []
    if summary['top_issue'] == 'Kein Foto':
        recommendations.append("📸 Foto-Schulung für Fahrer empfohlen")
    if summary['top_issue'] == 'Geo-Verstoß':
        recommendations.append("📍 GPS-Genauigkeit prüfen / Schulung zu korrekten Stops")
    if summary['critical_drivers'] > 3:
        recommendations.append(f"🎯 Fokus auf {summary['critical_drivers']} kritische Fahrer")
    if summary['time_patterns']['peak_hour']:
        recommendations.append(f"⏰ Peak-Zeit {summary['time_patterns']['peak_hour']} analysieren")
    
    summary['recommendations'] = recommendations[:4]  # Max 4
    
    # Risk Score (0-100)
    risk = 0
    risk += min(30, summary['critical_drivers'] * 5)  # Max 30 for critical drivers
    risk += min(20, (summary['avg_per_driver'] - 3) * 5) if summary['avg_per_driver'] > 3 else 0
    risk += min(20, len(patterns) * 5)  # Max 20 for patterns
    risk += min(30, (summary['total_cost'] / 1000))  # Max 30 for cost
    summary['risk_score'] = min(100, int(risk))
    
    return summary
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
    tab_overview, tab_drivers, tab_insights, tab_analytics, tab_actions = st.tabs(["Overview", "Drivers", "Insights", "Analytics", "Actions"])
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
                    st.dataframe(pd.DataFrame(hv_table), width='stretch', hide_index=True)
        
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
            st.plotly_chart(fig, width='stretch')
            
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
    # 2. DRIVERS (People-first) - ENHANCED
    with tab_drivers:
        searched = st.text_input("Find driver", placeholder="Search ID...", label_visibility="collapsed")
        
        # Build enhanced driver list
        drivers = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_problem(dd)
            enhanced = get_driver_enhanced_stats(df, did)
            
            drivers.append({
                'id': did, 
                'count': len(dd), 
                'problem': mp,
                'cost': enhanced['total_cost'],
                'trend': enhanced['trend_direction'],
                'trend_change': enhanced['trend_change'],
                'is_repeat': enhanced['is_repeat_offender'],
                'weeks': enhanced['consecutive_weeks'],
                'misbookings': enhanced['dimension_misbookings'],
                'delivery_types': enhanced['delivery_types']
            })
        
        drivers = sorted(drivers, key=lambda x: x['count'], reverse=True)
        if searched:
            drivers = [d for d in drivers if searched.lower() in str(d['id']).lower()]
        
        # Team summary header
        total_drivers = len(drivers)
        critical_count = len([d for d in drivers if d['count'] > 10])
        repeat_count = len([d for d in drivers if d['is_repeat']])
        total_cost = sum(d['cost'] for d in drivers)
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px;">
            <div style="background: var(--gray-50); padding: 12px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 500; color: #202124;">{total_drivers}</div>
                <div style="font-size: 0.75rem; color: #5f6368;">Fahrer gesamt</div>
            </div>
            <div style="background: #fce8e6; padding: 12px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 500; color: #c5221f;">{critical_count}</div>
                <div style="font-size: 0.75rem; color: #c5221f;">Kritisch</div>
            </div>
            <div style="background: #fef7e0; padding: 12px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 500; color: #b06000;">{repeat_count}</div>
                <div style="font-size: 0.75rem; color: #b06000;">Wiederholungstäter</div>
            </div>
            <div style="background: var(--gray-50); padding: 12px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 500; color: #202124;">€{total_cost:,.0f}</div>
                <div style="font-size: 0.75rem; color: #5f6368;">Gesamtkosten</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
        st.markdown(f"<div class='meta-text' style='margin-bottom:16px'>{len(drivers)} Fahrer gefunden</div>", unsafe_allow_html=True)
        
        for d in drivers[:20]:  # Limit list for performance
            risk_class = "risk-critical" if d['count'] > 10 else "risk-warning" if d['count'] > 5 else "risk-ok"
            risk_label = "Kritisch" if d['count'] > 10 else "Risiko" if d['count'] > 5 else "Beobachten"
            
            # Trend color
            trend_color = "#c5221f" if d['trend'] == '↑' else "#137333" if d['trend'] == '↓' else "#5f6368"
            
            # Build badges
            badges = []
            if d['is_repeat']:
                badges.append(f"<span style='background:#fef7e0; color:#b06000; padding:2px 6px; border-radius:4px; font-size:0.7rem; margin-left:4px;'>🔁 {d['weeks']}W</span>")
            if d['misbookings'] > 0:
                badges.append(f"<span style='background:#fce8e6; color:#c5221f; padding:2px 6px; border-radius:4px; font-size:0.7rem; margin-left:4px;'>📦 {int(d['misbookings'])}</span>")
            
            badges_html = ''.join(badges)
            
            # Delivery types breakdown
            types_str = ' · '.join([f"{k}:{v}" for k,v in d['delivery_types'].items()]) if d['delivery_types'] else ""
            
            with st.container():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f3f4;">
                    <div style="flex: 3;">
                        <div style="font-weight: 500; color: #202124;">{d['id']} {badges_html}</div>
                        <div style="font-size: 0.8rem; color: #5f6368;">{d['problem']} {('· ' + types_str) if types_str else ''}</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <span style="color: {trend_color}; font-size: 1.25rem;">{d['trend']}</span>
                        <span style="font-size: 0.75rem; color: #5f6368;">{d['trend_change']:+d}</span>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <span class='risk-tag {risk_class}'>{risk_label}</span>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="font-weight: 500;">{d['count']}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">€{d['cost']:,.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
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
            st.plotly_chart(fig, width='stretch')
        
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
                    st.dataframe(type_df[available_cols].head(20), width='stretch', hide_index=True)
        else:
            st.success("✓ Keine verdächtigen Muster erkannt")
        
        # --- DIMENSION MISBOOKING (NEW) ---
        st.markdown("---")
        st.markdown("### 📦 Briefkasten-Dimension Misbookings")
        st.markdown(f"<div style='font-size: 0.875rem; color: #5f6368; margin-bottom: 12px;'>Pakete ≤2.5cm als Household gebucht (sollten Briefkasten sein)</div>", unsafe_allow_html=True)
        
        # Debug info expander
        with st.expander("🔧 Debug: Daten-Diagnose"):
            st.write("**Vorhandene Spalten:**")
            dim_cols = ['Package Height', 'Package Width', 'Package Length', 
                       'Delivered to Maislot', 'Delivered to Household Member / Customer',
                       'Mailbox Eligible, Delivered Elsewhere']
            for col in dim_cols:
                if col in df.columns:
                    sample_vals = df[col].head(5).tolist()
                    non_zero = (df[col] != 0).sum() if pd.api.types.is_numeric_dtype(df[col]) else len(df[df[col].notna()])
                    st.write(f"✓ `{col}`: {non_zero} non-zero Werte | Sample: {sample_vals}")
                else:
                    st.write(f"✗ `{col}`: **FEHLT**")
            
            # Check actual values
            if 'Package Height' in df.columns and 'Package Width' in df.columns:
                small_packages = df[(df['Package Height'] <= MAILBOX_MAX_CM) & (df['Package Width'] <= MAILBOX_MAX_CM) & (df['Package Height'] > 0) & (df['Package Width'] > 0)]
                st.write(f"**Pakete ≤{MAILBOX_MAX_CM}cm:** {len(small_packages)}")
                
                if 'Delivered to Household Member / Customer' in df.columns:
                    small_as_household = small_packages[small_packages['Delivered to Household Member / Customer'] == 1]
                    st.write(f"**Davon als Household:** {len(small_as_household)}")
        
        dim_mismatches = detect_oversized_mailbox_packages(df)
        if len(dim_mismatches) > 0:
            # Summary by type
            oversized_count = len(dim_mismatches[dim_mismatches['mismatch_type'] == 'Übergroß für Briefkasten']) if 'mismatch_type' in dim_mismatches.columns else 0
            elsewhere_count = len(dim_mismatches[dim_mismatches['mismatch_type'] == 'Briefkasten-fähig, woanders zugestellt']) if 'mismatch_type' in dim_mismatches.columns else 0
            
            col1, col2 = st.columns(2)
            with col1:
                if oversized_count > 0:
                    st.markdown(f"""
                    <div class="mismatch-card mismatch-critical">
                        <strong>🚨 {oversized_count} Übergroße Pakete</strong><br>
                        <span style="font-size: 0.875rem;">Als Briefkasten gebucht, aber >2.5cm</span>
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                if elsewhere_count > 0:
                    st.markdown(f"""
                    <div class="mismatch-card">
                        <strong>⚠️ {elsewhere_count} Briefkasten-fähig</strong><br>
                        <span style="font-size: 0.875rem;">Aber woanders zugestellt</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Top offenders
            if 'transporter_id' in dim_mismatches.columns:
                top_offenders = dim_mismatches['transporter_id'].value_counts().head(5)
                st.markdown("**Top Fahrer mit Dimension-Misbookings:**")
                for driver, count in top_offenders.items():
                    st.markdown(f"• {driver}: **{count}** Fälle")
            
            with st.expander(f"Alle {len(dim_mismatches)} Dimension-Misbookings anzeigen"):
                display_cols = ['transporter_id', 'tracking_id', 'height_cm', 'width_cm', 'mismatch_type']
                available_cols = [c for c in display_cols if c in dim_mismatches.columns]
                st.dataframe(dim_mismatches[available_cols].head(30), width='stretch', hide_index=True)
        else:
            has_dim_data = 'Package Height' in df.columns and 'Package Width' in df.columns
            if has_dim_data:
                st.success("✓ Keine Dimension-Misbookings erkannt")
            else:
                st.info("Keine Paketmaß-Spalten (Package Height/Width) verfügbar")
        
        # --- ZIP RISK SCORES (NEW) ---
        st.markdown("---")
        st.markdown("### 📍 PLZ Risiko-Ranking")
        
        zip_risks = get_zip_risk_scores(df)
        if zip_risks:
            for i, z in enumerate(zip_risks[:5]):
                risk_pct = z['risk_score']
                risk_color = "#c5221f" if risk_pct > 50 else "#b06000" if risk_pct > 25 else "#137333"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f1f3f4;">
                    <div style="flex: 2;">
                        <div style="font-weight: 500;">PLZ {z['zip_code']}</div>
                        <div style="font-size: 0.75rem; color: #5f6368;">{z['count']} Concessions · {z['issues']} Issues</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <span style="font-size: 0.875rem; color: #5f6368;">€{z['cost']:,.0f}</span>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <span style="background: {risk_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">
                            {risk_pct:.0f}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # --- WEEK COMPARISON (NEW) ---
        st.markdown("---")
        st.markdown("### 📈 Woche-zu-Woche Vergleich")
        
        week_comp = get_week_comparison(df)
        if week_comp:
            change_color = "#c5221f" if week_comp['change'] > 0 else "#137333" if week_comp['change'] < 0 else "#5f6368"
            change_icon = "↑" if week_comp['change'] > 0 else "↓" if week_comp['change'] < 0 else "→"
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background: var(--gray-50); padding: 16px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.75rem; color: #5f6368; margin-bottom: 4px;">{week_comp['prev_week']}</div>
                    <div style="font-size: 1.5rem; font-weight: 500;">{week_comp['prev_count']}</div>
                    <div style="font-size: 0.875rem; color: #5f6368;">€{week_comp['prev_cost']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="background: var(--gray-50); padding: 16px; border-radius: 8px; text-align: center; border: 2px solid {change_color};">
                    <div style="font-size: 0.75rem; color: #5f6368; margin-bottom: 4px;">{week_comp['current_week']}</div>
                    <div style="font-size: 1.5rem; font-weight: 500; color: {change_color};">{week_comp['current_count']}</div>
                    <div style="font-size: 0.875rem; color: #5f6368;">€{week_comp['current_cost']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 12px; font-size: 1.25rem; color: {change_color};">
                {change_icon} {week_comp['change']:+d} Concessions ({week_comp['change_pct']:+.1f}%)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Mindestens 2 Wochen Daten benötigt für Vergleich")
    
    # 4. ANALYTICS (Extended Analytics Suite)
    with tab_analytics:
        st.markdown("## 📊 Extended Analytics")
        
        # --- EXECUTIVE SUMMARY ---
        st.markdown("### 🎯 Executive Summary")
        exec_summary = get_executive_summary(df)
        
        # Risk Score Gauge
        risk_color = "#c5221f" if exec_summary['risk_score'] > 60 else "#f9ab00" if exec_summary['risk_score'] > 30 else "#137333"
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, {risk_color}22 0%, {risk_color}11 100%); 
                        border: 3px solid {risk_color}; border-radius: 50%; width: 100px; height: 100px;
                        display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <div style="font-size: 2rem; font-weight: 700; color: {risk_color};">{exec_summary['risk_score']}</div>
                <div style="font-size: 0.7rem; color: {risk_color};">RISIKO</div>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 1.1rem; font-weight: 500; margin-bottom: 8px;">
                    {exec_summary['total_concessions']} Concessions · €{exec_summary['total_cost']:,.0f} · {exec_summary['total_drivers']} Fahrer
                </div>
                <div style="font-size: 0.9rem; color: #5f6368;">
                    Top-Problem: <strong>{exec_summary['top_issue']}</strong> ({exec_summary['top_issue_count']} Fälle) · 
                    Ø {exec_summary['avg_per_driver']:.1f} pro Fahrer · 
                    {exec_summary['critical_drivers']} kritische Fahrer
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Patterns & Recommendations
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🔍 Erkannte Muster:**")
            if exec_summary['patterns']:
                for p in exec_summary['patterns']:
                    st.markdown(f"• {p}")
            else:
                st.info("Keine auffälligen Muster erkannt")
        
        with col2:
            st.markdown("**💡 Empfehlungen:**")
            if exec_summary['recommendations']:
                for r in exec_summary['recommendations']:
                    st.markdown(f"• {r}")
            else:
                st.success("Keine dringenden Maßnahmen erforderlich")
        
        st.markdown("---")
        
        # --- TIME ANALYSIS ---
        st.markdown("### ⏰ Zeitanalyse & Muster")
        time_data = get_time_analysis(df)
        
        if time_data['peak_hour']:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style="background: var(--gray-50); padding: 16px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 500; color: #1a73e8;">{time_data['peak_hour']}</div>
                    <div style="font-size: 0.75rem; color: #5f6368;">Peak-Stunde ({time_data['peak_hour_pct']:.0f}%)</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="background: var(--gray-50); padding: 16px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 500; color: #1a73e8;">{time_data['peak_day'] or 'N/A'}</div>
                    <div style="font-size: 0.75rem; color: #5f6368;">Risiko-Tag ({time_data['peak_day_pct']:.0f}%)</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                days_text = f"{time_data['days_since_last']} Tage" if time_data['days_since_last'] is not None else "N/A"
                st.markdown(f"""
                <div style="background: var(--gray-50); padding: 16px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 500; color: #1a73e8;">{days_text}</div>
                    <div style="font-size: 0.75rem; color: #5f6368;">Seit letztem Vorfall</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Hourly distribution chart
            if time_data['hourly_dist']:
                st.markdown("**Stündliche Verteilung:**")
                hourly_df = pd.DataFrame([
                    {'Stunde': f"{h:02d}:00", 'Anzahl': c} 
                    for h, c in sorted(time_data['hourly_dist'].items())
                ])
                fig = px.bar(hourly_df, x='Stunde', y='Anzahl', text='Anzahl')
                fig.update_traces(marker_color='#1a73e8', textposition='outside')
                fig.update_layout(
                    plot_bgcolor='white', height=200,
                    margin=dict(t=10, l=0, r=0, b=0),
                    xaxis=dict(showgrid=False, title=None, tickangle=-45),
                    yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None)
                )
                st.plotly_chart(fig, width='stretch')
            
            # Daily distribution
            if time_data['daily_dist']:
                st.markdown("**Wochentag-Verteilung:**")
                daily_df = pd.DataFrame([
                    {'Tag': day, 'Anzahl': count} 
                    for day, count in time_data['daily_dist'].items()
                ])
                fig = px.bar(daily_df, x='Tag', y='Anzahl', text='Anzahl')
                fig.update_traces(marker_color='#34a853', textposition='outside')
                fig.update_layout(
                    plot_bgcolor='white', height=180,
                    margin=dict(t=10, l=0, r=0, b=0),
                    xaxis=dict(showgrid=False, title=None),
                    yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None)
                )
                st.plotly_chart(fig, width='stretch')
        else:
            st.info("Keine Zeitstempel-Daten für Analyse verfügbar (delivery_date_time, dnr_date)")
        
        st.markdown("---")
        
        # --- DELIVERY TYPE MISMATCHES ---
        st.markdown("### 🔄 Actual vs Promised Delivery Type")
        type_mismatches = get_delivery_type_mismatches(df)
        if len(type_mismatches) > 0:
            st.markdown(f"""
            <div class="hv-alert">
                <div class="hv-alert-title">⚠️ {len(type_mismatches)} Zustellart-Abweichungen</div>
                <div class="hv-alert-detail">Tatsächliche Zustellart weicht von versprochener ab</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Top mismatches by type
            if 'promised' in type_mismatches.columns and 'actual' in type_mismatches.columns:
                type_mismatches['mismatch'] = type_mismatches['promised'] + ' → ' + type_mismatches['actual']
                top_types = type_mismatches['mismatch'].value_counts().head(5)
                for mtype, count in top_types.items():
                    st.markdown(f"• **{mtype}**: {count} Fälle")
            
            with st.expander("Details anzeigen"):
                st.dataframe(type_mismatches.head(20), width='stretch', hide_index=True)
        else:
            if 'actual_delivery_type' in df.columns:
                st.success("✓ Keine Zustellart-Abweichungen erkannt")
            else:
                st.info("Spalten 'actual_delivery_type' / 'promised_delivery_type' nicht vorhanden")
        
        st.markdown("---")
        
        # --- CONTACT ANALYSIS ---
        st.markdown("### 📞 Kontakt-Analyse")
        contact = get_contact_analysis(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Anrufe", contact['total_calls'])
        with col2:
            st.metric("SMS", contact['total_texts'])
        with col3:
            st.metric("Erfolgsrate", f"{contact['success_rate']:.1f}%")
        with col4:
            st.metric("Ø Dauer", f"{contact['avg_call_duration']:.0f}s")
        
        if contact['no_contact_count'] > 0:
            st.warning(f"⚠️ {contact['no_contact_count']} Concessions ohne jeden Kontaktversuch")
        
        if contact['by_driver']:
            with st.expander("Fahrer mit niedrigster Erfolgsrate"):
                for d in contact['by_driver'][:5]:
                    st.markdown(f"• {d['driver']}: {d['success_rate']:.0f}% ({d['calls']} Anrufe)")
        
        st.markdown("---")
        
        # --- PHOTO COMPLIANCE ---
        st.markdown("### 📸 Foto-Compliance")
        photo = get_photo_compliance(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mit Foto", photo['with_photo'])
        with col2:
            st.metric("Ohne Foto", photo['without_photo'])
        with col3:
            compliance_color = "normal" if photo['compliance_rate'] > 80 else "inverse"
            st.metric("Compliance", f"{photo['compliance_rate']:.1f}%")
        
        if photo['pod_missing'] > 0:
            st.error(f"🚨 {photo['pod_missing']} Fälle: POD erforderlich aber kein Foto")
        
        if photo['by_driver']:
            with st.expander("Fahrer mit meisten fehlenden Fotos"):
                for d in photo['by_driver'][:5]:
                    st.markdown(f"• {d['driver']}: {d['missing']} fehlend ({d['rate']:.0f}% Rate)")
        
        st.markdown("---")
        
        # --- GROUP STOP ANALYSIS ---
        st.markdown("### 🔄 Group Stop Korrelation")
        group = get_group_stop_analysis(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Group Stop Concessions", group['group_stop_concessions'])
        with col2:
            st.metric("Anteil", f"{group['group_stop_rate']:.1f}%")
        
        st.markdown(f"**Korrelation:** {group['correlation']}")
        
        st.markdown("---")
        
        # --- PHR ANALYSIS ---
        st.markdown("### ✅ Präferenz Honoured Rate (PHR)")
        phr = get_phr_analysis(df)
        
        if phr['total_with_pref'] > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Eingehalten", phr['phr_honoured'])
            with col2:
                st.metric("Nicht eingehalten", phr['phr_not_honoured'])
            with col3:
                st.metric("PHR Rate", f"{phr['honour_rate']:.1f}%")
            
            if phr['by_driver']:
                with st.expander("Fahrer mit meisten Präferenz-Verstößen"):
                    for d in phr['by_driver'][:5]:
                        st.markdown(f"• {d['driver']}: {d['not_honoured']} Verstöße ({d['rate']:.0f}% Rate)")
        else:
            st.info("Keine PHR-Daten verfügbar")
        
        st.markdown("---")
        
        # --- REASON CODE ANALYSIS ---
        st.markdown("### 🏷️ Reason Code Analyse")
        reasons = get_reason_code_analysis(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**App Reason Codes:**")
            if reasons['app_reasons']:
                for code, count in list(reasons['app_reasons'].items())[:5]:
                    st.markdown(f"• {code}: **{count}**")
            else:
                st.info("Keine App Reason Codes")
        
        with col2:
            st.markdown("**Shipment Reasons:**")
            if reasons['shipment_reasons']:
                for code, count in list(reasons['shipment_reasons'].items())[:5]:
                    st.markdown(f"• {code}: **{count}**")
            else:
                st.info("Keine Shipment Reasons")
        
        st.markdown("---")
        
        # --- GEO DISTANCE DISTRIBUTION ---
        st.markdown("### 📍 Geo-Distanz Verteilung")
        geo = get_geo_distance_distribution(df)
        
        if geo['distribution']:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ø Distanz", f"{geo['avg_distance']}m")
            with col2:
                st.metric("Max Distanz", f"{geo['max_distance']}m")
            with col3:
                st.metric(">100m", geo['over_100m'])
            
            # Distribution chart
            dist_df = pd.DataFrame(geo['distribution'])
            fig = px.bar(dist_df, x='range', y='count', text='count')
            fig.update_traces(marker_color='#1a73e8', textposition='outside')
            fig.update_layout(
                plot_bgcolor='white', height=200,
                margin=dict(t=10, l=0, r=0, b=0),
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor='#f1f3f4', title=None)
            )
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Keine geo_dist Spalte vorhanden")
        
        st.markdown("---")
        
        # --- MULTI-ISSUE DRIVERS ---
        st.markdown("### ⚠️ Multi-Issue Fahrer")
        multi = get_multi_issue_drivers(df)
        
        if multi:
            st.markdown("Fahrer mit mehreren gleichzeitigen Concession-Gründen:")
            for d in multi[:5]:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f3f4;">
                    <span style="font-weight: 500;">{d['driver']}</span>
                    <span>{d['multi_issues']} Multi-Issues · €{d['cost']:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keine Multi-Issue Daten verfügbar")
    
    # 5. ACTIONS (Coaching)
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
            
            # --- ENHANCED ANALYTICS INSIGHTS FOR COACHING ---
            # Get extended analytics for this driver
            driver_stats = get_driver_enhanced_stats(df, sel_driver)
            driver_time = get_time_analysis(df, sel_driver)
            
            # Analytics insights panel
            insights_items = []
            
            # Time pattern insight
            if driver_time['peak_hour']:
                insights_items.append(f"⏰ Peak-Zeit: <strong>{driver_time['peak_hour']}</strong> ({driver_time['peak_hour_pct']:.0f}%)")
            if driver_time['peak_day']:
                insights_items.append(f"📅 Risiko-Tag: <strong>{driver_time['peak_day']}</strong> ({driver_time['peak_day_pct']:.0f}%)")
            
            # Contact rate insight
            if driver_stats['contact_attempts'] > 0 or driver_stats['contact_success_rate'] > 0:
                rate_color = "#137333" if driver_stats['contact_success_rate'] > 50 else "#c5221f"
                insights_items.append(f"📞 Kontakt-Rate: <strong style='color:{rate_color}'>{driver_stats['contact_success_rate']:.0f}%</strong>")
            
            # Dimension misbookings
            if driver_stats['dimension_misbookings'] > 0:
                insights_items.append(f"📦 Briefkasten-Misbookings: <strong style='color:#c5221f'>{int(driver_stats['dimension_misbookings'])}</strong>")
            
            # Cost insight
            if driver_stats['total_cost'] > 0:
                insights_items.append(f"💰 Kosten: <strong>€{driver_stats['total_cost']:,.0f}</strong> (Ø €{driver_stats['avg_cost']:.0f}/Concession)")
            
            # Trend insight
            if driver_stats['trend_direction'] != '→':
                trend_color = "#c5221f" if driver_stats['trend_direction'] == '↑' else "#137333"
                insights_items.append(f"📈 Trend: <strong style='color:{trend_color}'>{driver_stats['trend_direction']} {driver_stats['trend_change']:+d}</strong> vs. Vorwoche")
            
            # Repeat offender
            if driver_stats['is_repeat_offender']:
                insights_items.append(f"🔁 <strong style='color:#b06000'>Wiederholungstäter</strong> ({driver_stats['consecutive_weeks']} Wochen in Folge)")
            
            if insights_items:
                st.markdown(f"""
                <div style="background: #e8f0fe; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <div style="font-size: 0.75rem; color: #1967d2; font-weight: 500; margin-bottom: 8px;">🔍 ANALYTICS INSIGHTS</div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; font-size: 0.9rem; color: #202124;">
                        {''.join([f"<div>{item}</div>" for item in insights_items])}
                    </div>
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
                
                # Build time pattern string for coaching
                time_insight = ""
                if driver_time['peak_hour']:
                    time_insight = f" Auffällig: {driver_time['peak_hour_pct']:.0f}% deiner Probleme passieren zwischen {driver_time['peak_hour']}."
                if driver_time['peak_day'] and driver_time['peak_day_pct'] > 25:
                    time_insight += f" {driver_time['peak_day']} ist dein kritischster Tag ({driver_time['peak_day_pct']:.0f}%)."
                
                contact_insight = ""
                if driver_stats['contact_success_rate'] < 30 and driver_stats['contact_attempts'] > 0:
                    contact_insight = " Deine Kontakt-Erfolgsrate ist niedrig - Kunden erreichen ist wichtig für erfolgreiche Zustellung."
                
                misbooking_insight = ""
                if driver_stats['dimension_misbookings'] > 2:
                    misbooking_insight = f" {int(driver_stats['dimension_misbookings'])} Pakete wurden falsch als Briefkasten/Household gebucht."
                
                # 1. Observation (Fact) - ENHANCED
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-size: 0.7rem; color: #5f6368; text-transform: uppercase; font-weight: 500; margin-bottom: 8px;">1. FESTSTELLUNG</div>
                    <div style="font-size: 1rem; color: #202124; line-height: 1.6;">
                        Im Zeitraum <strong>{week_str}</strong> hattest du <strong>{total} Concessions</strong> (€{driver_stats['total_cost']:,.0f} Kosten).
                        Dein Hauptproblem ist <strong>{mp}</strong> ({int(max(counts.values()) if counts else 0)} Fälle).
                        {f'Zusätzlich: {zip_pct:.0f}% der Fälle in PLZ {top_zip}.' if top_zip and zip_pct > 30 else ''}
                        {time_insight}{contact_insight}{misbooking_insight}
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
                    if st.button("✓ Fahrer bestätigt", width='stretch'):
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
                    st.download_button("📥 Protokoll herunterladen", protocol, f"coaching_{sel_driver[:10]}.txt", width='stretch')
            
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
                    st.dataframe(pd.DataFrame(breakdown), width='stretch', hide_index=True)
                
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
                        st.plotly_chart(fig, width='stretch')
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
                    st.plotly_chart(fig, width='stretch')
            
            with subtab_history:
                cols_to_show = ['year_week', 'tracking_id', 'zip_code']
                if 'Concession Cost' in dd.columns:
                    cols_to_show.append('Concession Cost')
                st.dataframe(dd[cols_to_show], width='stretch', hide_index=True)
if __name__ == "__main__":
    main()
