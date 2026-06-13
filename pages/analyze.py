import streamlit as st
import json
import datetime
from utils.vision import analyze_shelf_image, resize_image_for_display


def show():
    st.title("📸 Анализ фотографии прилавка")

    # Проверяем наличие планограммы
    if "planogram" not in st.session_state:
        st.warning("⚠️ Сначала создайте планограмму в разделе **📋 Планограмма**")
        return

    planogram = st.session_state.planogram
    total_products = sum(len(s["products"]) for s in planogram["shelves"])

    if total_products == 0:
        st.warning("⚠️ Планограмма пустая. Добавьте товары в разделе **📋 Планограмма**")
        return

    # API ключ
    with st.expander("🔑 Настройки API", expanded=False):
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=st.session_state.get("api_key", st.secrets.get("ANTHROPIC_API_KEY", "")),
            help="Получить ключ: https://aistudio.google.com/apikey"
        )
        if api_key:
            st.session_state.api_key = api_key

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Загрузка фото")
        uploaded_file = st.file_uploader(
            "Выберите фотографию прилавка",
            type=["jpg", "jpeg", "png", "webp"],
            help="Фото должно быть сделано фронтально, все полки должны быть видны"
        )

        if uploaded_file:
            image_bytes = uploaded_file.read()
            display_bytes = resize_image_for_display(image_bytes)
            st.image(display_bytes, caption="Загруженное фото", use_container_width=True)

    with col_right:
        st.subheader("Активная планограмма")
        st.markdown(f"**{planogram['name']}**")
        for shelf in planogram["shelves"]:
            if shelf["products"]:
                products_display = " → ".join(shelf["products"])
                st.markdown(f"🗄️ **{shelf['name']}:** {products_display}")
            else:
                st.markdown(f"🗄️ **{shelf['name']}:** *(пусто)*")

    st.markdown("---")

    # Кнопка анализа
    can_analyze = uploaded_file and st.session_state.get("api_key")

    if not st.session_state.get("api_key"):
        st.info("💡 Введите Gemini API ключ в настройках выше для запуска анализа")

    if st.button(
        "🔍 Запустить анализ",
        disabled=not can_analyze,
        type="primary",
        use_container_width=True
    ):
        with st.spinner("Анализирую фотографию..."):
            try:
                result = analyze_shelf_image(
                    image_bytes,
                    planogram,
                    st.session_state.api_key
                )

                # Сохраняем в историю
                if "history" not in st.session_state:
                    st.session_state.history = []

                history_entry = {
                    "timestamp": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "filename": uploaded_file.name,
                    "planogram_name": planogram["name"],
                    "result": result,
                    "image_bytes": display_bytes
                }
                st.session_state.history.append(history_entry)
                st.session_state.last_result = result

            except json.JSONDecodeError as e:
                st.error(f"Ошибка парсинга ответа модели: {e}")
                st.stop()
            except Exception as e:
                st.error(f"Ошибка анализа: {e}")
                st.stop()

    # Отображение результатов
    if "last_result" in st.session_state and uploaded_file:
        display_results(st.session_state.last_result, planogram)


def display_results(result: dict, planogram: dict):
    st.markdown("---")
    st.subheader("📊 Результаты анализа")

    compliance = result.get("overall_compliance", 0)

    # Главный показатель
    col1, col2, col3 = st.columns(3)
    with col1:
        color = "🟢" if compliance >= 80 else ("🟡" if compliance >= 50 else "🔴")
        st.metric("Соответствие планограмме", f"{color} {compliance}%")
    with col2:
        violations = len(result.get("critical_violations", []))
        st.metric("Критических нарушений", violations)
    with col3:
        shelves = result.get("shelves_detected", 0)
        st.metric("Полок распознано", shelves)

    # Прогресс-бар соответствия
    st.progress(compliance / 100)

    # Резюме
    summary = result.get("summary", "")
    if summary:
        if compliance >= 80:
            st.success(f"✅ {summary}")
        elif compliance >= 50:
            st.warning(f"⚠️ {summary}")
        else:
            st.error(f"❌ {summary}")

    # Критические нарушения
    violations_list = result.get("critical_violations", [])
    if violations_list:
        st.markdown("### 🚨 Критические нарушения")
        for v in violations_list:
            st.error(f"• {v}")

    # Детали по полкам
    st.markdown("### 🗄️ Анализ по полкам")

    shelves_result = result.get("shelves", [])
    planogram_shelves = planogram.get("shelves", [])

    for i, shelf_res in enumerate(shelves_result):
        shelf_name = shelf_res.get("name") or (
            planogram_shelves[i]["name"] if i < len(planogram_shelves) else f"Полка {i+1}"
        )
        order_ok = shelf_res.get("order_correct", False)
        confidence = shelf_res.get("confidence", "medium")

        icon = "✅" if order_ok else "❌"
        conf_icon = {"high": "🔵", "medium": "🟡", "low": "🔴"}.get(confidence, "🟡")

        with st.expander(f"{icon} {shelf_name}  {conf_icon} уверенность: {confidence}", expanded=not order_ok):

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**Найдено на полке:**")
                found = shelf_res.get("products_found", [])
                if found:
                    for j, p in enumerate(found):
                        st.markdown(f"`{j+1}.` {p}")
                else:
                    st.markdown("*(товары не обнаружены)*")

            with c2:
                st.markdown("**По планограмме должно быть:**")
                if i < len(planogram_shelves):
                    for j, p in enumerate(planogram_shelves[i]["products"]):
                        st.markdown(f"`{j+1}.` {p}")

            missing = shelf_res.get("missing_products", [])
            extra = shelf_res.get("extra_products", [])
            wrong = shelf_res.get("wrong_order_details", "")

            if missing:
                st.warning(f"⚠️ **Отсутствуют:** {', '.join(missing)}")
            if extra:
                st.info(f"ℹ️ **Лишние товары:** {', '.join(extra)}")
            if wrong and not order_ok:
                st.error(f"🔄 **Нарушение порядка:** {wrong}")
            if order_ok:
                st.success("✅ Порядок соответствует планограмме")

    # Экспорт отчёта
    st.markdown("---")
    report = {
        "timestamp": str(st.session_state.get("history", [{}])[-1].get("timestamp", "")),
        "planogram": planogram["name"],
        "compliance_percent": compliance,
        "critical_violations": violations_list,
        "shelf_details": shelves_result,
        "summary": result.get("summary", "")
    }
    st.download_button(
        "⬇️ Скачать отчёт (JSON)",
        data=json.dumps(report, ensure_ascii=False, indent=2),
        file_name="shelf_report.json",
        mime="application/json"
    )
