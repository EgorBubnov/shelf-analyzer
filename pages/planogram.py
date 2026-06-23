import streamlit as st
import json


def show():
    st.title("Планограмма")
    st.markdown('<p class="page-meta">Задайте эталонный порядок товаров — он будет использоваться при проверке фото</p>', unsafe_allow_html=True)

    if "planogram" not in st.session_state:
        st.session_state.planogram = {
            "name": "Моя планограмма",
            "shelves": [
                {"id": 0, "name": "Верхняя полка", "products": ["Товар A", "Товар B", "Товар C"]},
                {"id": 1, "name": "Средняя полка", "products": ["Товар D", "Товар E", "Товар F"]},
                {"id": 2, "name": "Нижняя полка",  "products": ["Товар G", "Товар H", "Товар I"]}
            ]
        }

    planogram = st.session_state.planogram

    col1, col2 = st.columns([3, 1])
    with col1:
        planogram["name"] = st.text_input("Название", value=planogram["name"])
    with col2:
        num_shelves = st.number_input("Полок", min_value=1, max_value=8, value=len(planogram["shelves"]))

    while len(planogram["shelves"]) < num_shelves:
        i = len(planogram["shelves"])
        planogram["shelves"].append({"id": i, "name": f"Полка {i+1}", "products": []})
    while len(planogram["shelves"]) > num_shelves:
        planogram["shelves"].pop()

    st.markdown("<hr>", unsafe_allow_html=True)

    for i, shelf in enumerate(planogram["shelves"]):
        with st.expander(shelf["name"], expanded=True):
            c1, c2 = st.columns([2, 5])
            with c1:
                shelf["name"] = st.text_input("Название полки", value=shelf["name"], key=f"sn_{i}")
            with c2:
                raw = st.text_input(
                    "Товары через запятую (слева → направо)",
                    value=", ".join(shelf["products"]),
                    key=f"sp_{i}",
                    placeholder="Кола 0.5л, Спрайт 0.5л, Фанта 0.5л"
                )
                shelf["products"] = [p.strip() for p in raw.split(",") if p.strip()]
            if shelf["products"]:
                chips = " ".join([f'<span class="tag tag-note">{j+1}. {p}</span>' for j, p in enumerate(shelf["products"])])
                st.markdown(chips, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("Сохранить", use_container_width=True, type="primary"):
            st.session_state.planogram = planogram
            st.success("Сохранено")
    with c2:
        st.download_button(
            "Экспорт JSON",
            data=json.dumps(planogram, ensure_ascii=False, indent=2),
            file_name="planogram.json",
            mime="application/json",
            use_container_width=True
        )
    with c3:
        f = st.file_uploader("Импорт JSON", type="json", label_visibility="collapsed")
        if f:
            try:
                st.session_state.planogram = json.loads(f.read())
                st.success("Загружено")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка: {e}")