import streamlit as st
import pandas as pd
from datetime import date, time
from database.db import list_sessions, update_session, delete_session

def render_timetable():
    st.title("Your study timetable")
    sessions=list_sessions()
    if not sessions:
        st.info("Your timetable is empty. Generate a plan to populate it.")
        return
    df=pd.DataFrame(sessions)
    subjects=["All"]+sorted(df.subject.unique().tolist())
    selected=st.selectbox("Filter by subject",subjects)
    if selected!="All": df=df[df.subject==selected]
    statuses=["All","Not Started","In Progress","Completed"]
    status=st.selectbox("Filter by status",statuses)
    if status!="All": df=df[df.status==status]
    st.dataframe(df[["session_date","start_time","subject","topic","session_type","duration","status"]],use_container_width=True,hide_index=True)
    st.download_button("Export filtered timetable as CSV",df.to_csv(index=False).encode("utf-8"),"studypilot_timetable.csv","text/csv")
    st.subheader("Update a session")
    all_sessions=list_sessions()
    labels={f'#{s["id"]} · {s["session_date"]} · {s["subject"]}: {s["topic"]}':s for s in all_sessions}
    chosen=st.selectbox("Select session",list(labels))
    s=labels[chosen]
    with st.form("session_update"):
        status_new=st.selectbox("Status",["Not Started","In Progress","Completed"],index=["Not Started","In Progress","Completed"].index(s["status"]))
        session_day=st.date_input("Session date",value=date.fromisoformat(s["session_date"]))
        session_start=st.time_input("Start time",value=time.fromisoformat(s["start_time"]))
        topic=st.text_input("Topic",s["topic"])
        duration=st.number_input("Duration (hours)",min_value=.25,max_value=16.0,value=float(s["duration"]),step=.25)
        submitted=st.form_submit_button("Save session")
    if submitted:
        update_session(s["id"],status=status_new,session_date=session_day.isoformat(),start_time=session_start.strftime("%H:%M"),topic=topic,duration=duration)
        st.success("Session updated."); st.rerun()
    if st.button("Delete selected session"):
        delete_session(s["id"]); st.success("Session deleted."); st.rerun()
