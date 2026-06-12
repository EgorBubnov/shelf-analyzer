import streamlit as st
import json


def show():
    st.title("📋 Редактор планограммы")
    st.markdown("Задайте эталонный порядок товаров на каждой полке. Это будет стандартом для проверки.")

    # Инициализация состояния
    if "planogram" not in st.session_state:
        st.session_state.planogram = {
            "name": "Моя планограмма",
            "shelves": [
                {
                    "id": 0,
                    "name": "Верхняя полка",
                    "products": ["Товар A", "Товар B", "Товар C"]
                },
                {
                    "id": 1,
                    "name": "Средняя полка",
                    "products": ["Товар D", "Товар E", "Товар F", "Товар G"]
                },
                {
                    "id": 2,
                    "name": "Нижняя полка",
                    "products": ["Товар H", "Товар I", "Товар J"]
                }
            ]
        }

    planogram = st.session_state.planogram

    # Название планограммы
    col1, col2 = st.columns([3, 1])
    with col1:
        planogram["name"] = st.text_input("Название планограммы", value=planogram["name"])
    with col2:
        num_shelves = st.number_input("Количество полок", min_value=1, max_value=6,
                                       value=len(planogram["shelves"]))

    # Синхронизируем количество полок
    while len(planogram["shelves"]) < num_shelves:
        idx = len(planogram["shelves"])
        planogram["shelves"].append({
            "id": idx,
            "name": f"Полка {idx + 1}",
            "products": []
        })
    while len(planogram["shelves"]) > num_shelves:
        planogram["shelves"].pop()

    st.markdown("---")
    st.subheader("Полки и товары")
    st.caption("Вводите товары через запятую. Порядок важен — он проверяется при анализе.")

    for i, shelf in enumerate(planogram["shelves"]):
        with st.expander(f"🗄️ {shelf['name']}", expanded=True):
            c1, c2 = st.columns([2, 5])
            with c1:
                shelf["name"] = st.text_input(
                    "Название полки", value=shelf["name"], key=f"shelf_name_{i}"
                )
            with c2:
                products_str = st.text_input(
                    "Товары (через запятую, слева направо)",
                    value=", ".join(shelf["products"]),
                    key=f"shelf_products_{i}",
                    placeholder="Кола 0.5л, Спрайт 0.5л, Фанта 0.5л"
                )
                shelf["products"] = [p.strip() for p in products_str.split(",") if p.strip()]

            # Визуальный превью полки
            if shelf["products"]:
                st.markdown("**Вид полки:**")
                cols = st.columns(len(shelf["products"]))
                for j, product in enumerate(shelf["products"]):
                    with cols[j]:
                        st.markdown(
                            f"""<div style='background:#f0f2f6;border-radius:8px;
                            padding:8px 4px;text-align:center;font-size:12px;
                            border:1px solid #ddd;min-height:60px;
                            display:flex;align-items:center;justify-content:center'>
                            {j+1}. {product}</div>""",
                            unsafe_allow_html=True
                        )

    st.markdown("---")

    col_save, col_export, col_import = st.columns([1, 1, 2])

    with col_save:
        if st.button("💾 Сохранить", use_container_width=True, type="primary"):
            st.session_state.planogram = planogram
            st.success("Планограмма сохранена!")

    with col_export:
        planogram_json = json.dumps(planogram, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ Экспорт JSON",
            data=planogram_json,
            file_name="planogram.json",
            mime="application/json",
            use_container_width=True
        )

    with col_import:
        uploaded = st.file_uploader("📂 Импорт планограммы (JSON)", type="json")
        if uploaded:
            try:
                loaded = json.loads(uploaded.read())
                st.session_state.planogram = loaded
                st.success("Планограмма загружена!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка загрузки: {e}")

    # Итоговая сводка
    st.markdown("---")
    st.subheader("📊 Сводка планограммы")
    total_products = sum(len(s["products"]) for s in planogram["shelves"])
    all_products = []
    for s in planogram["shelves"]:
        all_products.extend(s["products"])
    unique_products = list(set(all_products))

    m1, m2, m3 = st.columns(3)
    m1.metric("Полок", len(planogram["shelves"]))
    m2.metric("Позиций всего", total_products)
    m3.metric("Уникальных товаров", len(unique_products))
