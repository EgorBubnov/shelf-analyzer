import streamlit as st

st.set_page_config(
    page_title="ShelfControl",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght=400;500;600;700&family=DM+Mono:wght=400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ─── ГЛОБАЛЬНЫЙ ТЁМНЫЙ ИНТЕРФЕЙС ─── */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background: #0E0E0C !important;
    color: #F5F0E8 !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }

/* ─── БОКОВОЕ МЕНЮ ─── */
[data-testid="stSidebar"] {
    background: #161614 !important;
    border-right: none !important;
    min-width: 200px !important;
    max-width: 200px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #F5F0E8 !important; }

.sc-brand {
    padding: 32px 24px 4px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #F5F0E8;
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

/* ─── ГЛАВНЫЙ КОНТЕЙНЕР ─── */
.main { background: #0E0E0C !important; }
.main .block-container {
    padding: 3rem 3rem 2rem;
    max-width: 1080px;
    background: #0E0E0C;
}

/* ─── ТИПОГРАФИКА ─── */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #F5F0E8 !important;
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
.rule { border: none; border-top: 1px solid #2E2E2C; margin: 28px 0; }

/* ─── KPI КАРТОЧКИ ─── */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; margin-bottom: 2px; }
.kpi-card {
    background: #1C1C1A;
    padding: 22px 26px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #2E2E2C;
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
    color: #F5F0E8;
    line-height: 1;
}
.kpi-num.red { color: #D4401A; }
.kpi-num.ok  { color: #A3E635; }
.kpi-num.mid { color: #F59E0B; }

/* ─── ИНДИКАТОР ВЫПОЛНЕНИЯ ─── */
.comp-wrap {
    background: #1C1C1A;
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

/* ─── СВОДНЫЙ БОКС ─── */
.sum-box {
    padding: 18px 22px;
    margin-bottom: 24px;
    border-left: 3px solid #2E2E2C;
    font-size: 13.5px;
    line-height: 1.7;
    color: #E5E5E0;
    background: #1C1C1A;
}
.sum-box.ok  { border-left-color: #A3E635; }
.sum-box.mid { border-left-color: #F59E0B; }
.sum-box.bad { border-left-color: #D4401A; }

/* ─── НАРУШЕНИЯ ─── */
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
    color: #F5F0E8;
    padding: 11px 16px;
    margin-bottom: 4px;
    background: #1C1C1A;
    border-left: 2px solid #D4401A;
    line-height: 1.5;
}

/* ─── КАРТОЧКИ ПОЛОК ─── */
.shelf-wrap {
    background: #1C1C1A;
    margin-bottom: 4px;
}
.shelf-head {
    padding: 13px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2E2E2C;
}
.shelf-title {
    font-size: 13px;
    font-weight: 600;
    color: #F5F0E8;
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
    color: #E5E5E0;
    padding: 4px 0;
    border-bottom: 1px solid #2E2E2C;
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

/* Статусы и теги */
.chip {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 8px;
    border: 1px solid currentColor;
}
.chip-ok  { color: #A3E635; }
.chip-bad { color: #D4401A; }
.chip-mid { color: #F59E0B; }

.tag-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    letter-spacing: 0.06em;
}
.tag-miss  { background: transparent; border: 1px solid #D4401A; color: #D4401A; }
.tag-extra { background: transparent; border: 1px solid #F59E0B; color: #F59E0B; }
.tag-ok    { background: transparent; border: 1px solid #A3E635; color: #A3E635; }
.tag-note  { background: transparent; border: 1px solid #8C8C7A; color: #8C8C7A; }

.wrong-note {
    font-size: 12px;
    color: #8C8C7A;
    margin-top: 10px;
    line-height: 1.6;
    font-style: italic;
}

/* ─── ИНПУТЫ И КВАДРАТИКИ (ИСПРАВЛЕНО НА ТЕМНЫЕ) ─── */
.stTextInput input, .stNumberInput input {
    background: #1C1C1A !important;
    border: 1px solid #2E2E2C !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13.5px !important;
    color: #F5F0E8 !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #D4401A !important;
    box-shadow: none !important;
    outline: none !important;
}
label { font-size: 11px !important; color: #8C8C7A !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }

/* ─── КНОПКИ ─── */
.stButton > button {
    background: #1C1C1A !important;
    color: #F5F0E8 !important;
    border: 1px solid #2E2E2C !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    padding: 11px 24px !important;
    text-transform: uppercase !important;
    transition: background .15s !important;
}
.stButton > button:hover { background: #D4401A !important; border-color: #D4401A !important; }
.stButton > button:disabled { background: #161614 !important; color: #5A5A52 !important; border-color: #2E2E2C !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: #F5F0E8 !important;
    border: 1px solid #2E2E2C !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 9px 18px !important;
}
.stDownloadButton > button:hover { background: #F5F0E8 !important; color: #0E0E0C !important; }

/* ─── ЗАГРУЗЧИК ФАЙЛОВ ─── */
[data-testid="stFileUploader"] {
    border: 1px dashed #8C8C7A !important;
    border-radius: 0 !important;
    background: #1C1C1A !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] * { color: #F5F0E8 !important; }

/* ─── КОНТЕЙНЕРЫ / ЭКСПАНДЕРЫ (ИСПРАВЛЕНО НА ТЕМНЫЕ) ─── */
div[data-testid="stExpander"] {
    border: 1px solid #2E2E2C !important;
    border-radius: 0 !important;
    background: #1C1C1A !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #F5F0E8 !important;
}

/* ─── РАДИОКНОПКИ НАВИГАЦИИ ─── */
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

/* Перехват инлайн-стилей темного текста из других файлов */
div[style*="color: #3A3A36"], div[style*="color:#3A3A36"] { color: #E5E5E0 !important; }
div[style*="color: #1C1C1A"], div[style*="color:#1C1C1A"] { color: #F5F0E8 !important; }
div[style*="border-bottom: 1px solid #DDD9CF"], div[style*="border-bottom:1px solid #DDD9CF"] { border-bottom-color: #2E2E2C !important; }
div[style*="border-top: 1px solid #DDD9CF"] { border-top-color: #2E2E2C !important; }
div[style*="border-left: 2px solid #DDD9CF"] { border-left-color: #2E2E2C !important; }

/* Уведомления */
.stAlert { border-radius: 0 !important; background-color: #1C1C1A !important; color: #F5F0E8 !important; border: 1px solid #2E2E2C !important; }

/* Спиннер */
.stSpinner { color: #D4401A !important; }

/* Метрики */
[data-testid="stMetric"] { background: #1C1C1A !important; padding: 16px 20px !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #8C8C7A !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 28px !important; color: #F5F0E8 !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="sc-brand">Shelf<span class="sc-brand-accent">Control</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<hr class="sc-divline">', unsafe_allow_html=True)


page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")

st.sidebar.markdown('<hr class="sc-divline" style="margin-top:auto">', unsafe_allow_html=True)


if page == "Планограмма":
    from pages import planogram
    planogram.show()
elif page == "Анализ":
    from pages import analyze
    analyze.show()
elif page == "История":
    from pages import history
    history.show()