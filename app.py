import streamlit as st

st.set_page_config(
    page_title="ShelfControl",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }

[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: none !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

.sc-logo {
    padding: 28px 24px 6px;
    font-size: 17px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.5px;
}
.sc-logo b { color: #3b82f6; font-weight: 700; }
.sc-tagline {
    padding: 0 24px 28px;
    font-size: 10.5px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.sc-nav-label {
    padding: 0 24px 8px;
    font-size: 10px;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
}
.sc-version {
    padding: 24px;
    font-size: 11px;
    color: #334155;
    position: absolute;
    bottom: 0;
}

.main .block-container {
    padding: 2.5rem 2.5rem 2rem;
    max-width: 1100px;
}

h1 { font-size: 22px !important; font-weight: 700 !important; color: #0f172a !important; letter-spacing: -0.3px !important; }
h2 { font-size: 16px !important; font-weight: 600 !important; color: #0f172a !important; }
h3 { font-size: 14px !important; font-weight: 600 !important; color: #374151 !important; }

.page-meta { font-size: 13.5px; color: #64748b; margin-top: -12px; margin-bottom: 28px; }
hr { border: none !important; border-top: 1px solid #f1f5f9 !important; margin: 24px 0 !important; }

.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 24px; }
.kpi { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px 22px; }
.kpi-label { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.kpi-val { font-size: 26px; font-weight: 700; color: #0f172a; line-height: 1; }
.kpi-val.green { color: #16a34a; }
.kpi-val.amber { color: #d97706; }
.kpi-val.red { color: #dc2626; }

.bar-wrap { background: #f1f5f9; border-radius: 3px; height: 5px; margin: 16px 0 6px; overflow: hidden; }
.bar { height: 100%; border-radius: 3px; }

.summary-box { padding: 14px 18px; border-radius: 8px; font-size: 13.5px; line-height: 1.6; margin-bottom: 20px; }
.summary-ok  { background: #f0fdf4; border-left: 3px solid #16a34a; color: #15803d; }
.summary-mid { background: #fffbeb; border-left: 3px solid #d97706; color: #92400e; }
.summary-bad { background: #fef2f2; border-left: 3px solid #dc2626; color: #b91c1c; }

.violations-title { font-size: 11px; font-weight: 700; color: #dc2626; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
.violation-row { font-size: 13px; color: #7f1d1d; background: #fef2f2; border-radius: 6px; padding: 10px 14px; margin-bottom: 6px; }

.shelf-card { border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden; margin-bottom: 10px; }
.shelf-card-head { padding: 12px 18px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
.shelf-card-name { font-size: 13.5px; font-weight: 600; color: #0f172a; }
.shelf-card-body { padding: 16px 18px; }
.conf-badge { font-size: 10px; font-weight: 600; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; }
.conf-ok   { background: #dcfce7; color: #166534; }
.conf-fail { background: #fee2e2; color: #991b1b; }
.conf-mid  { background: #fef9c3; color: #854d0e; }

.col-title { font-size: 10.5px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
.prod-row { font-size: 13px; color: #374151; padding: 3px 0; }
.prod-num { color: #94a3b8; margin-right: 6px; font-size: 11px; }

.tag-row { margin-top: 10px; }
.tag { display: inline-block; font-size: 11.5px; padding: 3px 9px; border-radius: 4px; margin: 2px 3px 2px 0; }
.tag-miss  { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.tag-extra { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
.tag-note  { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

.stButton > button {
    background: #1d4ed8 !important; color: #fff !important; border: none !important;
    border-radius: 7px !important; font-weight: 600 !important; font-size: 13.5px !important;
    padding: 10px 20px !important; letter-spacing: 0.01em !important;
}
.stButton > button:hover   { background: #1e40af !important; }
.stButton > button:disabled { background: #cbd5e1 !important; color: #94a3b8 !important; }

.stTextInput input, .stNumberInput input {
    border: 1px solid #e2e8f0 !important; border-radius: 7px !important;
    font-size: 13.5px !important; color: #0f172a !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,.12) !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important; border-radius: 10px !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary { font-size: 13.5px !important; font-weight: 500 !important; }

[data-testid="stRadio"] label { color: #cbd5e1 !important; font-size: 13.5px !important; }
[data-testid="stRadio"] div[role="radio"] { accent-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sc-logo">Shelf<b>Control</b></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sc-tagline">Контроль выкладки</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sc-nav-label">Навигация</div>', unsafe_allow_html=True)

page = st.sidebar.radio("", ["Планограмма", "Анализ", "История"], label_visibility="collapsed")

if page == "Планограмма":
    from pages import planogram
    planogram.show()
elif page == "Анализ":
    from pages import analyze
    analyze.show()
elif page == "История":
    from pages import history
    history.show()