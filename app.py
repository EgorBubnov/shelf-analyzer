import streamlit st

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
    background: #F5F0E8 !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: #1C1C1A !important;
    border-right: none !important;
    min-width: 200px !important;
    max-width: 200px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #F5F0E8 !important; }

.sc-brand {
    padding: 32px 24px 4px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px; /* Немного уменьшили для идеального выравнивания */
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #F5F0E8;
    white-space: nowrap; /* Запрещаем перенос букв на новую строку */
}
.sc-brand-accent { color: #D4401A !important; }
.sc-divline {
    margin: 16px 24px;
    border: none;
    border-top: 1px solid #2E2E2C;
}
.sc-nav-section {
    padding: 0 24px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5A5A52 !important;
}

/* ─── MAIN ─── */
.main { background: #F5F0E8 !important; }
.main .block-container {
    padding: 3rem 3rem 2rem;
    max-width: 1080px;
    background: #F5F0E8;
}

/* ─── TYPOGRAPHY ─── */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #1C1C1A !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 28px !important; font-weight: 700 !important; }
h2 { font-size: 18px !important; font-weight: 600 !important; }

.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8C8C7A;
    margin-bottom: 8px;
}
.page-desc {
    font-size: 14px;
    color: #8C8C7A;
    margin-top: -8px;
    margin-bottom: 32px;
    line-height: 1.6;
}
.rule { border: none; border-top: 1px solid #DDD9CF; margin: 28px 0; }

/* ─── KPI CARDS ─── */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; margin-bottom: 2px; }
.kpi-card {
    background: #EDEAE0;
    padding: 22px 26px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #DDD9CF;
}
.kpi-card.accent::before { background: #D4401A; }
.kpi-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8C8C7A;
    margin-bottom: 10px;
}
.kpi-num {
    font-family: 'DM Mono', monospace;
    font-size: 32px;
    font-weight: 500;
    color: #1C1C1A;
    line-height: 1;
}
.kpi-num.red { color: #D4401A; }
.kpi-num.ok  { color: #2D6A4F; }
.kpi-num.mid { color: #B45309; }

/* ─── COMPLIANCE BAR ─── */
.comp-wrap {
    background: #EDEAE0;
    height: 3px;
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
    color: #8C8C7A;
    text-align: right;
    margin-bottom: 24px;
}

/* ─── SUMMARY BOX ─── */
.sum-box {
    padding: 18px 22px;
    margin-bottom: 24px;
    border-left: 3px solid #DDD9CF;
    font-size: 13.5px;
    line-height: 1.7;
    color: #3A3A36;
    background: #EDEAE0;
}
.sum-box.ok  { border-left-color: #2D6A4F; }
.sum-box.mid { border-left-color: #B45309; }
.sum-box.bad { border-left-color: #D4401A; }

/* ─── VIOLATIONS ─── */
.viol-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #D4401A;
    margin-bottom: 10px;
}
.viol-row {
    font-size: 13px;
    color: #1C1C1A;
    padding: 11px 16px;
    margin-bottom: 4px;
    background: #EDEAE0;
    border-left: 2px solid #D4401A;
    line-height: 1.5;
}

/* ─── SHELF CARDS ─── */
.shelf-wrap {
    background: #EDEAE0;
    margin-bottom: 4px;
}
.shelf-head {
    padding: 13px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #DDD9CF;
}
.shelf-title {
    font-size: 13px;
    font-weight: 600;
    color: #1C1C1A;
    letter-spacing: 0.01em;
}
.shelf-body { padding: 16px 20px; }
.col-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8C8C7A;
    margin-bottom: 10px;
}
.prod-item {
    font-size: 13px;
    color: #3A3A36;
    padding: 4px 0;
    border-bottom: 1px solid #DDD9CF;
    display: flex;
    align-items: center;
    gap: 10px;
}
.prod-item:last-child { border-bottom: none; }
.prod-idx {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #8C8C7A;
    min-width: 18px;
}

/* status chips */
.chip {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 8px;
    border: 1px solid currentColor;
}
.chip-ok  { color: #2D6A4F; }
.chip-bad { color: #D4401A; }
.chip-mid { color: #B45309; }

.tag-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    letter-spacing: 0.06em;
}
.tag-miss  { background: transparent; border: 1px solid #D4401A; color: #D4401A; }
.tag-extra { background: transparent; border: 1px solid #B45309; color: #B45309; }
.tag-ok    { background: transparent; border: 1px solid #2D6A4F; color: #2D6A4F; }
.tag-note  { background: transparent; border: 1px solid #8C8C7A; color: #8C8C7A; }

.wrong-note {
    font-size: 12px;
    color: #8C8C7A;
    margin-top: 10px;
    line-height: 1.6;
    font-style: italic;
}

/* ─── INPUTS ─── */
.stTextInput input, .stNumberInput input {
    background: #EDEAE0 !important;
    border: 1px solid #DDD9CF !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13.5px !important;
    color: #1C1C1A !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #1C1C1A !important;
    box-shadow: none !important;
    outline: none !important;
}
label { font-size: 11px !important; color: #8C8C7A !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }

/* ─── BUTTON ─── */
.stButton > button {
    background: #1C1C1A !important;
    color: #F5F0E8 !important;
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
.stButton > button:hover { background: #D4401A !important; }
.stButton > button:disabled { background: #DDD9CF !important; color: #8C8C7A !important; }

/* download button */
.stDownloadButton > button {
    background: transparent !important;
    color: #1C1C1A !important;
    border: 1px solid #1C1C1A !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
.stDownloadButton > button:hover { background: #1C1C1A !important; color: #F5F0E8 !important; }

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] {
    border: 1px dashed #8C8C7A !important;
    border-radius: 0 !important;
    background: #EDEAE0 !important;
    padding: 12px !important;
}

/* ─── EXPANDER ─── */
div[data-testid="stExpander"] {
    border: 1px solid #DDD9CF !important;
    border-radius: 0 !important;
    background: #EDEAE0 !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #1C1C1A !important;
}

/* ─── RADIO (nav) ─── */
[data-testid="stRadio"] > div { gap: 0 !important; }
[data-testid="stRadio"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    color: #8C8C7A !important;
    padding: 10px 24px !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    border-left: 2px solid transparent !important;
    transition: all .15s !important;
    display: block !important;
}
[data-testid="stRadio"] label:hover { color: #F5F0E8 !important; background: #2E2E2C !important; }
[data-baseweb="radio"][aria-checked="true"] + div label,
[data-testid="stRadio"] [aria-checked="true"] ~ label {
    color: #F5F0E8 !important;
    border-left-color: #D4401A !important;
}

/* alerts */
.stAlert { border-radius: 0 !important; }

/* spinner */
.stSpinner { color: #D4401A !important; }

/* metric */
[data-testid="stMetric"] { background: #EDEAE0 !important; padding: 16px 20px !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #8C8C7A !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 28px !important; color: #1C1C1A !important; }
</style>
""", unsafe_allow_html=True)

# Логотип приложения (теперь с nowrap и адаптированным размером)
st.sidebar.markdown('<div class="sc-brand">Shelf<span class="sc-brand-accent">Control</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<hr class="sc-divline">', unsafe_allow_html=True)

# Переключатель разделов меню (строка "Разделы" успешно удалена)
page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")

# Нижний футер с версией полностью очищен

if page == "Планограмма":
    from pages import planogram
    planogram.show()
elif page == "Анализ":
    from pages import analyze
    analyze.show()
elif page == "История":
    from pages import history
    history.show()