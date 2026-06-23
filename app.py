import streamlit as st
import base64
import os

st.set_page_config(
    page_title="ShelfControl",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Функция динамической конвертации изображений в Base64
def get_base64_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

main_bg_base64 = get_base64_background("epic bakground.jpg")
sidebar_bg_base64 = get_base64_background("Black Fignya.jpg")

# Инжектим базовые стили приложения
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* Дефолтный шрифт и сброс базовых слоев */
[data-testid="stMainBlockContainer"], .main, body {
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }

/* Полностью скрываем кнопку управления боковой панелью (фиксируем её) */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* ─── SIDEBAR BASE ─── */
[data-testid="stSidebar"] {
    border-right: none !important;
    min-width: 200px !important;
    max-width: 200px !important;
    transform: none !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #F5F0E8 !important; }

.sc-brand {
    padding: 32px 24px 4px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #F5F0E8;
    position: relative;
    z-index: 2;
}
.sc-brand-accent { color: #D4401A !important; }
.sc-divline {
    margin: 16px 24px;
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 2;
}
.sc-nav-section {
    padding: 0 24px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8C8C7A !important;
    position: relative;
    z-index: 2;
}

/* ─── MAIN ─── */
.main .block-container {
    padding: 3rem 3rem 2rem;
    max-width: 1080px;
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

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] {
    border: 1px dashed #8C8C7A !important;
    border-radius: 0 !important;
    background: #EDEAE0 !important;
    padding: 12px !important;
}

/* ─── RADIO (навигация в сайдбаре) ─── */
[data-testid="stRadio"] {
    position: relative;
    z-index: 2;
}
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
[data-testid="stRadio"] label:hover { color: #F5F0E8 !important; background: rgba(255, 255, 255, 0.05) !important; }
[data-baseweb="radio"][aria-checked="true"] + div label,
[data-testid="stRadio"] [aria-checked="true"] ~ label {
    color: #F5F0E8 !important;
    border-left-color: #D4401A !important;
    background: rgba(255, 255, 255, 0.08) !important;
}

.stAlert { border-radius: 0 !important; }
.stSpinner { color: #D4401A !important; }

/* metric */
[data-testid="stMetric"] { background: #EDEAE0 !important; padding: 16px 20px !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #8C8C7A !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 28px !important; color: #1C1C1A !important; }
</style>
""", unsafe_allow_html=True)

# Динамическое применение картинок, если файлы на месте
if main_bg_base64:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{main_bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stMainBlockContainer"], .main, body {{
        background-color: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown('<style>[data-testid="stAppViewContainer"] { background-color: #F5F0E8 !important; }</style>', unsafe_allow_html=True)

if sidebar_bg_base64:
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/jpeg;base64,{sidebar_bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown('<style>[data-testid="stSidebar"] { background: #1C1C1A !important; }</style>', unsafe_allow_html=True)


# Sidebar Content
st.sidebar.markdown('<div class="sc-brand">Shelf<span class="sc-brand-accent">Control</span></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sc-nav-section">Разделы</div>', unsafe_allow_html=True)

page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")



if page == "Планограмма":
    from pages import planogram
    planogram.show()
elif page == "Анализ":
    from pages import analyze
    analyze.show()
elif page == "История":