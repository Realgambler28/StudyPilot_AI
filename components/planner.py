from datetime import date
import streamlit as st
from database.db import list_subjects, list_topics, save_sessions
from services.timetable_service import days_remaining, validate_sessions, rule_based_plan
from services.gemini_service import generate_plan

def render_planner():
    st.title("AI study plan generator")
    subjects=list_subjects()
    if not subjects:
        st.warning("Add subjects and syllabus topics first.")
        return
    with st.form("planner_form"):
        exam=st.date_input("Examination date",min_value=date.today())
        hours=st.number_input("Available study hours per day",min_value=0.5,max_value=16.0,value=3.0,step=0.5)
        start=st.time_input("Preferred daily start time")
        weekend=st.selectbox("Weekend preference",["Study as usual","Light study","Keep weekends free"])
        instructions=st.text_area("Additional instructions (optional)",placeholder="e.g. Keep 30 minutes for daily revision.")
        submitted=st.form_submit_button("Generate my study plan",type="primary")
    if submitted:
        st.session_state.fallback_exam = exam.isoformat()
        st.session_state.fallback_hours = float(hours)
        left=days_remaining(exam)
        if left <= 0:
            st.error("Choose an examination date in the future.")
            return
        payload=[]
        for s in subjects:
            ts=list_topics(s["id"])
            if not ts:
                st.error(f'Add at least one topic for {s["name"]}.')
                return
            payload.append({"name":s["name"],"difficulty":s["difficulty"],"topics":[{"name":t["name"]} for t in ts]})
        prefs=f"Start at {start.strftime('%H:%M')}; {weekend}; {instructions}"
        try:
            with st.spinner("Asking Gemini to build your personalized plan..."):
                sessions,prompt=generate_plan(payload,exam.isoformat(),left,hours,prefs)
            validate_sessions(sessions,exam,hours)
            save_sessions(sessions,exam.isoformat(),hours,prefs)
            st.session_state.last_prompt=prompt
            st.success(f"AI-generated plan saved: {len(sessions)} sessions across {left} days remaining.")
            st.dataframe(sessions,use_container_width=True)
            st.download_button("Download timetable CSV",_csv(sessions),"studypilot_timetable.csv","text/csv")
        except Exception as e:
            st.error(f"AI plan generation failed: {e}")
            st.caption("No fallback was silently substituted. You can explicitly create a rule-based plan below.")
    st.divider()
    st.subheader("Optional offline fallback")
    st.caption("This uses a deterministic rule-based scheduler and is not AI-generated.")
    if st.button("Create rule-based plan"):
        try:
            payload=[{"name":s["name"],"difficulty":s["difficulty"],"topics":[{"name":t["name"]} for t in list_topics(s["id"])]} for s in subjects]
            exam=st.session_state.get("fallback_exam")
            if not exam:
                st.info("Set an exam date in the form above, then submit it once before using fallback.")
            else:
                hours=float(st.session_state.get("fallback_hours",3.0))
                sessions=rule_based_plan(payload,exam,hours)
                validate_sessions(sessions,exam,hours)
                save_sessions(sessions,exam,hours,"Rule-based fallback")
                st.success("Rule-based plan saved (not AI-generated).")
        except Exception as e: st.error(str(e))

def _csv(sessions):
    import pandas as pd
    return pd.DataFrame(sessions).to_csv(index=False).encode("utf-8")
