import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_dashboard_data

def render_dashboard(go):
    data = get_dashboard_data()
    st.title("Good study starts with a clear plan.")
    st.caption("Your personal command center for exam preparation.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Subjects", len(data["subjects"]))
    c2.metric("Syllabus topics", len(data["topics"]))
    c3.metric("Planned sessions", data["total_sessions"])
    c4.metric("Preparation", f'{data["percent"]}%')
    st.progress(data["percent"]/100)
    left,right = st.columns([1.35,1])
    with left:
        st.subheader("Subject-wise syllabus")
        if data["topics"]:
            df = pd.DataFrame(data["topics"])
            summary = df.groupby("subject")["completed"].agg(["sum","count"]).reset_index()
            summary["Pending"] = summary["count"]-summary["sum"]
            fig = px.bar(summary, x="subject", y=["sum","Pending"], barmode="stack",
                         labels={"subject":"Subject","value":"Topics","variable":"Status"})
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("Add subjects and syllabus topics to see your preparation overview.")
    with right:
        st.subheader("Upcoming sessions")
        upcoming = [s for s in data["sessions"] if s["status"] != "Completed"][:5]
        if upcoming:
            for s in upcoming:
                st.markdown(f"**{s['session_date']} · {s['start_time']}**  \n{s['subject']} — {s['topic']}")
        else: st.info("No upcoming sessions yet. Generate your first plan.")
    st.divider()
    a,b,c = st.columns(3)
    if a.button("Manage subjects",use_container_width=True): go("Subjects & Syllabus")
    if b.button("Generate AI plan",use_container_width=True): go("AI Plan Generator")
    if c.button("Open timetable",use_container_width=True): go("Timetable")
