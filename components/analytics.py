import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_dashboard_data

def render_analytics():
    st.title("Progress & analytics")
    data=get_dashboard_data(); sessions=data["sessions"]
    st.metric("Overall session completion",f'{data["percent"]}%')
    st.progress(data["percent"]/100)
    if not sessions:
        st.info("Generate a timetable to unlock study analytics.")
        return
    df=pd.DataFrame(sessions)
    df["duration"]=pd.to_numeric(df["duration"])
    done=df[df.status=="Completed"]
    a,b,c=st.columns(3)
    a.metric("Completed sessions",len(done))
    b.metric("Pending sessions",len(df)-len(done))
    c.metric("Study hours completed",f'{done.duration.sum():.1f} h')
    by_subject=df.groupby("subject").agg(Planned=("id","count"),Completed=("status",lambda x:(x=="Completed").sum())).reset_index()
    fig=px.bar(by_subject,x="subject",y=["Completed","Planned"],barmode="group",title="Sessions by subject")
    st.plotly_chart(fig,use_container_width=True)
    types=df.groupby("session_type").size().reset_index(name="Sessions")
    st.plotly_chart(px.pie(types,names="session_type",values="Sessions",title="Session mix"),use_container_width=True)
