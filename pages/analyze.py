import streamlit as st
import json
import datetime
from utils.vision import analyze_shelf_image, resize_image_for_display


def show():
    st.title("Анализ фото")
    st.markdown('<p class="page-meta">Загрузите фотографию прилавка — система сравнит выкладку с планограммой</p>', unsafe_allow_html=True)

    if "planogram" not in st.session_state:
        st.warning("Сначала создайте планограмму в разделе «Планограмма»")
        return

    planogram = st.session_state.planogram
    if sum(len(s["products"]) for s in planogram["shelves"]) == 0:
        st.warning("Планограмма пустая — добавьте товары в разделе «Планограмма»")
        return

    with st.expander("Настройки API", expanded=False):
        try:
            default_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            default_key = ""
        api_key = st.text_input("API Key", type="password",
                                value=st.session_state.get("api_key", default_key))
        if api_key:
            st.session_state.api_key = api_key

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("**Фото прилавка**")
        uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if uploaded:
            image_bytes = uploaded.read()
            display_bytes = resize_image_for_display(image_bytes)
            st.image(display_bytes, use_container_width=True)

    with col_r:
        st.markdown("**Активная планограмма**")
        st.markdown(f"<div style='font-size:13px;font-weight:600;color:#0f172a;margin-bottom:10px'>{planogram['name']}</div>", unsafe_allow_html=True)
        for shelf in planogram["shelves"]:
            if shelf["products"]:
                prods = " → ".join(shelf["products"])
                st.markdown(f"<div style='font-size:12.5px;color:#374151;margin-bottom:6px'><span style='font-weight:600'>{shelf['name']}:</span> {prods}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    can_run = bool(uploaded and st.session_state.get("api_key"))
    if not st.session_state.get("api_key"):
        st.caption("Введите API ключ в настройках выше")

    if st.button("Запустить анализ", disabled=not can_run, type="primary", use_container_width=True):
        with st.spinner("Анализирую..."):
            try:
                result = analyze_shelf_image(image_bytes, planogram, st.session_state.api_key)
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({
                    "timestamp": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "filename": uploaded.name,
                    "planogram_name": planogram["name"],
                    "result": result,
                    "image_bytes": display_bytes
                })
                st.session_state.last_result = result
            except json.JSONDecodeError:
                st.error("Модель вернула некорректный ответ — попробуйте ещё раз")
                st.stop()
            except Exception as e:
                st.error(f"Ошибка анализа: {e}")
                st.stop()

    if "last_result" in st.session_state and uploaded:
        _render_results(st.session_state.last_result, planogram)


def _render_results(result: dict, planogram: dict):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.title("Результаты")

    pct = result.get("overall_compliance", 0)
    violations = result.get("critical_violations", [])
    shelves_r = result.get("shelves", [])
    plan_shelves = planogram.get("shelves", [])

    # Цвет
    if pct >= 80:
        bar_color, kpi_cls, sum_cls = "#16a34a", "green", "summary-ok"
    elif pct >= 50:
        bar_color, kpi_cls, sum_cls = "#d97706", "amber", "summary-mid"
    else:
        bar_color, kpi_cls, sum_cls = "#dc2626", "red", "summary-bad"

    # KPI
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-label">Соответствие</div><div class="kpi-val {kpi_cls}">{pct}%</div></div>
        <div class="kpi"><div class="kpi-label">Нарушений</div><div class="kpi-val {'red' if violations else 'green'}">{len(violations)}</div></div>
        <div class="kpi"><div class="kpi-label">Полок</div><div class="kpi-val">{result.get('shelves_detected', len(shelves_r))}</div></div>
    </div>
    <div class="bar-wrap"><div class="bar" style="width:{pct}%;background:{bar_color}"></div></div>
    """, unsafe_allow_html=True)

    summary = result.get("summary", "")
    if summary:
        st.markdown(f'<div class="summary-box {sum_cls}">{summary}</div>', unsafe_allow_html=True)

    if violations:
        st.markdown('<div class="violations-title">Критические нарушения</div>', unsafe_allow_html=True)
        for v in violations:
            st.markdown(f'<div class="violation-row">{v}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**Детали по полкам**")

    for i, sr in enumerate(shelves_r):
        name = sr.get("name") or (plan_shelves[i]["name"] if i < len(plan_shelves) else f"Полка {i+1}")
        ok = sr.get("order_correct", False)
        conf = sr.get("confidence", "medium")
        conf_label = {"high": "Высокая", "medium": "Средняя", "low": "Низкая"}.get(conf, conf)
        badge_cls = "conf-ok" if ok else ("conf-mid" if conf == "medium" else "conf-fail")
        status_cls = "conf-ok" if ok else "conf-fail"
        status_txt = "Соответствует" if ok else "Нарушение"

        found   = sr.get("products_found", [])
        missing = sr.get("missing_products", [])
        extra   = sr.get("extra_products", [])
        wrong   = sr.get("wrong_order_details", "")

        found_html = "".join([f'<div class="prod-row"><span class="prod-num">{j+1}</span>{p}</div>' for j, p in enumerate(found)]) or "<div style='color:#94a3b8;font-size:13px'>Не обнаружено</div>"
        plan_html  = "".join([f'<div class="prod-row"><span class="prod-num">{j+1}</span>{p}</div>' for j, p in enumerate(plan_shelves[i]["products"]) if i < len(plan_shelves)]) if i < len(plan_shelves) else ""

        miss_html  = "".join([f'<span class="tag tag-miss">нет: {p}</span>' for p in missing])
        extra_html = "".join([f'<span class="tag tag-extra">лишний: {p}</span>' for p in extra])
        ok_html    = '<span class="tag tag-note">Порядок соответствует планограмме</span>' if ok else ""
        wrong_html = f'<div style="font-size:12.5px;color:#92400e;margin-top:8px">{wrong}</div>' if wrong and not ok else ""

        st.markdown(f"""
        <div class="shelf-card">
            <div class="shelf-card-head">
                <span class="shelf-card-name">{name}</span>
                <span>
                    <span class="conf-badge {status_cls}">{status_txt}</span>
                    &nbsp;
                    <span class="conf-badge {badge_cls}" style="background:transparent;border:1px solid #e2e8f0;color:#64748b">уверенность: {conf_label}</span>
                </span>
            </div>
            <div class="shelf-card-body">
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-title">Найдено на полке</div>', unsafe_allow_html=True)
            st.markdown(found_html, unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="col-title">По планограмме</div>', unsafe_allow_html=True)
            st.markdown(plan_html, unsafe_allow_html=True)

        st.markdown(f'<div class="tag-row">{miss_html}{extra_html}{ok_html}{wrong_html}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    report = {
        "timestamp": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "planogram": planogram["name"],
        "compliance_percent": pct,
        "critical_violations": violations,
        "shelf_details": shelves_r,
        "summary": summary
    }
    st.download_button(
        "Скачать отчёт",
        data=json.dumps(report, ensure_ascii=False, indent=2),
        file_name="shelf_report.json",
        mime="application/json"
    )