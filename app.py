"""
LTS Quality Management
DNR Root Cause Analyse & Personalisiertes Fahrer-Coaching
Mobile-First Responsive Design
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
# Page Configuration - Mobile optimized
st.set_page_config(
    page_title="LTS Quality",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Always collapsed on load
)
# Mobile-First CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --primary: #2563eb;
        --danger: #ef4444;
        --success: #10b981;
        --warning: #f59e0b;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-500: #6b7280;
        --gray-700: #374151;
        --gray-900: #111827;
    }
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Hide defaults */
    #MainMenu, footer, .stDeployButton { display: none; }
    header[data-testid="stHeader"] { background: transparent; }
    
    /* Main container - responsive */
    .main .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1200px !important;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem 0.75rem !important;
            max-width: 100% !important;
        }
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
    }
    
    /* Header - responsive */
    .app-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    @media (max-width: 768px) {
        .app-header {
            padding: 12px 16px;
            margin-bottom: 12px;
        }
    }
    
    .app-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0;
    }
    
    @media (max-width: 768px) {
        .app-title { font-size: 1rem; }
    }
    
    .app-stat {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Cards - responsive */
    .compact-card {
        background: white;
        border-radius: 12px;
        border: 1px solid var(--gray-200);
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: box-shadow 0.2s ease;
    }
    
    .compact-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    @media (max-width: 768px) {
        .compact-card {
            padding: 12px;
            margin-bottom: 10px;
        }
    }
    
    .compact-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .compact-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--gray-900);
    }
    
    @media (max-width: 768px) {
        .compact-card-title { font-size: 0.85rem; }
    }
    
    .tag-sm {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    @media (max-width: 768px) {
        .tag-sm {
            padding: 2px 8px;
            font-size: 0.65rem;
        }
    }
    
    .tag-critical { background: #fef2f2; color: #dc2626; }
    .tag-info { background: #eff6ff; color: #2563eb; }
    .tag-low { background: #f0fdf4; color: #16a34a; }
    
    .compact-card-stat {
        font-size: 0.7rem;
        color: var(--gray-500);
        margin-bottom: 8px;
    }
    
    .compact-card-list {
        margin: 0;
        padding-left: 16px;
        font-size: 0.75rem;
        color: var(--gray-700);
    }
    
    .compact-card-list li {
        margin: 4px 0;
    }
    
    /* Driver row compact */
    .driver-row {
        background: white;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
        border: 1px solid var(--gray-200);
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    
    .driver-row-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .driver-id {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--gray-900);
        font-family: monospace;
    }
    
    .driver-count {
        font-size: 0.7rem;
        color: var(--danger);
        font-weight: 600;
    }
    
    .driver-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.65rem;
        font-weight: 500;
    }
    
    .badge-household { background: #fff7ed; color: #ea580c; }
    .badge-geo { background: #fef2f2; color: #dc2626; }
    .badge-prefs { background: #eff6ff; color: #2563eb; }
    .badge-multiple { background: #faf5ff; color: #7c3aed; }
    
    /* Coaching compact */
    .coaching-box {
        background: white;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        overflow: hidden;
    }
    
    .coaching-header {
        background: var(--primary);
        color: white;
        padding: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .coaching-section {
        padding: 12px;
        border-bottom: 1px solid var(--gray-100);
    }
    
    .coaching-label {
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    
    .coaching-content {
        font-size: 0.8rem;
        color: var(--gray-700);
        line-height: 1.5;
    }
    
    .coaching-question {
        padding: 6px 0 6px 10px;
        border-left: 2px solid var(--primary);
        margin: 6px 0;
        font-size: 0.8rem;
    }
    
    .coaching-commit {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 6px;
        padding: 10px;
        color: #166534;
        font-size: 0.8rem;
    }
    
    /* Make streamlit elements compact */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-size: 0.8rem;
    }
    
    .stSelectbox > div {
        font-size: 0.85rem;
    }
    
    .stMetric {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }
    
    .stMetric label {
        font-size: 0.65rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    
    /* Expander compact */
    .streamlit-expanderHeader {
        font-size: 0.8rem !important;
        padding: 8px !important;
    }
    
    /* DataFrames scrollable */
    [data-testid="stDataFrame"] {
        font-size: 0.75rem;
    }
    
    /* Button styles */
    .stButton button {
        font-size: 0.8rem !important;
        padding: 6px 12px !important;
    }
    
    .stDownloadButton button {
        width: 100%;
        font-size: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)
# ============================================================================
# DATA FUNCTIONS
# ============================================================================
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', '')
    return df
def convert_yn_to_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: 1 if str(x).upper().strip() in ['Y', 'YES', '1', 'TRUE'] else 0)
    return df
def fill_missing_columns(df):
    defaults = {
        'Delivered to Safe Location': 0, 'Geo Distance > 25m': 0,
        'Delivered to Household Member / Customer': 0, 'Delivery preferences not followed': 0,
        'Unattended Delivery & No Photo on Delivery': 0, 'Attended DNR Deliveries': 0,
        'Feedback False Scan Indicator': 0, 'High Value Item (Y/N)': 0, 'Concession Cost': 0.0
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val
    return df
def load_file_data(uploaded_file):
    filename = uploaded_file.name.lower()
    if filename.endswith(('.xlsx', '.xls')):
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Excel-Fehler: {e}")
            return None
    else:
        for enc in ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=None, engine='python', encoding=enc)
                break
            except:
                continue
        else:
            st.error("Datei konnte nicht geladen werden.")
            return None
    
    df = clean_column_names(df)
    df = convert_yn_to_numeric(df, ['High Value Item (Y/N)', 'Feedback False Scan Indicator', 'Attended DNR Deliveries'])
    df = fill_missing_columns(df)
    
    for col in ['Concession Cost', 'Geo Distance > 25m', 'Delivered to Household Member / Customer',
                'Delivery preferences not followed', 'Unattended Delivery & No Photo on Delivery']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df
def load_sample_data():
    import random
    random.seed(42)
    drivers = ['A1B23M63H4GRJ1', 'A1CE94XEF8Q4IW', 'A1A5TD0FB57T8D', 'A1HA4BWI34PE6T', 
               'A12VULCF9QV1FE', 'A1IQSLQOLKOZ0A', 'A12MTTC6P68FMV', 'A1XYZ123ABC']
    zips = ['5020', '5400', '5021', '5082', '5071']
    weeks = ['2025-44', '2025-45', '2025-46', '2025-47', '2025-48', '2025-49']
    
    data = []
    for _ in range(218):
        driver = random.choice(drivers)
        data.append({
            'year_week': random.choice(weeks),
            'transporter_id': driver,
            'zip_code': random.choice(zips),
            'tracking_id': f'TRK{random.randint(100000, 999999)}',
            'Concession Cost': round(random.uniform(5, 80), 2),
            'High Value Item (Y/N)': random.choice([0]*4 + [1]),
            'Geo Distance > 25m': random.choice([0]*3 + [1]) if driver in ['A1B23M63H4GRJ1', 'A12MTTC6P68FMV'] else 0,
            'Delivered to Household Member / Customer': random.choice([0, 0, 1]) if driver in ['A1A5TD0FB57T8D', 'A12VULCF9QV1FE'] else 0,
            'Delivery preferences not followed': random.choice([0]*3 + [1]) if driver == 'A1CE94XEF8Q4IW' else 0,
            'Feedback False Scan Indicator': 1 if driver == 'A1A5TD0FB57T8D' and random.random() > 0.85 else 0,
            'Unattended Delivery & No Photo on Delivery': random.choice([0, 0, 1]),
            'Attended DNR Deliveries': random.choice([0, 1]),
            'Delivered to Safe Location': 0
        })
    return pd.DataFrame(data)
# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================
def get_driver_main_problem(driver_data):
    problems = {
        'Geo Distance': driver_data.get('Geo Distance > 25m', pd.Series([0])).sum(),
        'Household Member': driver_data.get('Delivered to Household Member / Customer', pd.Series([0])).sum(),
        'Delivery Prefs': driver_data.get('Delivery preferences not followed', pd.Series([0])).sum(),
        'No Photo': driver_data.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum(),
        'False Scan': driver_data.get('Feedback False Scan Indicator', pd.Series([0])).sum(),
    }
    active = {k: v for k, v in problems.items() if v > 0}
    if len(active) > 1:
        max_prob = max(active, key=active.get)
        if active[max_prob] < sum(active.values()) * 0.5:
            return 'Multiple', problems
    return (max(problems, key=problems.get), problems) if sum(problems.values()) > 0 else ('Sonstige', problems)
def get_loss_buckets(df):
    return {
        'Household': int(df.get('Delivered to Household Member / Customer', pd.Series([0])).sum()),
        'Prefs': int(df.get('Delivery preferences not followed', pd.Series([0])).sum()),
        'Geo': int(df.get('Geo Distance > 25m', pd.Series([0])).sum()),
        'No Photo': int(df.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum()),
        'False Scan': int(df.get('Feedback False Scan Indicator', pd.Series([0])).sum()),
    }
def get_weekly_trend(df, driver_id):
    if 'year_week' not in df.columns:
        return []
    weekly = df[df['transporter_id'] == driver_id].groupby('year_week').size().sort_index()
    return weekly.tolist()[-6:]
# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Data loading via expander
    with st.expander("📁 Daten laden", expanded=True):
        uploaded_file = st.file_uploader("CSV/Excel hochladen", type=['csv', 'xlsx', 'xls'], label_visibility="collapsed")
        if uploaded_file:
            df = load_file_data(uploaded_file)
            if df is not None:
                st.success(f"✓ {len(df)} Zeilen geladen")
        else:
            df = None
    
    # Empty state - no demo data
    if df is None:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; background: white; border-radius: 12px; border: 2px dashed #e5e7eb; margin-top: 20px;">
            <div style="font-size: 3rem; margin-bottom: 16px;">📊</div>
            <h2 style="color: #374151; margin-bottom: 8px;">Willkommen bei LTS Quality Management</h2>
            <p style="color: #6b7280; margin-bottom: 24px;">Lade deine Concession-Daten hoch, um zu starten.</p>
            <div style="background: #f3f4f6; padding: 16px; border-radius: 8px; display: inline-block; text-align: left;">
                <p style="font-size: 0.85rem; color: #374151; margin: 0 0 8px 0;"><strong>Benötigte Spalten:</strong></p>
                <code style="font-size: 0.75rem; color: #6b7280;">transporter_id, year_week, zip_code, Geo Distance > 25m, ...</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Compact header
    weeks = sorted(df['year_week'].unique()) if 'year_week' in df.columns else []
    week_range = f"KW{weeks[0].split('-')[1]}-{weeks[-1].split('-')[1]}" if weeks else ""
    
    st.markdown(f"""
    <div class="app-header">
        <span class="app-title">📊 LTS Quality</span>
        <span class="app-stat">DNR: {len(df)} ({week_range})</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation via TABS (mobile friendly)
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Roadmap", "👥 Fahrer", "📈 Trends", "🎓 Coaching"])
    
    # ========================================================================
    # TAB 1: ROADMAP
    # ========================================================================
    with tab1:
       # Compact header
    weeks = sorted([str(w) for w in df['year_week'].unique()]) if 'year_week' in df.columns else []
    try:
        week_range = f"KW{str(weeks[0]).split('-')[1]}-{str(weeks[-1]).split('-')[1]}" if weeks and '-' in str(weeks[0]) else ""
    except:
        week_range = ""
        actions = [
            {"tag": "SOFORT", "tag_class": "tag-critical", 
             "content": ["Standup-Briefing", "'Household' nur bei Übergabe", "POD Umgehung = Warnung"]},
            {"tag": "TRAINING", "tag_class": "tag-info",
             "content": ["1:1 mit Top Geo-Fahrern", "Scan an Haustür", "Ride-along"]},
            {"tag": "ANALYSE", "tag_class": "tag-low",
             "content": ["Apartmentkomplexe prüfen", "Access Codes", "Safe Locations"]}
        ]
        
        for i, (bucket_name, count) in enumerate(sorted_b):
            a = actions[i] if i < len(actions) else actions[-1]
            pct = count / sum(buckets.values()) * 100 if sum(buckets.values()) > 0 else 0
            
            st.markdown(f"""
            <div class="compact-card">
                <div class="compact-card-header">
                    <span class="compact-card-title">{i+1}. {bucket_name}</span>
                    <span class="tag-sm {a['tag_class']}">{a['tag']}</span>
                </div>
                <div class="compact-card-stat">{pct:.0f}% • {count} Fälle</div>
                <ul class="compact-card-list">
                    {''.join(f'<li>{c}</li>' for c in a['content'])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("📋 Maßnahmenplan"):
            plan = pd.DataFrame([
                {"Prio": "🔴", "Maßnahme": "POD Check", "Ziel": "Top 3 Fahrer"},
                {"Prio": "🟠", "Maßnahme": "Geo Training", "Ziel": "Top 5 Fahrer"},
                {"Prio": "🟡", "Maßnahme": "Ablageort", "Ziel": "Alle"},
            ])
            st.dataframe(plan, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # TAB 2: FAHRER
    # ========================================================================
    with tab2:
        search = st.text_input("🔍", placeholder="Suche ID...", label_visibility="collapsed")
        
        watchlist = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_main_problem(dd)
            watchlist.append({'id': did, 'count': len(dd), 'problem': mp})
        
        wdf = sorted(watchlist, key=lambda x: x['count'], reverse=True)
        if search:
            wdf = [w for w in wdf if search.lower() in w['id'].lower()]
        
        for w in wdf[:8]:
            badge_class = 'badge-geo' if 'Geo' in w['problem'] else 'badge-household' if 'Household' in w['problem'] else 'badge-prefs' if 'Pref' in w['problem'] else 'badge-multiple'
            
            st.markdown(f"""
            <div class="driver-row">
                <div class="driver-row-top">
                    <span class="driver-id">{w['id'][:12]}...</span>
                    <span class="driver-count">{w['count']} DSC</span>
                </div>
                <span class="driver-badge {badge_class}">{w['problem']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 3: TRENDS
    # ========================================================================
    with tab3:
        # Loss buckets chart
        buckets = get_loss_buckets(df)
        bdf = pd.DataFrame(list(buckets.items()), columns=['Grund', 'Anzahl']).sort_values('Anzahl', ascending=True)
        
        fig = px.bar(bdf, x='Anzahl', y='Grund', orientation='h',
                    color_discrete_sequence=['#ef4444'])
        fig.update_layout(
            height=200, 
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=False,
            xaxis_title="", yaxis_title="",
            plot_bgcolor='white',
            font=dict(size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Weekly trend
        if 'year_week' in df.columns:
            weekly = df.groupby('year_week').size().reset_index(name='count')
            fig2 = px.line(weekly, x='year_week', y='count', markers=True)
            fig2.update_traces(line_color='#3b82f6', line_width=2, marker_size=6)
            fig2.update_layout(
                height=180, 
                margin=dict(l=0, r=0, t=10, b=10),
                xaxis_title="", yaxis_title="DNR",
                plot_bgcolor='white',
                font=dict(size=10)
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Top ZIPs
        if 'zip_code' in df.columns:
            st.markdown("**Top PLZ:**")
            zc = df.groupby('zip_code').size().sort_values(ascending=False).head(3)
            for z, c in zc.items():
                pct = c / len(df) * 100
                st.markdown(f"• **{z}**: {c} ({pct:.0f}%)")
    
    # ========================================================================
    # TAB 4: COACHING
    # ========================================================================
    with tab4:
        opts = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_main_problem(dd)
            opts.append({'id': did, 'label': f"{did[:10]}.. ({len(dd)})", 'count': len(dd), 'problem': mp})
        opts = sorted(opts, key=lambda x: x['count'], reverse=True)
        
        sel = st.selectbox(
            "Fahrer", 
            options=[o['id'] for o in opts],
            format_func=lambda x: next((o['label'] for o in opts if o['id'] == x), x),
            label_visibility="collapsed"
        )
        
        if sel:
            driver_data = df[df['transporter_id'] == sel]
            mp, counts = get_driver_main_problem(driver_data)
            total = len(driver_data)
            weeks_active = driver_data['year_week'].nunique() if 'year_week' in driver_data.columns else 1
            hv = int(driver_data.get('High Value Item (Y/N)', pd.Series([0])).sum())
            
            trend = get_weekly_trend(df, sel)
            trend_txt = "↑" if len(trend) >= 2 and trend[-1] > trend[-2] else "↓" if len(trend) >= 2 and trend[-1] < trend[-2] else "→"
            
            # Metrics row
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("DSC", total)
            c2.metric("Wochen", weeks_active)
            c3.metric("Trend", trend_txt)
            c4.metric("HV", hv if hv > 0 else "—")
            
            # Coaching content
            if counts.get('False Scan', 0) > 0:
                problem = f"🚨 KRITISCH: {int(counts['False Scan'])}x False Scan!"
                questions = ["Erkläre diese Fälle", "Scan im Fahrzeug?", "Weißt du: False Scan = Kündigung?"]
                commit = "Erste Verwarnung. Nächster Vorfall = HR."
            elif counts.get('Household Member', 0) > 0:
                problem = f"{int(counts['Household Member'])}x 'Household Member' ohne echte Übergabe"
                questions = ["Wann Household Member?", "Was bei Ablage?", "Ohne Foto = wir zahlen"]
                commit = "Ablage = Foto + Safe Location"
            elif counts.get('Geo Distance', 0) > 0:
                problem = f"{int(counts['Geo Distance'])}x GPS >25m beim Scan"
                questions = ["Scannst du im Auto?", "Kennst du Group Stop Ablauf?"]
                commit = "Scan IMMER an Haustür"
            else:
                problem = "Verschiedene Issues - Detailanalyse nötig"
                questions = ["Lass uns Zustellungen durchgehen"]
                commit = "Follow-up in 1 Woche"
            
            st.markdown(f"""
            <div class="coaching-box">
                <div class="coaching-header">🎓 {sel[:14]}...</div>
                <div class="coaching-section">
                    <div class="coaching-label">Problem</div>
                    <div class="coaching-content">{problem}</div>
                </div>
                <div class="coaching-section">
                    <div class="coaching-label">Fragen</div>
                    {''.join(f'<div class="coaching-question">{q}</div>' for q in questions)}
                </div>
                <div class="coaching-section">
                    <div class="coaching-label">Commitment</div>
                    <div class="coaching-commit">{commit}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            with st.expander("📊 Details"):
                breakdown = []
                for col, label in [
                    ('Geo Distance > 25m', 'Geo'),
                    ('Delivered to Household Member / Customer', 'Household'),
                    ('Delivery preferences not followed', 'Prefs'),
                    ('Unattended Delivery & No Photo on Delivery', 'No Photo'),
                    ('Feedback False Scan Indicator', 'False Scan')
                ]:
                    if col in driver_data.columns:
                        cnt = int(driver_data[col].sum())
                        if cnt > 0:
                            breakdown.append({'Typ': label, '#': cnt})
                
                if breakdown:
                    st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)
                
                if 'zip_code' in driver_data.columns:
                    st.markdown(f"**PLZ:** {', '.join(driver_data['zip_code'].value_counts().head(3).index.tolist())}")
            
            # Download
            protocol = f"""COACHING: {sel}
Datum: {datetime.now().strftime('%d.%m.%Y')}
Problem: {problem}
Fragen: {'; '.join(questions)}
Commit: {commit}
"""
            st.download_button("📥 Protokoll", protocol, f"coaching_{sel[:8]}.txt")
if __name__ == "__main__":
    main()

