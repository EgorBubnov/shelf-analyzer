import streamlit as st
import json


def show():
    st.title("История")
    st.markdown('<p class="page-meta">Журнал всех проверок выкладки</p>', unsafe_allow_html=True)

    if "history" not in st.session_state or not st.session_state.history:
        st.markdown("<div style='color:#94a3b8;font-size:14px;padding:40px 0'>Проверок пока нет — перейдите в раздел «Анализ», чтобы начать</div>", unsafe_allow_html=True)
        return

    history = st.session_state.history
    compliances = [e["result"].get("overall_compliance", 0) for e in history]
    avg = sum(compliances) / len(compliances)
    total_v = sum(len(e["result"].get("critical_violations", [])) for e in history)

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-label">Проверок</div><div class="kpi-val">{len(history)}</div></div>
        <div class="kpi"><div class="kpi-label">Среднее соответствие</div><div class="kpi-val {'green' if avg>=80 else 'amber' if avg>=50 else 'red'}">{avg:.0f}%</div></div>
        <div class="kpi"><div class="kpi-label">Нарушений всего</div><div class="kpi-val {'red' if total_v else 'green'}">{total_v}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    for i, entry in enumerate(reversed(history)):
        result = entry["result"]
        pct = result.get("overall_compliance", 0)
        v_count = len(result.get("critical_violations", []))
        color = "#16a34a" if pct >= 80 else ("#d97706" if pct >= 50 else "#dc2626")

        with st.expander(f"{entry['timestamp']}  —  {entry['filename']}  —  {pct}%", expanded=(i == 0)):
            c1, c2 = st.columns([1, 2])
            with c1:
                if "image_bytes" in entry:
                    st.image(entry["image_bytes"], use_container_width=True)
            with c2:
                st.markdown(f"""
                <div style="font-size:13px;line-height:2">
                    <div><span style="color:#94a3b8">Планограмма:</span> {entry['planogram_name']}</div>
                    <div><span style="color:#94a3b8">Соответствие:</span> <span style="color:{color};font-weight:600">{pct}%</span></div>
                    <div><span style="color:#94a3b8">Нарушений:</span> {v_count}</div>
                </div>
                """, unsafe_allow_html=True)
                summary = result.get("summary", "")
                if summary:
                    st.markdown(f'<div style="font-size:13px;color:#374151;margin-top:8px;line-height:1.6">{summary}</div>', unsafe_allow_html=True)
                if result.get("critical_violations"):
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                    for v in result["critical_violations"]:
                        st.markdown(f'<div class="violation-row">{v}</div>', unsafe_allow_html=True)

            report_data = {
                "timestamp": entry["timestamp"],
                "filename": entry["filename"],
                "planogram": entry["planogram_name"],
                "compliance_percent": pct,
                "critical_violations": result.get("critical_violations", []),
                "summary": result.get("summary", ""),
                "shelf_details": result.get("shelves", [])
            }
            st.download_button(
                "Скачать отчёт",
                data=json.dumps(report_data, ensure_ascii=False, indent=2),
                file_name=f"report_{entry['timestamp'].replace(':', '-').replace(' ', '_')}.json",
                mime="application/json",
                key=f"dl_{i}"
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Очистить историю"):
        st.session_state.history = []
        if "last_result" in st.session_state:
            del st.session_state.last_result
        st.rerun()