import streamlit as st
import json


def show():
    st.title("📊 История анализов")

    if "history" not in st.session_state or not st.session_state.history:
        st.info("Здесь будет отображаться история проверок прилавков после первого анализа.")
        st.markdown("Перейдите в **📸 Анализ фото**, чтобы начать.")
        return

    history = st.session_state.history

    # Сводная статистика
    st.subheader("Общая статистика")
    compliances = [e["result"].get("overall_compliance", 0) for e in history]
    avg_compliance = sum(compliances) / len(compliances) if compliances else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Всего проверок", len(history))
    m2.metric("Среднее соответствие", f"{avg_compliance:.0f}%")
    violations_total = sum(len(e["result"].get("critical_violations", [])) for e in history)
    m3.metric("Нарушений выявлено", violations_total)

    st.markdown("---")

    # Таблица проверок
    st.subheader("Журнал проверок")

    for i, entry in enumerate(reversed(history)):
        result = entry["result"]
        compliance = result.get("overall_compliance", 0)
        color = "🟢" if compliance >= 80 else ("🟡" if compliance >= 50 else "🔴")
        violations = len(result.get("critical_violations", []))

        with st.expander(
            f"{color} {entry['timestamp']} — {entry['filename']} — {compliance}% соответствия",
            expanded=(i == 0)
        ):
            c1, c2 = st.columns([1, 2])
            with c1:
                if "image_bytes" in entry:
                    st.image(entry["image_bytes"], caption=entry["filename"], use_container_width=True)
            with c2:
                st.markdown(f"**Планограмма:** {entry['planogram_name']}")
                st.markdown(f"**Соответствие:** {color} {compliance}%")
                st.markdown(f"**Нарушений:** {violations}")
                summary = result.get("summary", "")
                if summary:
                    st.markdown(f"**Резюме:** {summary}")

                if result.get("critical_violations"):
                    st.markdown("**Нарушения:**")
                    for v in result["critical_violations"]:
                        st.markdown(f"• {v}")

            # Экспорт отдельной записи
            report_data = {
                "timestamp": entry["timestamp"],
                "filename": entry["filename"],
                "planogram": entry["planogram_name"],
                "compliance_percent": compliance,
                "critical_violations": result.get("critical_violations", []),
                "summary": result.get("summary", ""),
                "shelf_details": result.get("shelves", [])
            }
            st.download_button(
                f"⬇️ Отчёт",
                data=json.dumps(report_data, ensure_ascii=False, indent=2),
                file_name=f"report_{entry['timestamp'].replace(':', '-').replace(' ', '_')}.json",
                mime="application/json",
                key=f"dl_{i}"
            )

    # Кнопка очистки истории
    st.markdown("---")
    if st.button("🗑️ Очистить историю", type="secondary"):
        st.session_state.history = []
        if "last_result" in st.session_state:
            del st.session_state.last_result
        st.rerun()
