"""
LTS Quality Management
DNR Root Cause Analyse & Personalisiertes Fahrer-Coaching
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
# Page Configuration
st.set_page_config(
    page_title="LTS Quality Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"  # Auto-collapse on mobile
)
# Professional CSS - Modern UI Best Practices
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-500: #6b7280;
        --gray-700: #374151;
        --gray-900: #111827;
        --radius: 12px;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: var(--gray-50);
    }
    
    /* Hide Streamlit Defaults */
    #MainMenu, footer, .stDeployButton {display: none;}
    header[data-testid="stHeader"] {background: transparent;}
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: none;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.8) !important;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 4px 0;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.1);
        color: white !important;
    }
    
    /* Logo/Brand */
    .brand {
        padding: 24px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 24px;
    }
    
    .brand-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .brand-subtitle {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.6);
        margin-top: 4px;
    }
    
    /* Page Header */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 32px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--gray-200);
    }
    
    .page-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--gray-900);
        margin: 0;
    }
    
    .page-subtitle {
        font-size: 0.875rem;
        color: var(--gray-500);
        margin-top: 4px;
    }
    
    /* Stats Badge */
    .stats-badge {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 24px;
        padding: 8px 20px;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--danger);
        box-shadow: var(--shadow-sm);
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: var(--radius);
        border: 1px solid var(--gray-200);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 0.2s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
    }
    
    .card-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: var(--radius);
        border: 1px solid var(--gray-200);
        padding: 20px 24px;
        box-shadow: var(--shadow-sm);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--gray-900);
    }
    
    .metric-value.danger {
        color: var(--danger);
    }
    
    .metric-value.success {
        color: var(--success);
    }
    
    /* Priority Tags */
    .tag {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .tag-critical { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .tag-high { background: #fff7ed; color: #ea580c; border: 1px solid #fed7aa; }
    .tag-medium { background: #fefce8; color: #ca8a04; border: 1px solid #fef08a; }
    .tag-low { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    .tag-info { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    
    /* Problem Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        gap: 6px;
    }
    
    .badge-geo { background: #fef2f2; color: #dc2626; }
    .badge-household { background: #fff7ed; color: #ea580c; }
    .badge-prefs { background: #eff6ff; color: #2563eb; }
    .badge-photo { background: #f0fdf4; color: #16a34a; }
    .badge-falsescan { background: #dc2626; color: white; }
    .badge-multiple { background: #faf5ff; color: #7c3aed; }
    
    /* Action Cards */
    .action-card {
        background: white;
        border-radius: var(--radius);
        border: 1px solid var(--gray-200);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--danger);
        height: 100%;
    }
    
    .action-card.training {
        border-left-color: var(--primary);
    }
    
    .action-card.analyse {
        border-left-color: var(--gray-500);
    }
    
    .action-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    
    .action-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--gray-900);
    }
    
    .action-card-stat {
        font-size: 0.875rem;
        color: var(--gray-500);
        margin-bottom: 16px;
    }
    
    .action-card-content {
        font-size: 0.875rem;
        color: var(--gray-700);
        line-height: 1.7;
    }
    
    .action-card-content li {
        margin: 8px 0;
    }
    
    /* Coaching Sections */
    .coaching-container {
        background: white;
        border-radius: var(--radius);
        border: 1px solid var(--gray-200);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    .coaching-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        padding: 20px 24px;
        color: white;
    }
    
    .coaching-driver-id {
        font-size: 1.25rem;
        font-weight: 700;
    }
    
    .coaching-section {
        padding: 20px 24px;
        border-bottom: 1px solid var(--gray-100);
    }
    
    .coaching-section:last-child {
        border-bottom: none;
    }
    
    .coaching-section-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    .coaching-section-content {
        font-size: 0.9375rem;
        color: var(--gray-700);
        line-height: 1.7;
    }
    
    .coaching-question {
        padding: 8px 0;
        padding-left: 16px;
        border-left: 2px solid var(--primary);
        margin: 8px 0;
    }
    
    .coaching-commitment {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 16px;
        color: #166534;
    }
    
    /* Alert Box */
    .alert {
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    .alert-warning {
        background: #fefce8;
        border: 1px solid #fef08a;
        color: #854d0e;
    }
    
    .alert-title {
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    /* Table Styles */
    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .data-table th {
        background: var(--gray-50);
        padding: 12px 16px;
        text-align: left;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid var(--gray-200);
    }
    
    .data-table td {
        padding: 16px;
        border-bottom: 1px solid var(--gray-100);
        font-size: 0.875rem;
        color: var(--gray-700);
    }
    
    .data-table tr:hover td {
        background: var(--gray-50);
    }
    
    /* Button */
    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
    }
    
    .btn-primary {
        background: var(--primary);
        color: white;
    }
    
    .btn-primary:hover {
        background: var(--primary-dark);
    }
    
    .btn-outline {
        background: white;
        color: var(--gray-700);
        border: 1px solid var(--gray-300);
    }
    
    .btn-outline:hover {
        background: var(--gray-50);
        border-color: var(--gray-400);
    }
    
    /* =====================================================
       MOBILE RESPONSIVE STYLES
       ===================================================== */
    
    /* Tablet and below */
    @media (max-width: 992px) {
        .page-title {
            font-size: 1.5rem;
        }
        
        .action-card {
            padding: 16px;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Mobile devices */
    @media (max-width: 768px) {
        /* Main container padding */
        .main .block-container {
            padding: 1rem 1rem !important;
            max-width: 100% !important;
        }
        
        /* Page header stacked */
        .page-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
        }
        
        .page-title {
            font-size: 1.25rem;
        }
        
        .page-subtitle {
            font-size: 0.75rem;
        }
        
        /* Stats badge full width on mobile */
        .stats-badge {
            padding: 6px 14px;
            font-size: 0.75rem;
        }
        
        /* Cards responsive */
        .card, .action-card, .metric-card {
            padding: 16px;
            border-radius: 10px;
        }
        
        .action-card-header {
            flex-direction: column;
            gap: 8px;
        }
        
        .action-card-title {
            font-size: 0.9rem;
        }
        
        .action-card-content {
            font-size: 0.8rem;
        }
        
        .action-card-content li {
            margin: 6px 0;
        }
        
        /* Metrics smaller on mobile */
        .metric-value {
            font-size: 1.25rem;
        }
        
        .metric-label {
            font-size: 0.65rem;
        }
        
        /* Tags smaller */
        .tag {
            padding: 3px 8px;
            font-size: 0.65rem;
        }
        
        .badge {
            padding: 4px 8px;
            font-size: 0.7rem;
        }
        
        /* Coaching container mobile */
        .coaching-section {
            padding: 16px;
        }
        
        .coaching-driver-id {
            font-size: 1rem;
        }
        
        .coaching-section-content {
            font-size: 0.85rem;
        }
        
        .coaching-question {
            padding-left: 12px;
            font-size: 0.85rem;
        }
        
        /* Tables scrollable */
        [data-testid="stDataFrame"] {
            overflow-x: auto !important;
        }
        
        /* Sidebar collapsed by default on mobile - handled by Streamlit */
        [data-testid="stSidebar"] {
            min-width: 250px !important;
        }
        
        [data-testid="stSidebar"] .brand {
            padding: 16px;
        }
        
        [data-testid="stSidebar"] .brand-title {
            font-size: 1rem;
        }
        
        /* Columns stack on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        
        /* Selectbox full width */
        .stSelectbox {
            width: 100% !important;
        }
        
        /* Expander padding */
        .streamlit-expanderHeader {
            font-size: 0.85rem !important;
        }
        
        /* Download button */
        .stDownloadButton button {
            width: 100% !important;
            padding: 12px !important;
        }
        
        /* Alert boxes */
        .alert {
            padding: 12px 14px;
            font-size: 0.85rem;
        }
        
        /* Markdown text sizing */
        h2 {
            font-size: 1.25rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        h4 {
            font-size: 1rem !important;
        }
        
        p, li {
            font-size: 0.9rem !important;
        }
    }
    
    /* Small phones */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.75rem 0.5rem !important;
        }
        
        .page-title {
            font-size: 1.1rem;
        }
        
        .metric-value {
            font-size: 1.1rem;
        }
        
        .action-card {
            padding: 12px;
        }
        
        .coaching-section {
            padding: 12px;
        }
        
        .brand {
            padding: 12px !important;
        }
    }
    
    /* Touch-friendly improvements */
    @media (pointer: coarse) {
        /* Larger touch targets */
        .stRadio label {
            min-height: 48px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        .stSelectbox > div {
            min-height: 48px !important;
        }
        
        button {
            min-height: 44px !important;
            padding: 10px 16px !important;
        }
        
        /* More spacing between interactive elements */
        .stButton {
            margin: 8px 0 !important;
        }
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
        'Geo Distance / Group Stops': driver_data.get('Geo Distance > 25m', pd.Series([0])).sum(),
        'DNR (Household Member)': driver_data.get('Delivered to Household Member / Customer', pd.Series([0])).sum(),
        'Delivery Preferences': driver_data.get('Delivery preferences not followed', pd.Series([0])).sum(),
        'No Photo on Delivery': driver_data.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum(),
        'False Scan': driver_data.get('Feedback False Scan Indicator', pd.Series([0])).sum(),
    }
    
    active = {k: v for k, v in problems.items() if v > 0}
    if len(active) > 1:
        max_prob = max(active, key=active.get)
        if active[max_prob] < sum(active.values()) * 0.5:
            return 'Multiple Reasons', problems
    
    return (max(problems, key=problems.get), problems) if sum(problems.values()) > 0 else ('Sonstige', problems)
def get_loss_buckets(df):
    return {
        'Household Member': int(df.get('Delivered to Household Member / Customer', pd.Series([0])).sum()),
        'Delivery Prefs': int(df.get('Delivery preferences not followed', pd.Series([0])).sum()),
        'Geo Distance > 25m': int(df.get('Geo Distance > 25m', pd.Series([0])).sum()),
        'No Photo': int(df.get('Unattended Delivery & No Photo on Delivery', pd.Series([0])).sum()),
        'False Scan': int(df.get('Feedback False Scan Indicator', pd.Series([0])).sum()),
    }
def get_weekly_trend(df, driver_id):
    if 'year_week' not in df.columns:
        return []
    weekly = df[df['transporter_id'] == driver_id].groupby('year_week').size().sort_index()
    return weekly.tolist()[-6:]
def generate_coaching(df, driver_id):
    driver_data = df[df['transporter_id'] == driver_id]
    if driver_data.empty:
        return None
    
    total = len(driver_data)
    main_problem, counts = get_driver_main_problem(driver_data)
    weeks = driver_data['year_week'].nunique() if 'year_week' in driver_data.columns else 1
    hv = int(driver_data.get('High Value Item (Y/N)', pd.Series([0])).sum())
    
    trend = get_weekly_trend(df, driver_id)
    trend_text = "steigend ⬆️" if len(trend) >= 2 and trend[-1] > trend[-2] else "stabil ➡️" if len(trend) >= 2 and trend[-1] == trend[-2] else "fallend ⬇️" if len(trend) >= 2 else "—"
    
    coaching = {
        'driver_id': driver_id, 'total': total, 'main_problem': main_problem,
        'counts': counts, 'weeks': weeks, 'hv': hv, 'trend': trend_text,
        'facts': [], 'problem': '', 'questions': [], 'commitment': '', 'tags': []
    }
    
    coaching['facts'] = [
        f"{total} Concessions in {weeks} Wochen",
        f"Trend: {trend_text}",
        f"Hauptproblem: {main_problem}"
    ]
    if hv > 0:
        coaching['facts'].append(f"⚠️ {hv} High-Value Items betroffen")
    
    # Problem specific content
    if counts.get('False Scan', 0) > 0:
        coaching['tags'] = ['False Scan', 'Kritisch']
        coaching['problem'] = f"KRITISCH: {int(counts['False Scan'])}x False Scan erkannt. Das System zeigt Scans an Orten, wo du laut GPS nicht warst. Dies ist ein schwerer Verstoß."
        coaching['questions'] = [
            "Erkläre, was an diesen Adressen passiert ist.",
            "Hast du Pakete im Fahrzeug gescannt?",
            "Weißt du, dass False Scans zur Kündigung führen können?"
        ]
        coaching['commitment'] = "Erste Verwarnung. Nächster Vorfall = HR-Eskalation."
    elif counts.get('DNR (Household Member)', 0) > 0:
        c = int(counts['DNR (Household Member)'])
        coaching['tags'] = ['Household Member', 'High']
        coaching['problem'] = f"{c}x 'Delivered to Household Member' gewählt, aber keine echte Übergabe. Das Paket wird abgelegt, ohne Foto. Bei DNR = kein Beweis."
        coaching['questions'] = [
            "Wann darfst du 'Household Member' auswählen? (Nur bei Übergabe!)",
            "Was musst du bei Ablage machen? (Safe Location + Foto)",
            "Verstehst du, dass ohne Foto wir automatisch zahlen?"
        ]
        coaching['commitment'] = "Ab sofort: Bei jeder Ablage ein Foto. 'Household Member' NUR bei Augenkontakt."
    elif counts.get('Geo Distance / Group Stops', 0) > 0:
        c = int(counts['Geo Distance / Group Stops'])
        coaching['tags'] = ['Geo Distance', 'Training']
        coaching['problem'] = f"{c}x GPS-Abweichung >25m beim Scannen. Mögliche Ursachen: Scannen im Auto, falsche Group-Stop-Handhabung."
        coaching['questions'] = [
            "Scannst du manchmal schon im Fahrzeug?",
            "Kennst du den korrekten Group-Stop-Ablauf?",
            "Scan erst an der Haustür - verstanden?"
        ]
        coaching['commitment'] = "Scan IMMER erst an der Haustür. Bei Group Stops: Jedes Paket einzeln vor Ort."
    elif counts.get('Delivery Preferences', 0) > 0:
        c = int(counts['Delivery Preferences'])
        coaching['tags'] = ['Preferences', 'Medium']
        coaching['problem'] = f"{c}x Kundenpräferenzen nicht befolgt. Kunden hinterlegen Wünsche, die du beachten musst."
        coaching['questions'] = [
            "Liest du die Präferenzen vor jeder Zustellung?",
            "Weißt du, wo du sie in der App findest?"
        ]
        coaching['commitment'] = "Präferenzen werden vor jeder Zustellung gelesen und befolgt."
    else:
        coaching['tags'] = ['Multiple']
        coaching['problem'] = "Verschiedene Probleme ohne klares Muster. Detailanalyse erforderlich."
        coaching['questions'] = ["Lass uns gemeinsam ein paar Zustellungen durchgehen.", "Wo siehst du Verbesserungspotenzial?"]
        coaching['commitment'] = "Follow-up in einer Woche."
    
    return coaching
# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="brand">
            <div class="brand-title">📊 LTS Quality</div>
            <div class="brand-subtitle">Concession Management</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Daten laden", type=['csv', 'xlsx', 'xls'], label_visibility="collapsed")
        
        if uploaded_file:
            df = load_file_data(uploaded_file)
            if df is not None:
                st.success(f"✓ {len(df)} Datensätze")
        else:
            df = load_sample_data()
            st.caption("📋 Demo-Daten aktiv")
        
        st.markdown("---")
        page = st.radio("", ["🗺️ Action Roadmap", "👥 Fahrer Watchlist", "📈 Trend Analyse", "🎓 Coaching Tool"], label_visibility="collapsed")
        
        st.markdown("---")
        
        if df is not None and 'zip_code' in df.columns:
            top_zip = df.groupby('zip_code').size().idxmax()
            top_pct = df.groupby('zip_code').size().max() / len(df) * 100
            st.markdown(f"""
            <div class="alert alert-warning">
                <div class="alert-title">⚠️ Kritischer Fokus</div>
                ZIP {top_zip} = {top_pct:.0f}% aller Verluste
            </div>
            """, unsafe_allow_html=True)
    
    if df is None:
        st.error("Keine Daten")
        return
    
    # Header
    weeks = sorted(df['year_week'].unique()) if 'year_week' in df.columns else []
    week_range = f"KW{weeks[0].split('-')[1]}-{weeks[-1].split('-')[1]}" if weeks else ""
    
    # ========================================================================
    # ACTION ROADMAP
    # ========================================================================
    if "Roadmap" in page:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="page-header">
                <div>
                    <h1 class="page-title">Action Roadmap</h1>
                    <p class="page-subtitle">Datenbasis: {week_range}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stats-badge">Total DNR: {len(df)}</div>', unsafe_allow_html=True)
        
        # Top 3 Actions
        buckets = get_loss_buckets(df)
        sorted_b = sorted(buckets.items(), key=lambda x: x[1], reverse=True)[:3]
        
        cols = st.columns(3)
        
        actions = [
            {"title": "False 'Household' Scan", "tag": "Sofort", "tag_class": "tag-critical", "card_class": "",
             "content": ["Standup-Briefing morgen früh", "'Household Member' NUR bei Augenkontakt", "Wer POD umgeht → Tier 1 Warnung"]},
            {"title": "Geo-Fence Verhalten", "tag": "Training", "tag_class": "tag-info", "card_class": "training",
             "content": ["1:1 Gespräch mit Top 5 Geo-Sündern", "Scan erst an der Haustür, nie im Auto", "Ride-along für kritische Fahrer"]},
            {"title": f"ZIP {df.groupby('zip_code').size().idxmax()} Fokus" if 'zip_code' in df.columns else "ZIP Fokus", 
             "tag": "Analyse", "tag_class": "tag-low", "card_class": "analyse",
             "content": ["Komplexe Apartmentkomplexe prüfen", "Access Codes aktualisieren", "'Safe Locations' pushen"]}
        ]
        
        for i, col in enumerate(cols):
            if i < len(sorted_b):
                with col:
                    a = actions[i] if i < len(actions) else actions[-1]
                    pct = sorted_b[i][1] / sum(buckets.values()) * 100 if sum(buckets.values()) > 0 else 0
                    st.markdown(f"""
                    <div class="action-card {a['card_class']}">
                        <div class="action-card-header">
                            <span class="action-card-title">{i+1}. {sorted_b[i][0]}</span>
                            <span class="tag {a['tag_class']}">{a['tag']}</span>
                        </div>
                        <div class="action-card-stat">{pct:.1f}% der Verluste • {sorted_b[i][1]} Fälle</div>
                        <div class="action-card-content">
                            <ul style="margin:0;padding-left:20px;">
                                {''.join(f'<li>{c}</li>' for c in a['content'])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Implementation Plan
        st.markdown("### 📋 Implementierungsplan")
        
        plan = pd.DataFrame([
            {"PRIO": "High", "MASSNAHME": "POD Compliance Check", "ZIELGRUPPE": "Top 3 Household-Fahrer", "OWNER": "Lead Driver", "STATUS": "Offen"},
            {"PRIO": "High", "MASSNAHME": "Geo-Fence Training", "ZIELGRUPPE": "Top 5 Geo-Fahrer", "OWNER": "Dispatcher", "STATUS": "Offen"},
            {"PRIO": "Med", "MASSNAHME": "Ablageort-Training", "ZIELGRUPPE": "Alle Fahrer", "OWNER": "DSP Manager", "STATUS": "Geplant"},
        ])
        st.dataframe(plan, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # FAHRER WATCHLIST
    # ========================================================================
    elif "Watchlist" in page:
        st.markdown(f"""
        <div class="page-header">
            <div>
                <h1 class="page-title">Fahrer Performance Watchlist</h1>
                <p class="page-subtitle">Datenbasis: {week_range}</p>
            </div>
            <div class="stats-badge">Total DNR: {len(df)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        search = st.text_input("🔍 Suche Transporter ID...", "", label_visibility="collapsed", placeholder="Suche Transporter ID...")
        
        # Build watchlist
        watchlist = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_main_problem(dd)
            watchlist.append({'ID': did, 'Total DSC': len(dd), 'Hauptproblem': mp})
        
        wdf = pd.DataFrame(watchlist).sort_values('Total DSC', ascending=False)
        if search:
            wdf = wdf[wdf['ID'].str.contains(search, case=False)]
        
        # Custom table display
        for _, row in wdf.head(10).iterrows():
            badge_class = 'badge-geo' if 'Geo' in row['Hauptproblem'] else 'badge-household' if 'Household' in row['Hauptproblem'] else 'badge-prefs' if 'Pref' in row['Hauptproblem'] else 'badge-multiple'
            
            cols = st.columns([3, 2, 3, 2])
            cols[0].markdown(f"**{row['ID']}**")
            cols[1].markdown(f"{row['Total DSC']} DSCs")
            cols[2].markdown(f'<span class="badge {badge_class}">{row["Hauptproblem"]}</span>', unsafe_allow_html=True)
            if cols[3].button("Coaching →", key=f"c_{row['ID']}", use_container_width=True):
                st.session_state['sel_driver'] = row['ID']
    
    # ========================================================================
    # TREND ANALYSE
    # ========================================================================
    elif "Trend" in page:
        st.markdown(f"""
        <div class="page-header">
            <div>
                <h1 class="page-title">Concession Trend Analyse</h1>
                <p class="page-subtitle">Datenbasis: {week_range}</p>
            </div>
            <div class="stats-badge">Total DNR: {len(df)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Verlustgründe (Buckets)")
            buckets = get_loss_buckets(df)
            bdf = pd.DataFrame(list(buckets.items()), columns=['Grund', 'Anzahl']).sort_values('Anzahl', ascending=True)
            
            fig = px.bar(bdf, x='Anzahl', y='Grund', orientation='h',
                        color_discrete_sequence=['#ef4444', '#f97316', '#8b5cf6', '#3b82f6', '#10b981'])
            fig.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=10), showlegend=False,
                            xaxis_title="", yaxis_title="", plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Wöchentliche Entwicklung")
            if 'year_week' in df.columns:
                weekly = df.groupby('year_week').size().reset_index(name='count')
                fig = px.line(weekly, x='year_week', y='count', markers=True)
                fig.update_traces(line_color='#3b82f6', line_width=3, marker_size=8)
                fig.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=10),
                                xaxis_title="", yaxis_title="DNR Count", plot_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Heatmap: ZIP Codes")
        if 'zip_code' in df.columns:
            zc = df.groupby('zip_code').size().reset_index(name='count').sort_values('count', ascending=False)
            zc['pct'] = (zc['count'] / zc['count'].sum() * 100).round(1)
            
            fig = px.bar(zc.head(5), x='zip_code', y='count', text='pct',
                        color='count', color_continuous_scale='Reds')
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=250, showlegend=False, coloraxis_showscale=False,
                            xaxis_title="", yaxis_title="", plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # COACHING TOOL
    # ========================================================================
    elif "Coaching" in page:
        st.markdown("## 🎓 Fahrer Coaching Generator")
        st.caption("Personalisierte Coaching-Skripte basierend auf Root Cause Analyse")
        
        # Build options with detailed info
        opts = []
        for did in df['transporter_id'].unique():
            dd = df[df['transporter_id'] == did]
            mp, _ = get_driver_main_problem(dd)
            opts.append({'id': did, 'label': f"{did} — {mp} ({len(dd)} DSCs)", 'count': len(dd), 'problem': mp})
        opts = sorted(opts, key=lambda x: x['count'], reverse=True)
        
        st.markdown("### Fahrer auswählen")
        sel = st.selectbox(
            "Fahrer",
            options=[o['id'] for o in opts],
            format_func=lambda x: next((o['label'] for o in opts if o['id'] == x), x),
            label_visibility="collapsed"
        )
        
        if sel:
            driver_data = df[df['transporter_id'] == sel]
            c = generate_coaching(df, sel)
            
            if c:
                st.markdown("---")
                
                # Header with badges
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### Coaching: {c['driver_id']}")
                with col2:
                    badge_colors = {'Kritisch': '🔴', 'High': '🟠', 'Training': '🔵', 'Medium': '🟡', 'Multiple': '🟣'}
                    badges = " ".join([f"{badge_colors.get(t, '⚪')} **{t}**" for t in c['tags']])
                    st.markdown(badges)
                
                # =====================================================
                # DIE FAKTEN (DATEN) - Maximum Information
                # =====================================================
                st.markdown("#### 📊 DIE FAKTEN (DATEN)")
                
                # Key metrics in columns
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Concessions gesamt", c['total'])
                m2.metric("Wochen aktiv", c['weeks'])
                m3.metric("Trend", c['trend'])
                m4.metric("High-Value Items", c['hv'] if c['hv'] > 0 else "—")
                
                # Detailed breakdown
                st.markdown("**Detailanalyse:**")
                
                # Problem breakdown
                problem_cols = {
                    'Geo Distance > 25m': 'Geo-Fence Violations',
                    'Delivered to Household Member / Customer': 'Household Member (ohne echte Übergabe)',
                    'Delivery preferences not followed': 'Präferenzen ignoriert',
                    'Unattended Delivery & No Photo on Delivery': 'Ablage ohne Foto',
                    'Feedback False Scan Indicator': '🚨 False Scan (Betrug!)'
                }
                
                breakdown_data = []
                for col, label in problem_cols.items():
                    if col in driver_data.columns:
                        count = int(driver_data[col].sum())
                        if count > 0:
                            breakdown_data.append({'Kategorie': label, 'Anzahl': count})
                
                if breakdown_data:
                    bdf = pd.DataFrame(breakdown_data).sort_values('Anzahl', ascending=False)
                    st.dataframe(bdf, use_container_width=True, hide_index=True)
                
                # ZIP Code analysis
                if 'zip_code' in driver_data.columns:
                    zip_counts = driver_data.groupby('zip_code').size().sort_values(ascending=False)
                    top_zips = zip_counts.head(3)
                    st.markdown(f"**Hauptsächlich betroffene PLZ:** {', '.join([f'{z} ({c}x)' for z, c in top_zips.items()])}")
                
                # Weekly trend
                if 'year_week' in driver_data.columns:
                    weekly_counts = driver_data.groupby('year_week').size().sort_index()
                    trend_str = " → ".join([f"KW{w.split('-')[1]}: {cnt}" for w, cnt in weekly_counts.items()])
                    st.markdown(f"**Wöchentlicher Verlauf:** {trend_str}")
                
                # Tracking IDs
                if 'tracking_id' in driver_data.columns and len(driver_data) <= 20:
                    tracking_ids = driver_data['tracking_id'].tolist()
                    with st.expander(f"📦 Betroffene Tracking IDs ({len(tracking_ids)})"):
                        st.code(", ".join(str(t) for t in tracking_ids))
                
                st.markdown("---")
                
                # =====================================================
                # DAS PROBLEM (VERHALTEN)
                # =====================================================
                st.markdown("#### ⚠️ DAS PROBLEM (VERHALTEN)")
                
                if "False Scan" in str(c['tags']):
                    st.error(c['problem'])
                elif "High" in str(c['tags']) or "Kritisch" in str(c['tags']):
                    st.warning(c['problem'])
                else:
                    st.info(c['problem'])
                
                # Additional context based on data
                if c['counts'].get('DNR (Household Member)', 0) > 0:
                    st.markdown("""
                    **Root Cause Analyse:**
                    - Der Fahrer wählt 'Delivered to Household Member', macht aber keine echte Übergabe
                    - Das Paket wird unbeaufsichtigt abgelegt
                    - Da kein Foto gemacht wird, haben wir bei einem Verlust (DNR) keinen Beweis
                    - Das verhindert das 'Photo on Delivery' (POD) System
                    """)
                
                if c['counts'].get('Geo Distance / Group Stops', 0) > 0:
                    st.markdown("""
                    **Root Cause Analyse:**
                    - Fahrer scannt Pakete im Van ("Simultaneous Group Stops")
                    - Läuft dann zum Kunden → System registriert "Geo Distance > 25m"
                    - Mögliche Ursachen: Zeitdruck, falsches Training, oder GPS-Probleme
                    """)
                
                st.markdown("---")
                
                # =====================================================
                # COACHING FRAGEN (GESPRÄCHSLEITFADEN)
                # =====================================================
                st.markdown("#### 💬 COACHING FRAGEN (GESPRÄCHSLEITFADEN)")
                
                for i, q in enumerate(c['questions'], 1):
                    st.markdown(f"**{i}.** {q}")
                
                # Additional questions based on severity
                st.markdown("**Zusätzliche Fragen je nach Situation:**")
                additional_qs = []
                
                if c['hv'] > 0:
                    additional_qs.append("• Bei High-Value: Wo genau hast du das Paket abgelegt? War jemand in der Nähe?")
                
                if 'zip_code' in driver_data.columns:
                    top_zip = driver_data.groupby('zip_code').size().idxmax()
                    additional_qs.append(f"• Was ist besonders an PLZ {top_zip}? Gibt es dort Probleme?")
                
                if c['counts'].get('No Photo on Delivery', 0) > 0:
                    additional_qs.append("• Wenn du kein Foto machst, bezahlen wir das Paket sofort, wenn der Kunde sich beschwert. Wir brauchen das Foto.")
                
                for q in additional_qs:
                    st.markdown(q)
                
                st.markdown("---")
                
                # =====================================================
                # VEREINBARTE LÖSUNG (COMMITMENT)
                # =====================================================
                st.markdown("#### ✅ VEREINBARTE LÖSUNG (COMMITMENT)")
                st.success(c['commitment'])
                
                # Action items
                st.markdown("**Konkrete Maßnahmen:**")
                
                actions = []
                if "Household" in c['main_problem']:
                    actions = [
                        "☐ 'Household Member' NUR bei Augenkontakt/Übergabe auswählen",
                        "☐ Bei Ablage IMMER 'Safe Location' + Foto wählen",
                        "☐ Foto muss Paket UND Ablageort zeigen"
                    ]
                elif "Geo" in c['main_problem']:
                    actions = [
                        "☐ Scan ERST an der Haustür - niemals im Fahrzeug",
                        "☐ Bei Group Stops: Jedes Paket einzeln vor Ort scannen",
                        "☐ Bei GPS-Problemen: Gerät neustarten vor Tour"
                    ]
                elif "False Scan" in str(c['tags']):
                    actions = [
                        "☐ Sofortige Verwarnung dokumentieren",
                        "☐ Nächster Vorfall = HR-Eskalation",
                        "☐ Ride-along in nächster Woche"
                    ]
                else:
                    actions = [
                        "☐ Allgemeines Refresher-Training",
                        "☐ Follow-up Gespräch in 1 Woche",
                        "☐ Performance wird überwacht"
                    ]
                
                for action in actions:
                    st.markdown(action)
                
                st.markdown("---")
                
                # =====================================================
                # ROHDATEN
                # =====================================================
                with st.expander("📊 Vollständige Rohdaten für diesen Fahrer"):
                    st.dataframe(driver_data, use_container_width=True, hide_index=True)
                
                # =====================================================
                # COACHING PROTOKOLL EXPORT
                # =====================================================
                st.markdown("---")
                
                protocol = f"""COACHING PROTOKOLL
====================
Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Fahrer: {c['driver_id']}
Hauptproblem: {c['main_problem']}
Tags: {', '.join(c['tags'])}
FAKTEN
------
- {c['total']} Concessions in {c['weeks']} Wochen
- Trend: {c['trend']}
- High-Value Items: {c['hv']}
PROBLEM
-------
{c['problem']}
COACHING FRAGEN
---------------
{chr(10).join(f'- {q}' for q in c['questions'])}
VEREINBARTE LÖSUNG
------------------
{c['commitment']}
MASSNAHMEN
----------
{chr(10).join(actions)}
Unterschrift Fahrer: ___________________
Unterschrift Manager: ___________________
"""
                
                st.download_button(
                    "📥 Coaching-Protokoll herunterladen",
                    protocol,
                    file_name=f"coaching_{c['driver_id']}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
if __name__ == "__main__":
    main()
