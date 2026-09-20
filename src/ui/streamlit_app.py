"""AI Invoice Auditor — Main Streamlit Application Entry Point.

Configures enterprise layout, injects global theme variables (Light & Dark),
sets up multipage routing (/dashboard, /invoice?id=...),
and hosts the bottom-right floating action button for the RAG Copilot.
"""
import streamlit as st
from streamlit_theme import st_theme

# Configure page layout and metadata with icon (must be first Streamlit command)
st.set_page_config(
    page_title="AI Invoice Auditor",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Detect Streamlit theme dynamically via st_theme
theme = st_theme()
theme_base = "light"
if theme and isinstance(theme, dict) and "base" in theme and theme["base"]:
    theme_base = theme["base"]
    st.session_state["theme_base"] = theme_base
elif "theme_base" in st.session_state:
    theme_base = st.session_state["theme_base"]

is_dark = (theme_base == "dark")

# Palette configuration based on theme['base']
if is_dark:
    t_bg = "#0e1117"
    t_card_bg = "#1e212b"
    t_subcard_bg = "#161922"
    t_text_primary = "#fafafa"
    t_text_secondary = "#a3a8b8"
    t_text_muted = "#8b949e"
    t_border = "#31333f"
    t_row_divider = "#2a2d38"
    t_code_bg = "#151821"
    t_code_border = "#2e323e"
    t_tag_bg = "#262935"
    t_tag_text = "#e2e8f0"
    t_dialog_bg = "#161922"
    t_dialog_border = "#31333f"
    t_chat_bubble_bg = "#222531"
    t_chat_bubble_border = "#31333f"
    t_chat_bubble_text = "#fafafa"
    t_chat_form_bg = "#1a1d26"
    t_pill_bg = "rgba(99, 102, 241, 0.2)"
    t_pill_border = "rgba(99, 102, 241, 0.45)"
    t_pill_text = "#c7d2fe"
    t_alert_warn_bg = "rgba(245, 158, 11, 0.12)"
    t_alert_warn_border = "#f59e0b"
    t_alert_warn_text = "#fde68a"
    t_alert_danger_bg = "rgba(239, 68, 68, 0.12)"
    t_alert_danger_border = "#ef4444"
    t_alert_danger_text = "#fecaca"
    t_card_shadow = "0 2px 6px rgba(0,0,0,0.35)"
else:
    t_bg = "#ffffff"
    t_card_bg = "#ffffff"
    t_subcard_bg = "#f8fafc"
    t_text_primary = "#0f172a"
    t_text_secondary = "#64748b"
    t_text_muted = "#94a3b8"
    t_border = "#e2e8f0"
    t_row_divider = "#f1f5f9"
    t_code_bg = "#f8fafc"
    t_code_border = "#cbd5e1"
    t_tag_bg = "#f1f5f9"
    t_tag_text = "#475569"
    t_dialog_bg = "#ffffff"
    t_dialog_border = "#e2e8f0"
    t_chat_bubble_bg = "#f8fafc"
    t_chat_bubble_border = "#e2e8f0"
    t_chat_bubble_text = "#1e293b"
    t_chat_form_bg = "#f8fafc"
    t_pill_bg = "rgba(99, 102, 241, 0.08)"
    t_pill_border = "rgba(99, 102, 241, 0.22)"
    t_pill_text = "#4338ca"
    t_alert_warn_bg = "rgba(245, 158, 11, 0.08)"
    t_alert_warn_border = "#f59e0b"
    t_alert_warn_text = "#92400e"
    t_alert_danger_bg = "rgba(239, 68, 68, 0.08)"
    t_alert_danger_border = "#ef4444"
    t_alert_danger_text = "#991b1b"
    t_card_shadow = "0 1px 3px rgba(0,0,0,0.03)"

# Global Enterprise CSS & Layout Injection with Dynamic Theme Values
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}

    /* Top padding so headers never get hidden under Streamlit's top controls */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 1400px !important;
    }}

    /* Hide default Streamlit sidebar clutter */
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}

    /* Header styling */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* Streamlit Theme CSS Custom Properties */
    :root, .stApp {{
        --copilot-h: min(650px, calc(100vh - 32px));
        --st-background-color: {t_bg};
        --st-secondary-background-color: {t_card_bg};
        --st-text-color: {t_text_primary};
        --st-text-secondary: {t_text_secondary};
        --st-text-muted: {t_text_muted};
        --st-subcard-background: {t_subcard_bg};
        --st-heading-color: {t_text_primary};
        --st-border-color: {t_border};
        --st-font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --st-code-background-color: {t_code_bg};
        --st-code-text-color: {t_text_primary};
    }}

    .stApp {{
        background-color: {t_bg} !important;
        color: {t_text_primary} !important;
    }}

    @keyframes spinStepProgress {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* Expander theming & matching rounded corners */
    [data-testid="stExpander"] {{
        background-color: {t_card_bg} !important;
        padding-bottom: 4px !important;
        transition: all 0.2s ease !important;
        overflow: hidden !important;
    }}

    [data-testid="stExpander"]:hover {{
        border-color: rgba(99, 102, 241, 0.4) !important;
    }}

    /* Expander summary layout: full width flex with name left, duration right, matching corners */
    [data-testid="stExpander"] summary {{
        color: {t_text_primary} !important;
        display: flex !important;
        align-items: center !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        border-radius: 7px !important;
        overflow: hidden !important;
    }}

    [data-testid="stExpander"][open] summary {{
        border-bottom-left-radius: 0 !important;
        border-bottom-right-radius: 0 !important;
    }}

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        border-bottom-left-radius: 7px !important;
        border-bottom-right-radius: 7px !important;
        overflow: hidden !important;
    }}

    /* Status-specific icon colors (LEFT SIDE) */
    [data-testid="stExpander"]:has([data-status="success"]) summary [data-testid="stExpanderIcon"],
    [data-testid="stExpander"]:has([data-status="success"]) summary [data-testid="stExpanderIconCheck"],
    [data-testid="stExpander"]:has([data-status="success"]) summary [data-testid="stExpanderStepIcon"],
    [data-testid="stExpander"]:has([data-status="success"]) summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"]:has([data-status="success"]) summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stExpander"]:has([data-status="success"]) summary svg:not(:first-child),
    [data-testid="stExpander"]:has([data-status="success"]) summary i:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIconCheck"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderStepIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="success"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary svg:not(:first-child) {{
        color: #10b981 !important;
    }}

    [data-testid="stExpander"]:has([data-status="failed"]) summary [data-testid="stExpanderIcon"],
    [data-testid="stExpander"]:has([data-status="failed"]) summary [data-testid="stExpanderIconError"],
    [data-testid="stExpander"]:has([data-status="failed"]) summary [data-testid="stExpanderStepIcon"],
    [data-testid="stExpander"]:has([data-status="failed"]) summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"]:has([data-status="failed"]) summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stExpander"]:has([data-status="failed"]) summary svg:not(:first-child),
    [data-testid="stExpander"]:has([data-status="failed"]) summary i:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIconError"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderStepIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="failed"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary svg:not(:first-child) {{
        color: #ef4444 !important;
    }}

    [data-testid="stExpander"]:has([data-status="warning"]) summary [data-testid="stExpanderIcon"],
    [data-testid="stExpander"]:has([data-status="warning"]) summary [data-testid="stExpanderStepIcon"],
    [data-testid="stExpander"]:has([data-status="warning"]) summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"]:has([data-status="warning"]) summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stExpander"]:has([data-status="warning"]) summary svg:not(:first-child),
    [data-testid="stExpander"]:has([data-status="warning"]) summary i:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="warning"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="warning"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderStepIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="warning"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="warning"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="warning"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary svg:not(:first-child) {{
        color: #f59e0b !important;
    }}

    [data-testid="stExpander"]:has([data-status="in_progress"]) summary [data-testid="stExpanderIcon"],
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary [data-testid="stExpanderIconSpinner"],
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary [data-testid="stExpanderStepIcon"],
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary svg:not(:first-child),
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary i:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIconSpinner"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderStepIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary svg:not(:first-child) {{
        color: #3b82f6 !important;
        animation: spinStepProgress 1.4s linear infinite !important;
        display: inline-flex !important;
    }}

    [data-testid="stExpander"]:has([data-status="waiting"]) summary [data-testid="stExpanderIcon"],
    [data-testid="stExpander"]:has([data-status="waiting"]) summary [data-testid="stExpanderStepIcon"],
    [data-testid="stExpander"]:has([data-status="waiting"]) summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"]:has([data-status="waiting"]) summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stExpander"]:has([data-status="waiting"]) summary svg:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="waiting"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="waiting"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stExpanderStepIcon"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="waiting"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stElementContainer"]:has(.step-marker[data-status="waiting"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary span.material-symbols-rounded:not(:first-child),
    [data-testid="stElementContainer"]:has(.step-marker[data-status="waiting"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary svg:not(:first-child) {{
        color: #94a3b8 !important;
    }}

    /* Markdown container inside summary stretches full width */
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] {{
        flex: 1 1 auto !important;
        width: 100% !important;
    }}

    /* Name on left-most corner, duration badge pushed to right-most corner */
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {{
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        margin: 0 !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        color: {t_text_primary} !important;
    }}

    /* Step duration on right-most corner: clean plain text, NO box, normal secondary color */
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p code,
    [data-testid="stExpander"] summary code {{
        margin-left: auto !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        font-family: inherit !important;
        padding: 0 !important;
        border-radius: 0 !important;
        background: transparent !important;
        color: {t_text_secondary} !important;
        border: none !important;
        box-shadow: none !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        letter-spacing: 0.01em !important;
    }}

    /* Only for processing (in_progress): spinning refresh icon on left side of timer without any box */
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary [data-testid="stMarkdownContainer"] p code::before,
    [data-testid="stExpander"]:has([data-status="in_progress"]) summary code::before,
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p code::before,
    [data-testid="stElementContainer"]:has(.step-marker[data-status="in_progress"]) + [data-testid="stElementContainer"] [data-testid="stExpander"] summary code::before {{
        content: "↻" !important;
        display: inline-block !important;
        margin-right: 5px !important;
        font-size: 0.86rem !important;
        line-height: 1 !important;
        animation: spinStepProgress 1.2s linear infinite !important;
        color: #3b82f6 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform-origin: center center !important;
    }}

    /* Completely eliminate huge gap above tabs when expander opens */
    [data-testid="stExpanderDetails"] {{
        padding-top: 2px !important;
        padding-bottom: 12px !important;
        padding-left: 14px !important;
        padding-right: 14px !important;
    }}

    /* Step Timeline Container: tight 4px spacing between steps */
    [data-testid="stVerticalBlock"]:has(#steps-timeline-marker) {{
        gap: 6px !important;
    }}

    [data-testid="stVerticalBlock"]:has(#steps-timeline-marker) > [data-testid="stElementContainer"]:has(.step-marker),
    [data-testid="stVerticalBlock"]:has(#steps-timeline-marker) > [data-testid="stElementContainer"]:has(#steps-timeline-marker) {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 0 !important;
    }}

    [data-testid="stVerticalBlock"]:has(#steps-timeline-marker) [data-testid="stExpander"] {{
        margin-bottom: 0 !important;
        margin-top: 0 !important;
    }}

    /* Hide the step-marker container before the expander without taking any vertical space */
    [data-testid="stElementContainer"]:has(.step-marker) {{
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    [data-testid="stExpanderDetails"] [data-testid="stTabs"] {{
        margin-top: 0 !important;
        padding-top: 0 !important;
    }}

    [data-testid="stExpanderDetails"] [data-baseweb="tab-list"] {{
        margin-top: 0 !important;
        padding-top: 2px !important;
        margin-bottom: 12px !important;
    }}

    /* Tabs theming */
    button[data-baseweb="tab"] {{
        color: {t_text_secondary} !important;
        font-weight: 500 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #6366f1 !important;
        border-bottom-color: #6366f1 !important;
        font-weight: 700 !important;
    }}

    .audit-title {{
        color: {t_text_primary} !important;
        margin: 0;
        font-size: 2.4rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }}
    .audit-subtitle {{
        color: {t_text_secondary} !important;
        margin: 0 0 6px 0;
        font-size: 0.88rem;
    }}
    .kpi-card {{
        background-color: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: {t_card_shadow};
    }}
    .kpi-card-success {{
        border-left: 4px solid #10b981 !important;
    }}
    .kpi-card-warning {{
        border-left: 4px solid #f59e0b !important;
    }}
    .kpi-card-info {{
        border-left: 4px solid #3b82f6 !important;
    }}
    .kpi-card-danger {{
        border-left: 4px solid #ef4444 !important;
    }}
    .kpi-label {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {t_text_secondary} !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .kpi-val {{
        font-size: 2.5rem;
        font-weight: 600;
        color: {t_text_primary} !important;
        line-height: 1.1;
    }}
    .inv-table-header {{
        display: grid;
        grid-template-columns: 1.5fr 2.4fr 1.4fr 1.2fr 1.7fr 1.4fr;
        gap: 12px;
        padding: 13px 18px;
        background-color: {t_subcard_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        color: {t_text_secondary} !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        align-items: center;
        justify-items: center;
        box-sizing: border-box;
        margin-bottom: 13px;
    }}

    /* Reduce gap between table items to exactly 2px */
    [data-testid="stVerticalBlock"]:has(#inv-table-body-marker),
    div[data-testid="stVerticalBlock"]:has(.inv-table-row-marker) {{
        gap: 2px !important;
    }}

    [data-testid="stVerticalBlock"]:has(#inv-table-body-marker) > div,
    [data-testid="stVerticalBlock"]:has(#inv-table-body-marker) [data-testid="stElementContainer"] {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}

    div:has(> div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker)) {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}

    /* Entire Table Row: Total Borders for every item with 2px gap */
    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) {{
        background-color: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 8px !important;
        padding: 6px 18px !important;
        min-height: 56px !important;
        align-items: center !important;
        box-sizing: border-box !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        transition: background-color 0.15s ease !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker):hover {{
        background-color: {t_subcard_bg} !important;
    }}

    /* Vertical centering for all columns in table rows */
    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) > div[data-testid="stColumn"] {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        min-height: 48px !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Column 2 (Vendor & PO): center aligned */
    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) > div[data-testid="stColumn"]:nth-child(2) {{
        align-items: center !important;
        text-align: center !important;
    }}

    /* Column 6: Action Button Perfectly Centered */
    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) > div[data-testid="stColumn"]:nth-child(6) {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) [data-testid="stElementContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) .stButton {{
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.inv-table-row-marker) .stButton > button {{
        width: 100% !important;
        height: 36px !important;
        margin: 0 !important;
        padding: 0 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}

    .inv-cell-primary {{
        font-weight: 700;
        color: {t_text_primary} !important;
        font-size: 0.9rem;
        line-height: 1;
    }}
    .inv-cell-secondary {{
        font-weight: 600;
        color: {t_text_secondary} !important;
        font-size: 0.9rem;
        line-height: 1.2;
        margin-top: 8px;
    }}
    .inv-cell-muted {{
        font-size: 0.85rem;
        color: {t_text_muted} !important;
        font-family: monospace;
        margin-top: 3px;
        margin-bottom:7px;
    }}
    .inv-cell-amount {{
        font-weight: 600;
        color: {t_text_primary} !important;
        font-size: 0.95rem;
        font-family: monospace;
    }}
    .inv-empty-state {{
        text-align: center;
        padding: 48px;
        background-color: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-top: none;
        border-radius: 0 0 8px 8px;
        color: {t_text_muted} !important;
        font-size: 0.9rem;
    }}
    .pipeline-banner {{
        background-color: {t_card_bg} !important;
        border-top: 1px solid {t_border} !important;
        border-right: 1px solid {t_border} !important;
        border-bottom: 1px solid {t_border} !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
        padding: 20px 24px;
        box-shadow: none !important;
        margin-bottom: 28px;
    }}
    .pipeline-banner.status-validated {{
        border-left: 4px solid #10b981 !important;
        border-left-color: #10b981 !important;
    }}
    .pipeline-banner.status-processing {{
        border-left: 4px solid #3b82f6 !important;
        border-left-color: #3b82f6 !important;
    }}
    .pipeline-banner.status-review {{
        border-left: 4px solid #f59e0b !important;
        border-left-color: #f59e0b !important;
    }}
    .pipeline-banner.status-failed {{
        border-left: 4px solid #ef4444 !important;
        border-left-color: #ef4444 !important;
    }}
    .pipeline-tag {{
        font-family: monospace;
        font-size: 0.8rem;
        background-color: {t_tag_bg} !important;
        border: 1px solid {t_border} !important;
        color: {t_tag_text} !important;
        padding: 2px 8px;
        border-radius: 6px;
    }}
    .audit-card {{
        background-color: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        box-shadow: {t_card_shadow};
    }}
    .audit-card-code {{
        font-size: 0.8rem;
        color: {t_text_secondary} !important;
        line-height: 1.45;
        font-family: monospace;
        background-color: {t_code_bg} !important;
        padding: 8px 10px;
        border-radius: 6px;
        border: 1px solid {t_code_border} !important;
        border-left: 3px solid #6366f1 !important;
    }}
    .themed-box {{
        background-color: {t_card_bg} !important;
        color: {t_text_primary} !important;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid {t_border} !important;
        font-family: var(--st-font);
    }}
    .artifact-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 12px;
        background-color: {t_subcard_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 6px;
        margin-bottom: 6px;
    }}
    .agent-trace-step {{
        display: flex;
        flex-direction: column;
        margin-bottom: 8px;
        padding: 8px 12px;
        background-color: {t_subcard_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 8px;
        border-left: 3px solid #6366f1 !important;
    }}
    .audit-alert-warning {{
        background-color: {t_alert_warn_bg} !important;
        border: 1px solid {t_alert_warn_border} !important;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 24px;
        color: {t_alert_warn_text} !important;
    }}
    .audit-alert-danger {{
        background-color: {t_alert_danger_bg} !important;
        border: 1px solid {t_alert_danger_border} !important;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 24px;
        color: {t_alert_danger_text} !important;
    }}

    /* Floating Action Button (FAB) */
    @keyframes fabPulseGlow {{
        0% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7), 0 8px 24px -4px rgba(79, 70, 229, 0.6); }}
        70% {{ box-shadow: 0 0 0 14px rgba(99, 102, 241, 0), 0 8px 24px -4px rgba(79, 70, 229, 0.6); }}
        100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0), 0 8px 24px -4px rgba(79, 70, 229, 0.6); }}
    }}

    div:has(#fab-marker) + div,
    div:has(#fab-marker) + div [data-testid="stVerticalBlock"] {{
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        left: auto !important;
        top: auto !important;
        width: 60px !important;
        height: 60px !important;
        z-index: 999999 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }}

    div:has(#fab-marker) + div .stButton {{
        position: static !important;
        width: 60px !important;
        height: 60px !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }}

    div:has(#fab-marker) + div button {{
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 60px !important;
        height: 60px !important;
        min-width: 60px !important;
        min-height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
        color: #ffffff !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        z-index: 999999 !important;
        padding: 0 !important;
        margin: 0 !important;
        animation: fabPulseGlow 3s infinite !important;
    }}

    div:has(#fab-marker) + div button:hover {{
        transform: scale(1.08) translateY(-2px) !important;
        box-shadow: 0 14px 30px -4px rgba(79, 70, 229, 0.75) !important;
    }}

    div:has(#fab-marker) + div button [data-testid="stIconMaterial"] {{
        font-size: 28px !important;
        color: #ffffff !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* ============================================================
       COPILOT DIALOG DOCKING — pure CSS, structural, no JS tagging.

       :has() matches the real dialog panel the instant it exists in the
       DOM (same paint as everything else), so there is no frame where
       Streamlit's default centered dialog is visible before our styling
       applies. No polling, no iframe, no flash.
       ============================================================ */

    /* Root: pinned to all four edges of the dialog panel (inside its 12px padding) */
    div[data-testid="stDialog"] .st-key-copilot_root {{
        position: absolute !important;
        top: 12px !important;
        bottom: 12px !important;
        left: 12px !important;
        right: 12px !important;
        width: auto !important;
        height: auto !important;
        max-height: none !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}

    /* Overlay: dims the page and docks its content bottom-right.
       Scoped with :has() so only OUR dialog (the copilot) gets this
       treatment — any other st.dialog in the app is unaffected. */
     div[data-testid="stDialog"]:has(.st-key-copilot_root) {{
        position: fixed !important;
        inset: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
        background-color: rgba(15, 23, 42, 0.45) !important;
        z-index: 1000000 !important;
        overflow: hidden !important;
    }}

    /* Any wrapper div sitting between the overlay and the real dialog panel
       collapses out of the box tree structurally, so the panel becomes a
       direct flex item of the overlay — found purely by structure, no
       JS-added class required. */
    div[data-testid="stDialog"]:has(.st-key-copilot_root)
        div:has(.st-key-copilot_root):not([role="dialog"]):not([aria-modal="true"]) {{
        display: contents !important;
    }}
 /* The real dialog panel: pinned to the bottom-right corner with fixed
       offsets. Locked to its final horizontal position from the very
       first frame — only a small vertical rise animates. */
    div[data-testid="stDialog"] [role="dialog"]:has(.st-key-copilot_root),
    div[data-testid="stDialog"] [aria-modal="true"]:has(.st-key-copilot_root) {{
        position: absolute !important;
        top: auto !important;
        left: auto !important;
        right: 16px !important;
        bottom: 16px !important;
        margin: 0 !important;
        width: 540px !important;
        max-width: calc(100% - 32px) !important;
        height: var(--copilot-h) !important;
        max-height: calc(100% - 32px) !important;
        padding: 12px !important;
        box-sizing: border-box !important;
        border-radius: 18px !important;
        background: {t_dialog_bg} !important;
        color: {t_text_primary} !important;
        border: 1px solid {t_dialog_border} !important;
        box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 0, 0, 0.06) !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        animation: drawerSlideIn 0.32s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }}

    @keyframes drawerSlideIn {{
        0%   {{ opacity: 0; transform: translateY(40px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Top and bottom: natural height, pinned */
    div[data-testid="stDialog"] .st-key-copilot_root > .st-key-copilot_top,
    div[data-testid="stDialog"] .st-key-copilot_root > .st-key-copilot_bottom,
    div[data-testid="stDialog"] .st-key-copilot_root > :has(> .st-key-copilot_top),
    div[data-testid="stDialog"] .st-key-copilot_root > :has(> .st-key-copilot_bottom) {{
        flex: 0 0 auto !important;
    }}

    /* Middle (or its wrapper): takes all remaining height */
    div[data-testid="stDialog"] .st-key-copilot_root > .st-key-copilot_body,
    div[data-testid="stDialog"] .st-key-copilot_root > :has(> .st-key-copilot_body) {{
        flex: 1 1 0px !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
    }}

    /* Normalize internal dialog content padding: eliminates large horizontal gutters */
    div[data-testid="stDialog"] [data-testid="stDialogContent"],
    div[data-testid="stDialog"] > div[role="dialog"] > div,
    div[data-testid="stDialog"] > div[role="dialog"] > div > div {{
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}

    /* History Popover Dropdown Styling */
    div[data-testid="stPopoverBody"] {{
        background: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 12px !important;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.3) !important;
        padding: 10px 12px !important;
        width: 320px !important;
        max-width: 90vw !important;
        z-index: 1000005 !important;
    }}

    /* Tighten vertical gap between thread rows */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {{
        gap: 3px !important;
    }}

    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div,
    div[data-testid="stPopoverBody"] [data-testid="stElementContainer"] {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}

    div[data-testid="stPopoverBody"] [data-testid="stHorizontalBlock"] {{
        gap: 6px !important;
        margin: 0 !important;
        padding: 0 !important;
        align-items: center !important;
    }}

    div[data-testid="stPopoverBody"] .stButton {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    div[data-testid="stPopoverBody"] div[data-testid="stColumn"]:first-child button {{
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 0.82rem !important;
        padding: 6px 10px !important;
        min-height: 34px !important;
        height: 34px !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }}

    div[data-testid="stPopoverBody"] div[data-testid="stColumn"]:last-child button {{
        background: transparent !important;
        border: none !important;
        color: var(--st-text-muted, #94a3b8) !important;
        padding: 0 !important;
        min-height: 34px !important;
        height: 34px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 8px !important;
    }}

    div[data-testid="stPopoverBody"] div[data-testid="stColumn"]:last-child button:hover {{
        color: #ef4444 !important;
        background: rgba(239, 68, 68, 0.12) !important;
    }}

    /* Hide native Dialog Header duplicates */
    div[role="dialog"] > div:first-child:has(button[aria-label="Close"]),
    div[role="dialog"] > div:first-child:has(h2),
    div[role="dialog"] button[aria-label="Close"],
    div[data-testid="stDialog"] button[aria-label="Close"],
    div[data-testid="stDialog"] h2,
    div[data-testid="stDialogHeader"],
    div[data-testid="stModalHeader"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }}

    /* ============================================================
       COPILOT DIALOG: 3-section flex layout
       Top / Body / Bottom
       ============================================================ */

    /* TOP + BOTTOM: natural height, never shrink or scroll */
    div[data-testid="stDialog"] .st-key-copilot_top,
    div[data-testid="stDialog"] .st-key-copilot_bottom,
    div[data-testid="stDialog"] div:has(.st-key-copilot_top):not(:has(.st-key-copilot_body)),
    div[data-testid="stDialog"] div:has(.st-key-copilot_bottom):not(:has(.st-key-copilot_body)) {{
        flex: 0 0 auto !important;
        min-height: auto !important;
        overflow: visible !important;
    }}

    /* ============================================================
       TOP SECTION
       3 columns: New | History | Close
       ============================================================ */

    div[data-testid="stDialog"] .st-key-copilot_top {{
        padding: 2px 0 10px 0 !important;
    }}

    /* Top row */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 8px !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* All three columns */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"] {{
        min-width: 0 !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Column 1: New */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"]:nth-child(1) {{
        flex: 0 0 auto !important;
        width: auto !important;
    }}

    /* Column 2: History / Thread title */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"]:nth-child(2) {{
        flex: 1 1 auto !important;
        width: auto !important;
        min-width: 0 !important;
    }}

    /* Ensure middle content fits */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"]:nth-child(2) > * {{
        min-width: 0 !important;
        max-width: 100% !important;
    }}

    /* Column 3: Close button at far right */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"]:nth-child(3) {{
        flex: 0 0 auto !important;
        width: auto !important;
        margin-left: auto !important;
        justify-content: flex-end !important;
    }}

    /* ============================================================
       TOP BUTTONS
       ============================================================ */

    div[data-testid="stDialog"] .st-key-copilot_top button {{
        min-height: 36px !important;
        height: 36px !important;
        padding: 0 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
    }}

    /* Close button: compact and right-aligned */
    div[data-testid="stDialog"] .st-key-copilot_top
    [data-testid="stColumn"]:nth-child(3) button {{
        width: 40px !important;
        min-width: 40px !important;
        padding: 0 !important;
    }}

    /* Material icons */
    div[data-testid="stDialog"] .st-key-copilot_top button
    [data-testid="stIconMaterial"],
    div[data-testid="stDialog"] .st-key-copilot_top button
    span.material-symbols-rounded {{
        font-size: 1.25rem !important;
        width: 1.25rem !important;
        height: 1.25rem !important;
        line-height: 1 !important;
    }}


    /* Thread title: same look as the input box below, not a button */
    .thread-field {{
        display: flex;
        align-items: center;
        gap: 8px;
        width: 100%;
        padding: 0 12px;
        box-sizing: border-box;
        background-color: {t_chat_form_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 8px;
        color: {t_text_primary} !important;
        font-size: 0.85rem;
        font-weight: 600;
        min-width: 0;
        cursor: default;
    }}
    .thread-field svg {{ flex-shrink: 0; }}
    .thread-field span {{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        min-width: 0;
    }}

    /* MIDDLE: takes ALL remaining space between top and bottom, scrolls smoothly */
    div[data-testid="stDialog"] .st-key-copilot_body {{
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 0px !important;
        min-height: 0 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        scroll-behavior: smooth !important;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        gap: 14px !important;
        padding: 8px 6px 8px 2px !important;
    }}

    /* User message */
    .chat-user-bubble {{
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        width: fit-content;
        max-width: 86%;
        margin-left: auto;
        margin-bottom:10px;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px;
        font-size: 0.95rem;
        line-height: 1.4;
        word-break: break-word;
    }}

    /* Assistant response card (one card per response) */
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] {{
        background-color: {t_card_bg} !important;
        border: 1px solid {t_border} !important;
        border-radius: 16px 16px 16px 4px !important;
        padding: 14px 16px !important;
        gap: 12px !important;
        box-shadow: {t_card_shadow};
        margin-right: 3%;
    }}

    .bot-head {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom:8px;
    }}
    .bot-avatar {{
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .bot-name {{
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        color: {t_pill_text} !important;
    }}

    /* Answer typography */
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] [data-testid="stMarkdownContainer"] p {{
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0 0 0.55rem 0;
        color: {t_chat_bubble_text};
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] [data-testid="stMarkdownContainer"] p:last-child {{
        margin-bottom: 0;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] ul,
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] ol {{
        margin: 0.25rem 0 0.6rem 0;
        padding-left: 1.15rem;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] li {{
        font-size: 0.86rem;
        line-height: 1.55;
        margin-bottom: 0.3rem;
        color: {t_chat_bubble_text};
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] strong {{
        font-weight: 700;
        color: {t_text_primary};
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_answer_"] code {{
        font-size: 0.9rem;
        padding: 1px 6px;
        border-radius: 6px;
        background: {t_code_bg};
        border: 1px solid {t_code_border};
    }}

    /* Expanders inside a response: compact, rounded, borderless */
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stExpander"] {{
        border-radius: 4px !important;
        background-color: {t_subcard_bg} !important;
        padding: 0 !important;
        margin-bottom: -6px !important;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stExpander"] summary {{
        padding: 8px 12px !important;
        margin: 0 !important;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {{
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stExpanderDetails"] {{
        padding: 4px 12px 12px 12px !important;
    }}

    /* Reflection metrics as small tiles */
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stMetric"] {{
        background-color: {t_card_bg};
        border: 1px solid {t_border};
        border-radius: 8px;
        padding: 8px 10px;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stMetricLabel"] p {{
        font-size: 0.64rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: {t_text_secondary} !important;
    }}
    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] [data-testid="stMetricValue"] {{
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stDialog"] [class*="st-key-bot_msg_"] .audit-card {{
        box-shadow: none;
        margin-bottom: 6px;
    }}

    /* Slim scrollbar */
    div[data-testid="stDialog"] .st-key-copilot_body::-webkit-scrollbar {{
        width: 6px;
    }}
    div[data-testid="stDialog"] .st-key-copilot_body::-webkit-scrollbar-thumb {{
        background: {t_border};
        border-radius: 9999px;
    }}

    /* Body children must not shrink/squash while the container scrolls */
    div[data-testid="stDialog"] .st-key-copilot_body > * {{
        flex-shrink: 0 !important;
    }}
    div[data-testid="stDialog"] .st-key-copilot_body .copilot-empty-state {{
        flex: 1 1 auto !important;
    }}

    /* The zero-height iframe that runs the auto-scroll script must take no space */
    div[data-testid="stDialog"] .st-key-copilot_body [data-testid="stElementContainer"]:has(iframe) {{
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        line-height: 0 !important;
    }}

    /* BOTTOM: form pinned to the bottom edge */
    div[data-testid="stDialog"] .st-key-copilot_bottom {{
        padding-top: 4px !important;
    }}

    div[data-testid="stDialog"] div[data-testid="stForm"] {{
        border: 1px solid {t_border} !important;
        border-radius: 12px !important;
        padding: 8px 10px !important;
        background: {t_chat_form_bg} !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }}

    /* Empty state inside Copilot drawer: borderless, adapts height, centered */
    .copilot-empty-state {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
        height: 100% !important;
        min-height: 0 !important;
        flex: 1 1 auto !important;
        border: none !important;
        border-width: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 16px !important;
        margin-top:48px;
        box-sizing: border-box !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sub-module imports
from ui.pages.dashboard import render_dashboard
from ui.pages.job_detail import render_job_detail
from ui.pages.rag_assistant import render_rag_drawer
from ui.services.jobs_client import JobsClient
from ui.services.rag_client import RAGClient

# Cache clients in Session State to prevent redundant instantiations
if "jobs_client" not in st.session_state:
    st.session_state.jobs_client = JobsClient()

if "rag_client" not in st.session_state:
    st.session_state.rag_client = RAGClient()

if "selected_invoice_id" not in st.session_state:
    st.session_state.selected_invoice_id = "INV-1042"

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False


# Multipage Page Functions
def page_dashboard_view():
    render_dashboard(
        jobs_client=st.session_state.jobs_client,
        on_select_invoice=lambda inv_id: st.switch_page(invoice_page),
    )


def page_invoice_view():
    inv_id = st.query_params.get("id") or st.session_state.get("selected_invoice_id", "INV-1042")
    render_job_detail(
        invoice_id=inv_id,
        jobs_client=st.session_state.jobs_client,
        on_back=lambda: st.switch_page(dashboard_page),
    )


dashboard_page = st.Page(
    page_dashboard_view,
    title="Dashboard",
    icon=":material/dashboard:",
    url_path="dashboard",
    default=True,
)

invoice_page = st.Page(
    page_invoice_view,
    title="Invoice Pipeline",
    icon=":material/account_tree:",
    url_path="invoice",
)

# Multipage Navigation Setup with HIDDEN position (no box or tabs shown at top)
pg = st.navigation(
    [dashboard_page, invoice_page],
    position="hidden",
)

# Execute active page
pg.run()

# Floating Action Button Marker & Button
st.markdown('<div id="fab-marker"></div>', unsafe_allow_html=True)

if st.button("", icon=":material/chat:", key="fab_bot_trigger", help="Open AI Audit Copilot"):
    st.session_state.show_chat = not st.session_state.show_chat
    st.rerun()

# Render Floating Chatbot Drawer when toggled
if st.session_state.show_chat:
    render_rag_drawer(
        rag_client=st.session_state.rag_client,
        jobs_client=st.session_state.jobs_client,
    )