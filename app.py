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
