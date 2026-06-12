import streamlit as st

st.set_page_config(
    page_title="Анализатор прилавков",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Навигация через sidebar
st.sidebar.title("🛒 Анализатор прилавков")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Раздел",
    ["📋 Планограмма", "📸 Анализ фото", "📊 История"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small>Система проверки правильности выкладки товаров на основе компьютерного зрения</small>",
    unsafe_allow_html=True
)

if page == "📋 Планограмма":
    from pages import planogram
    planogram.show()
elif page == "📸 Анализ фото":
    from pages import analyze
    analyze.show()
elif page == "📊 История":
    from pages import history
    history.show()
