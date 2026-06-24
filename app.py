import os
import sys
import base64
import streamlit as st

# Страховка путей для импорта страниц из папки pages
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(
    page_title="ShelfControl",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Функция динамической конвертации изображений в Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

sidebar_bg = get_base64_image("Black Fignya.jpg")
main_bg = get_base64_image("epic bakground.jpg")

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

/* Полностью скрываем кнопку управления боковой панелью */
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

/* Принудительно делаем все внутренние контейнеры 
   сайдбара прозрачными, чтобы картинка фона пробилась наружу */
[data-testid="stSidebar"] > div, 
[data-testid="stSidebarContent"], 
[data-testid="stSidebarUserContent"] {
    background-color: transparent !important;
    background: transparent !important;
    padding: 0 !important;
}

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

/* ─── КНОПКИ (СКРУГЛЕНИЕ И ФИКС НАВЕДЕНИЯ) ─── */
/* ─── ВСЕ КНОПКИ ─── */
.stButton > button,
.stDownloadButton > button,
div[data-testid="stNumberInput"] button,
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-primary"] {
    background: #1C1C1A !important;
    background-color: #1C1C1A !important;
    color: #F5F0E8 !important;
    border: none !important;
    border-radius: 30px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: background-color 0.15s !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Hover — тёмно-красный */
.stButton > button:hover,
.stButton > button:active,
.stButton > button:focus,
.stButton > button:focus-visible,
.stDownloadButton > button:hover,
.stDownloadButton > button:active,
div[data-testid="stNumberInput"] button:hover,
div[data-testid="stNumberInput"] button:active,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-secondary"]:active,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primary"]:active {
    background: #D4401A !important;
    background-color: #D4401A !important;
    color: #F5F0E8 !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    opacity: 1 !important;
}


/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] {
    border: 1px dashed #8C8C7A !important;
    border-radius: 0 !important;
    background: #EDEAE0 !important;
    padding: 12px !important;
}

/* ─── НАВИГАЦИЯ В САЙДБАРЕ (БЕЗ ФОНОВОЙ ПОДСВЕТКИ) ─── */
[data-testid="stRadio"] {
    position: relative;
    z-index: 2;
}
[data-testid="stRadio"] > div { gap: 0 !important; }

/* Уничтожаем подложки у внутренних элементов BaseWeb */
[data-testid="stRadio"] [data-baseweb="radio"],
[data-testid="stRadio"] [data-baseweb="radio"]:hover,
[data-testid="stRadio"] div[role="radiogroup"] div {
    background-color: transparent !important;
    background: transparent !important;
}

/* Стили кнопок-лейблов */
[data-testid="stRadio"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    color: #8C8C7A !important;
    padding: 10px 24px !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    border-left: 2px solid transparent !important;
    transition: color .15s, border-color .15s !important;
    display: block !important;
    background: transparent !important;
    background-color: transparent !important;
}

/* Эффект наведения — только изменение цвета текста, без белых плашек */
[data-testid="stRadio"] label:hover { 
    color: #F5F0E8 !important; 
    background: transparent !important;
    background-color: transparent !important;
}

/* Активное состояние */
[data-baseweb="radio"][aria-checked="true"] + div label,
[data-testid="stRadio"] [aria-checked="true"] ~ label {
    color: #F5F0E8 !important;
    border-left-color: #D4401A !important;
    background: transparent !important;
    background-color: transparent !important;
}

.stAlert { border-radius: 0 !important; }

/* ─── EXPANDER (полки) ─── */
div[data-testid="stExpander"] {
    border: 1px solid #DDD9CF !important;
    border-radius: 12px !important;
    background: rgba(237, 234, 224, 0.85) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    font-family: "Space Grotesk", sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #1C1C1A !important;
    background: transparent !important;
    background-color: transparent !important;
    border-radius: 0 !important;
    padding: 12px 16px !important;
}
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] summary:focus,
div[data-testid="stExpander"] summary:active {
    background: transparent !important;
    background-color: transparent !important;
    color: #1C1C1A !important;
    outline: none !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] summary svg {
    fill: #1C1C1A !important;
    color: #1C1C1A !important;
}
.stSpinner { color: #D4401A !important; }

/* metric */
[data-testid="stMetric"] { background: #EDEAE0 !important; padding: 16px 20px !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #8C8C7A !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 28px !important; color: #1C1C1A !important; }
</style>
""", unsafe_allow_html=True)

# Динамическое применение основного фонда
if main_bg:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{main_bg}") !important;
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

# Динамическое применение изображения на фон левого сайдбара
if sidebar_bg:
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/jpeg;base64,{sidebar_bg}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown('<style>[data-testid="stSidebar"] { background: #1C1C1A !important; }</style>', unsafe_allow_html=True)


# Контент Сайдбара
st.sidebar.markdown('<div class="sc-brand">Shelf<span class="sc-brand-accent">Control</span></div>', unsafe_allow_html=True)


page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")



# Маршрутизация страниц с защитой от сбоев путей окружения
if page == "Планограмма":
    try:
        from pages import planogram
    except ModuleNotFoundError:
        import planogram
    planogram.show()
elif page == "Анализ":
    try:
        from pages import analyze
    except ModuleNotFoundError:
        import analyze
    analyze.show()
elif page == "История":
    try:
        from pages import history
    except ModuleNotFoundError:
        import history
    history.show()