"""
LTS Quality Management - UI Components
Reusable Streamlit components for enterprise-grade UI
"""

import streamlit as st
from typing import Optional, Union, List, Dict
from pathlib import Path


def load_custom_css():
    """Load the custom LTS theme CSS"""
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", icon: str = ""):
    """
    Render a styled page header.
    
    Args:
        title: Main page title
        subtitle: Optional subtitle/description
        icon: Optional emoji icon
    """
    header_html = f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0.25rem;">{icon} {title}</h1>
        {f'<p style="color: #718096; font-size: 1rem; margin-top: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_kpi_card(
    value: Union[str, int, float],
    label: str,
    delta: Optional[str] = None,
    delta_type: str = "neutral",  # "positive", "negative", "neutral"
    prefix: str = "",
    suffix: str = "",
    color: str = "primary"  # "primary", "success", "warning", "danger"
):
    """
    Render a styled KPI card with optional delta.
    
    Args:
        value: The main metric value
        label: Description label
        delta: Optional change indicator (e.g., "+5%")
        delta_type: Type of delta for coloring
        prefix: Text before value (e.g., "€")
        suffix: Text after value (e.g., "%")
        color: Card accent color
    """
    color_map = {
        "primary": "#0D47A1",
        "success": "#2E7D32",
        "warning": "#F9A825",
        "danger": "#C62828"
    }
    
    delta_color_map = {
        "positive": "#2E7D32",
        "negative": "#C62828",
        "neutral": "#718096"
    }
    
    accent_color = color_map.get(color, color_map["primary"])
    delta_color = delta_color_map.get(delta_type, delta_color_map["neutral"])
    
    delta_html = ""
    if delta:
        delta_icon = "↑" if delta_type == "positive" else "↓" if delta_type == "negative" else ""
        delta_html = f'<div style="color: {delta_color}; font-size: 0.85rem; margin-top: 0.5rem;">{delta_icon} {delta}</div>'
    
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-left: 4px solid {accent_color};
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: box-shadow 0.2s ease;
    ">
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {accent_color};
            line-height: 1.2;
        ">{prefix}{value}{suffix}</div>
        <div style="
            font-size: 0.85rem;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.5rem;
        ">{label}</div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_empty_state(
    icon: str = "📊",
    title: str = "Keine Daten verfügbar",
    description: str = "Laden Sie Daten hoch, um Analysen anzuzeigen.",
    action_text: str = "",
    action_key: str = ""
) -> bool:
    """
    Render a beautiful empty state placeholder.
    
    Args:
        icon: Emoji icon to display
        title: Main message title
        description: Helpful description
        action_text: Optional button text
        action_key: Unique key for the button
        
    Returns:
        True if action button was clicked (if provided)
    """
    empty_html = f"""
    <div style="
        text-align: center;
        padding: 3rem 2rem;
        background-color: #FFFFFF;
        border: 2px dashed #E2E8F0;
        border-radius: 16px;
        margin: 1rem 0;
    ">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">{icon}</div>
        <div style="
            font-size: 1.25rem;
            font-weight: 600;
            color: #1A1A2E;
            margin-bottom: 0.5rem;
        ">{title}</div>
        <div style="
            color: #718096;
            font-size: 0.95rem;
            max-width: 400px;
            margin: 0 auto;
        ">{description}</div>
    </div>
    """
    st.markdown(empty_html, unsafe_allow_html=True)
    
    if action_text and action_key:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button(action_text, key=action_key, use_container_width=True)
    return False


def render_status_badge(
    status: str,
    size: str = "normal"  # "small", "normal", "large"
) -> str:
    """
    Render a status badge/pill.
    
    Args:
        status: One of "high", "medium", "low", or custom text
        size: Badge size
        
    Returns:
        HTML string for the badge
    """
    status_lower = status.lower()
    
    style_map = {
        "high": {"bg": "#C62828", "text": "#FFFFFF"},
        "hoch": {"bg": "#C62828", "text": "#FFFFFF"},
        "medium": {"bg": "#F9A825", "text": "#333333"},
        "mittel": {"bg": "#F9A825", "text": "#333333"},
        "low": {"bg": "#2E7D32", "text": "#FFFFFF"},
        "niedrig": {"bg": "#2E7D32", "text": "#FFFFFF"},
        "success": {"bg": "#2E7D32", "text": "#FFFFFF"},
        "warning": {"bg": "#F9A825", "text": "#333333"},
        "error": {"bg": "#C62828", "text": "#FFFFFF"},
    }
    
    size_map = {
        "small": "0.2rem 0.5rem; font-size: 0.7rem",
        "normal": "0.3rem 0.75rem; font-size: 0.8rem",
        "large": "0.4rem 1rem; font-size: 0.9rem"
    }
    
    style = style_map.get(status_lower, {"bg": "#718096", "text": "#FFFFFF"})
    padding = size_map.get(size, size_map["normal"])
    
    return f"""
    <span style="
        background-color: {style['bg']};
        color: {style['text']};
        padding: {padding};
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    ">{status.upper()}</span>
    """


def render_section_header(title: str, icon: str = "", help_text: str = ""):
    """
    Render a section header with optional help tooltip.
    
    Args:
        title: Section title
        icon: Optional emoji
        help_text: Optional help tooltip text
    """
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(f"### {icon} {title}")
    if help_text:
        with col2:
            st.markdown(f'<span title="{help_text}" style="cursor: help; font-size: 1.2rem;">ℹ️</span>', 
                       unsafe_allow_html=True)


def render_action_card(
    title: str,
    description: str,
    icon: str,
    urgency: str = "normal",  # "urgent", "normal", "low"
    action_items: List[str] = None
):
    """
    Render an action/recommendation card.
    
    Args:
        title: Card title
        description: Main description
        icon: Emoji icon
        urgency: Urgency level
        action_items: List of action items
    """
    urgency_colors = {
        "urgent": "#FFEBEE",
        "normal": "#FFF8E1",
        "low": "#E8F5E9"
    }
    
    bg_color = urgency_colors.get(urgency, urgency_colors["normal"])
    
    actions_html = ""
    if action_items:
        items = "".join([f"<li style='margin: 0.25rem 0;'>{item}</li>" for item in action_items])
        actions_html = f"<ul style='margin: 0.75rem 0 0 0; padding-left: 1.5rem;'>{items}</ul>"
    
    card_html = f"""
    <div style="
        background-color: {bg_color};
        border-radius: 10px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    ">
        <div style="display: flex; align-items: flex-start; gap: 1rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1A1A2E; font-size: 1rem;">{title}</div>
                <div style="color: #4A5568; font-size: 0.9rem; margin-top: 0.25rem;">{description}</div>
                {actions_html}
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_stat_row(stats: List[Dict]):
    """
    Render a row of small statistics.
    
    Args:
        stats: List of dicts with 'label' and 'value' keys
    """
    cols = st.columns(len(stats))
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.25rem; font-weight: 600; color: #0D47A1;">{stat.get('value', '-')}</div>
                <div style="font-size: 0.75rem; color: #718096; text-transform: uppercase;">{stat.get('label', '')}</div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# GERMAN TRANSLATIONS
# =============================================================================

TRANSLATIONS = {
    # Navigation & Tabs
    "Overview": "Überblick",
    "Depot Comparison": "Depot-Vergleich",
    "Risk Analysis": "Risikoanalyse",
    "Pattern Recognition": "Mustererkennung",
    "Customer Abuse": "Missbrauchserkennung",
    "Driver Profiles": "Fahrerprofile",
    "Data Management": "Datenverwaltung",
    
    # Metrics & Labels
    "Total Deliveries": "Gesamtzustellungen",
    "Concessions": "Konzessionen",
    "Concession Rate": "Konzessionsrate",
    "Total Cost": "Gesamtkosten",
    "Drivers": "Fahrer",
    "Active Drivers": "Aktive Fahrer",
    "High Risk": "Hochrisiko",
    "Medium Risk": "Mittleres Risiko",
    "Low Risk": "Niedriges Risiko",
    
    # Actions
    "Upload Data": "Daten hochladen",
    "Download Report": "Bericht herunterladen",
    "Filter": "Filter",
    "Select": "Auswählen",
    "Apply": "Anwenden",
    "Reset": "Zurücksetzen",
    
    # Status & Messages
    "No data available": "Keine Daten verfügbar",
    "Loading...": "Wird geladen...",
    "Success": "Erfolgreich",
    "Warning": "Warnung",
    "Error": "Fehler",
    
    # Time
    "Today": "Heute",
    "Yesterday": "Gestern",
    "This Week": "Diese Woche",
    "Last Week": "Letzte Woche",
    "This Month": "Diesen Monat",
    "Last Month": "Letzten Monat",
}


def t(text: str) -> str:
    """
    Translate text to German.
    
    Args:
        text: English text key
        
    Returns:
        German translation or original text if not found
    """
    return TRANSLATIONS.get(text, text)
