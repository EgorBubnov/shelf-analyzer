import streamlit as st
import json


def show():
    
    st.title("История проверок")
    st.markdown('<p class="page-desc">Все проведённые анализы выкладки в хронологическом порядке.</p>', unsafe_allow_html=True)

    if "history" not in st.session_state or not st.session_state.history:
        st.markdown("""
        <div style="padding:48px 0;color:#8C8C7A;font-size:14px;border-top:1px solid #DDD9CF">
            Проверок пока нет. Перейдите в раздел «Анализ», чтобы начать.
        </div>
        """, unsafe_allow_html=True)
        return

    history = st.session_state.history
    compliances = [e["result"].get("overall_compliance", 0) for e in history]
    avg = sum(compliances) / len(compliances)
    total_v = sum(len(e["result"].get("critical_violations", [])) for e in history)

    avg_cls = "ok" if avg >= 80 else ("mid" if avg >= 50 else "red")
    viol_cls = "red" if total_v else "ok"

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-lbl">Проверок</div><div class="kpi-num">{len(history)}</div></div>
        <div class="kpi-card accent"><div class="kpi-lbl">Среднее соответствие</div><div class="kpi-num {avg_cls}">{avg:.0f}%</div></div>
        <div class="kpi-card"><div class="kpi-lbl">Нарушений выявлено</div><div class="kpi-num {viol_cls}">{total_v}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)

    for i, entry in enumerate(reversed(history)):
        result = entry["result"]
        pct = result.get("overall_compliance", 0)
        v_count = len(result.get("critical_violations", []))
        color = "#2D6A4F" if pct >= 80 else ("#B45309" if pct >= 50 else "#D4401A")

        with st.expander(f"{entry['timestamp']}  ·  {entry['filename']}  ·  {pct}%", expanded=(i == 0)):
            c1, c2 = st.columns([1, 2])
            with c1:
                if "image_bytes" in entry:
                    st.image(entry["image_bytes"], use_container_width=True)
            with c2:
                st.markdown(f"""
                <div style="font-size:13px;line-height:1">
                    <div style="margin-bottom:14px">
                        <div class="col-lbl">Планограмма</div>
                        <div style="color:#1C1C1A;font-weight:500">{entry['planogram_name']}</div>
                    </div>
                    <div style="margin-bottom:14px">
                        <div class="col-lbl">Соответствие</div>
                        <div style="color:{color};font-family:'DM Mono',monospace;font-size:22px;font-weight:500">{pct}%</div>
                    </div>
                    <div>
                        <div class="col-lbl">Нарушений</div>
                        <div style="color:#1C1C1A;font-weight:500">{v_count}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                summary = result.get("summary", "")
                if summary:
                    st.markdown(f'<div style="margin-top:16px;font-size:13px;color:#3A3A36;line-height:1.6;border-left:2px solid #DDD9CF;padding-left:14px">{summary}</div>', unsafe_allow_html=True)

                if result.get("critical_violations"):
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                    for v in result["critical_violations"]:
                        st.markdown(f'<div class="viol-row">{v}</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
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

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    if st.button("Очистить историю"):
        st.session_state.history = []
        if "last_result" in st.session_state:
            del st.session_state.last_result
        st.rerun()
