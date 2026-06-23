import streamlit as st

st.set_page_config(
    page_title="ShelfControl",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background: #0E0E10 !important;
    color: #E4E4E7 !important;
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none; }

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="collapsedControl"] {
    color: #FFFFFF !important;
    background: #16161A !important;
    border-radius: 4px;
    padding: 4px;
    margin-left: 10px;
}

[data-testid="stSidebar"] {
    background: #111113 !important;
    border-right: 1px solid #1F1F23 !important;
    min-width: 200px !important;
    max-width: 200px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #E4E4E7 !important; }

.sc-brand {
    padding: 32px 24px 4px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #FFFFFF;
}
.sc-brand-accent { color: #E24A24 !important; }

.sc-divline {
    margin: 16px 24px;
    border: none;
    border-top: 1px solid #1F1F23;
}
.sc-nav-section {
    padding: 0 24px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #52525B !important;
}

.main { background: #0E0E10 !important; }
.main .block-container {
    padding: 3rem 3rem 2rem;
    max-width: 1080px;
    background: #0E0E10;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 28px !important; font-weight: 700 !important; }
h2 { font-size: 18px !important; font-weight: 600 !important; }

.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #71717A;
    margin-bottom: 8px;
}
.page-desc {
    font-size: 14px;
    color: #A1A1AA;
    margin-top: -8px;
    margin-bottom: 32px;
    line-height: 1.6;
}
.rule { border: none; border-top: 1px solid #1F1F23; margin: 28px 0; }

.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; margin-bottom: 2px; }
.kpi-card {
    background: #16161A;
    padding: 22px 26px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #27272A;
}
.kpi-card.accent::before { background: #E24A24; }
.kpi-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #71717A;
    margin-bottom: 10px;
}
.kpi-num {
    font-family: 'DM Mono', monospace;
    font-size: 32px;
    font-weight: 500;
    color: #FFFFFF;
    line-height: 1;
}
.kpi-num.red { color: #FF453A; }
.kpi-num.ok  { color: #32D74B; }
.kpi-num.mid { color: #FF9F0A; }

...comp-wrap {
    background: #16161A;
    height: 4px;
    margin: 20px 0 6px;
    position: relative;
}
.comp-fill {
    position: absolute;
    top: 0; left: 0;
    height: 100%;
    transition: width .8s cubic-bezier(.4,0,.2,1);
}
.comp-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #71717A;
    text-align: right;
    margin-bottom: 24px;
}

.sum-box {
    padding: 18px 22px;
    margin-bottom: 24px;
    border-left: 3px solid #27272A;
    font-size: 13.5px;
    line-height: 1.7;
    color: #E4E4E7;
    background: #16161A;
}
.sum-box.ok  { border-left-color: #32D74B; }
.sum-box.mid { border-left-color: #FF9F0A; }
.sum-box.bad { border-left-color: #FF453A; }

.viol-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #FF453A;
    margin-bottom: 10px;
}
.viol-row {
    font-size: 13px;
    color: #E4E4E7;
    padding: 11px 16px;
    margin-bottom: 4px;
    background: #16161A;
    border-left: 2px solid #FF453A;
    line-height: 1.5;
}

.shelf-wrap {
    background: #16161A;
    margin-bottom: 4px;
    border: 1px solid #1F1F23;
}
.shelf-head {
    padding: 13px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1F1F23;
    background: #1A1A1E;
}
.shelf-title {
    font-size: 13px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.01em;
}
.shelf-body { padding: 16px 20px; }
.col-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #71717A;
    margin-bottom: 10px;
}
.prod-item {
    font-size: 13px;
    color: #E4E4E7;
    padding: 6px 0;
    border-bottom: 1px solid #1F1F23;
    display: flex;
    align-items: center;
    gap: 10px;
}
.prod-item:last-child { border-bottom: none; }
.prod-idx {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #71717A;
    min-width: 18px;
}

.chip {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 8px;
    border: 1px solid currentColor;
}
.chip-ok  { color: #32D74B; }
.chip-bad { color: #FF453A; }
.chip-mid { color: #FF9F0A; }

.tag-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    letter-spacing: 0.06em;
}
.tag-miss  { background: transparent; border: 1px solid #FF453A; color: #FF453A; }
.tag-extra { background: transparent; border: 1px solid #FF9F0A; color: #FF9F0A; }
.tag-ok    { background: transparent; border: 1px solid #32D74B; color: #32D74B; }
.tag-note  { background: transparent; border: 1px solid #71717A; color: #71717A; }

.wrong-note {
    font-size: 12px;
    color: #71717A;
    margin-top: 10px;
    line-height: 1.6;
    font-style: italic;
}

.stTextInput input, .stNumberInput input {
    background: #16161A !important;
    border: 1px solid #1F1F23 !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13.5px !important;
    color: #FFFFFF !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #E24A24 !important;
    box-shadow: none !important;
    outline: none !important;
}
label { font-size: 11px !important; color: #71717A !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }

.stButton > button {
    background: #E24A24 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    padding: 11px 24px !important;
    text-transform: uppercase !important;
    transition: background .15s !important;
}
.stButton > button:hover { background: #FF5733 !important; }
.stButton > button:disabled { background: #1F1F23 !important; color: #71717A !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: #FFFFFF !important;
    border: 1px solid #1F1F23 !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 9px 18px !important;
}
.stDownloadButton > button:hover { background: #FFFFFF !important; color: #0E0E10 !important; }

[data-testid="stFileUploader"] {
    border: 1px dashed #71717A !important;
    border-radius: 0 !important;
    background: #16161A !important;
    padding: 12px !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #1F1F23 !important;
    border-radius: 0 !important;
    background: #16161A !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #FFFFFF !important;
}

[data-testid="stRadio"] > div { gap: 0 !important; }
[data-testid="stRadio"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    color: #A1A1AA !important;
    padding: 10px 24px !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    border-left: 2px solid transparent !important;
    transition: all .15s !important;
    display: block !important;
}
[data-testid="stRadio"] label:hover { color: #FFFFFF !important; background: #1C1C21 !important; }
[data-baseweb="radio"][aria-checked="true"] + div label,
[data-testid="stRadio"] [aria-checked="true"] ~ label {
    color: #FFFFFF !important;
    border-left-color: #E24A24 !important;
    background: #16161A !important;
}

.stAlert { border-radius: 0 !important; background-color: #16161A !important; border: 1px solid #1F1F23 !important; }

.stSpinner { color: #E24A24 !important; }

[data-testid="stMetric"] { background: #16161A !important; padding: 16px 20px !important; border: 1px solid #1F1F23 !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #71717A !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 28px !important; color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sc-brand">Shelf<span class="sc-brand-accent">Control</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<hr class="sc-divline">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sc-nav-section">Разделы</div>', unsafe_allow_html=True)

page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")

st.sidebar.markdown('<hr class="sc-divline" style="margin-top:auto">', unsafe_allow_html=True)
st.sidebar.markdown('<div style="padding:16px 24px;font-family:\'DM Mono\',monospace;font-size:10px;color:#52525B;letter-spacing:0.1em">v1.0 / 2026</div>', unsafe_allow_html=True)

if page == "Планограмма":
    from pages import planogram
    planogram.show()
elif page == "Анализ":
    from pages import analyze
    analyze.show()
elif page == "История":
    from pages import history
    history.show()