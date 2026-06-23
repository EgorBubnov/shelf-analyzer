import streamlit as st
import json
import datetime
from utils.vision import analyze_shelf_image, resize_image_for_display


def show():
    st.markdown('<div class="page-eyebrow">Проверка выкладки</div>', unsafe_allow_html=True)
    st.title("Анализ фото")
    st.markdown('<p class="page-desc">Загрузите фронтальное фото прилавка — система сравнит фактическую выкладку с планограммой и укажет нарушения.</p>', unsafe_allow_html=True)

    if "planogram" not in st.session_state:
        st.warning("Сначала настройте планограмму в соответствующем разделе.")
        return

    planogram = st.session_state.planogram
    if sum(len(s["products"]) for s in planogram["shelves"]) == 0:
        st.warning("Планограмма пустая — добавьте товары.")
        return

    # Автоматическое получение API ключа из secrets без вывода интерфейса конфигурации
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        api_key = ""

    col_l, col_r = st.columns([5, 4])

    with col_l:
        st.markdown('<div class="col-lbl">Фото прилавка</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if uploaded:
            image_bytes = uploaded.read()
            display_bytes = resize_image_for_display(image_bytes)
            st.image(display_bytes, use_container_width=True)

    with col_r:
        st.markdown('<div class="col-lbl">Активная планограмма</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#F5F0E8;margin-bottom:14px">{planogram["name"]}</div>', unsafe_allow_html=True)
        for shelf in planogram["shelves"]:
            if shelf["products"]:
                prods = " → ".join(shelf["products"])
                st.markdown(f"""
                <div style="margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #2E2E2C">
                    <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.18em;text-transform:uppercase;color:#8C8C7A;margin-bottom:4px">{shelf['name']}</div>
                    <div style="font-size:12.5px;color:#E5E5E0;line-height:1.5">{prods}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)

    can_run = bool(uploaded and api_key)
    if not api_key:
        st.caption("Ошибка конфигурации: в secrets не найден API ключ.")

    if st.button("Запустить анализ", disabled=not can_run, type="primary", use_container_width=True):
        with st.spinner("Анализирую выкладку..."):
            try:
                result = analyze_shelf_image(image_bytes, planogram, api_key)
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
                st.error("Некорректный ответ модели — попробуйте ещё раз")
                st.stop()
            except Exception as e:
                st.error(f"Ошибка: {e}")
                st.stop()

    if "last_result" in st.session_state and uploaded:
        _render(st.session_state.last_result, planogram)


def _render(result: dict, planogram: dict):
    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    st.markdown('<div class="page-eyebrow">Результат</div>', unsafe_allow_html=True)
    st.title("Отчёт о выкладке")

    pct        = result.get("overall_compliance", 0)
    violations = result.get("critical_violations", [])
    shelves_r  = result.get("shelves", [])
    plan_sh    = planogram.get("shelves", [])

    if pct >= 80:
        bar_color, kpi_cls, sum_cls = "#A3E635", "ok",  "ok"
    elif pct >= 50:
        bar_color, kpi_cls, sum_cls = "#F59E0B", "mid", "mid"
    else:
        bar_color, kpi_cls, sum_cls = "#D4401A", "red", "bad"

    # KPI метрики
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card accent">
            <div class="kpi-lbl">Соответствие планограмме</div>
            <div class="kpi-num {kpi_cls}">{pct}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-lbl">Критических нарушений</div>
            <div class="kpi-num {'red' if violations else 'ok'}">{len(violations)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-lbl">Полок распознано</div>
            <div class="kpi-num">{result.get('shelves_detected', len(shelves_r))}</div>
        </div>
    </div>
    <div class="comp-wrap"><div class="comp-fill" style="width:{pct}%;background:{bar_color}"></div></div>
    <div class="comp-label">{pct} / 100</div>
    """, unsafe_allow_html=True)

    summary = result.get("summary", "")
    if summary:
        st.markdown(f'<div class="sum-box {sum_cls}">{summary}</div>', unsafe_allow_html=True)

    if violations:
        st.markdown('<div class="viol-lbl">Критические нарушения</div>', unsafe_allow_html=True)
        for v in violations:
            st.markdown(f'<div class="viol-row">{v}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    st.markdown('<div class="page-eyebrow">Детализация</div>', unsafe_allow_html=True)
    st.markdown("**Анализ по полкам**")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for i, sr in enumerate(shelves_r):
        name    = sr.get("name") or (plan_sh[i]["name"] if i < len(plan_sh) else f"Полка {i+1}")
        ok      = sr.get("order_correct", False)
        conf    = sr.get("confidence", "medium")
        conf_ru = {"high": "высокая", "medium": "средняя", "low": "низкая"}.get(conf, conf)
        s_chip  = f'<span class="chip chip-ok">OK</span>' if ok else f'<span class="chip chip-bad">Нарушение</span>'
        c_chip  = f'<span class="chip chip-mid" style="margin-left:8px">уверенность: {conf_ru}</span>'

        found   = sr.get("products_found", [])
        missing = sr.get("missing_products", [])
        extra   = sr.get("extra_products", [])
        wrong   = sr.get("wrong_order_details", "")

        found_html = "".join([f'<div class="prod-item"><span class="prod-idx">{j+1}</span>{p}</div>' for j, p in enumerate(found)]) \
                     or '<div style="color:#8C8C7A;font-size:12px;font-style:italic">Товары не обнаружены</div>'
        plan_html  = "".join([f'<div class="prod-item"><span class="prod-idx">{j+1}</span>{p}</div>' for j, p in enumerate(plan_sh[i]["products"])]) \
                     if i < len(plan_sh) else ""

        miss_html  = "".join([f'<span class="tag tag-miss">нет: {p}</span>'    for p in missing])
        extra_html = "".join([f'<span class="tag tag-extra">лишний: {p}</span>' for p in extra])
        ok_tag     = '<span class="tag tag-ok">Порядок верен</span>' if ok else ""
        wrong_html = f'<div class="wrong-note">{wrong}</div>' if wrong and not ok else ""

        st.markdown(f"""
        <div class="shelf-wrap">
            <div class="shelf-head">
                <span class="shelf-title">{name}</span>
                <span>{s_chip}{c_chip}</span>
            </div>
            <div class="shelf-body">
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="col-lbl">Найдено на полке</div>{found_html}', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="col-lbl">По планограмме</div>{plan_html}', unsafe_allow_html=True)

        st.markdown(f'<div class="tag-row">{miss_html}{extra_html}{ok_tag}</div>{wrong_html}', unsafe_allow_html=True)
        st.markdown("</div></div><div style='height:2px'></div>", unsafe_allow_html=True)

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
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