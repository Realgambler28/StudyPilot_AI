import streamlit as st
from config import APP_NAME
from database.db import init_db, get_dashboard_data
from components.dashboard import render_dashboard
from components.subjects import render_subjects
from components.timetable import render_timetable
from components.assistant import render_assistant
from components.analytics import render_analytics

st.set_page_config(page_title=APP_NAME, page_icon="📘", layout="wide", initial_sidebar_state="expanded")
init_db()

st.markdown("""
<style>
:root { --ink:#17233d; --muted:#64748b; --accent:#6657d9; }
[data-testid="stAppViewContainer"] { background:#f5f7fc; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#111a31,#202b4b); }
[data-testid="stSidebar"] * { color:#f4f6ff !important; }
.block-container { padding-top:1.8rem; max-width:1450px; }
div[data-testid="stMetric"] { background:white; border:1px solid #e8ebf4; padding:16px; border-radius:14px; box-shadow:0 4px 18px rgba(30,41,59,.04); }
h1,h2,h3 { color:#17233d; }
.stButton>button { border-radius:9px; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Overview"

def go(page):
    st.session_state.page = page

with st.sidebar:
    st.markdown("# StudyPilot AI")
    st.caption("Your Personal AI Exam Command Center")
    st.divider()
    for label, icon in [("Overview","⌂"),("Subjects & Syllabus","▤"),("AI Plan Generator","✦"),("Timetable","▦"),("AI Study Assistant","◉"),("Progress & Analytics","▥")]:
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            go(label)
    st.divider()
    st.caption("GenAI Mini Project · Problem Statement 25")
    st.caption("Student: Shivam Mhamane · Roll No. 25")

page = st.session_state.page
if page == "Overview":
    render_dashboard(go)
elif page == "Subjects & Syllabus":
    render_subjects()
elif page == "AI Plan Generator":
    from components.planner import render_planner
    render_planner()
elif page == "Timetable":
    render_timetable()
elif page == "AI Study Assistant":
    render_assistant()
elif page == "Progress & Analytics":
    render_analytics()
