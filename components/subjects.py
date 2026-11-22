import streamlit as st
from database.db import add_subject, update_subject, delete_subject, list_subjects, add_topic, list_topics, set_topic_complete

def render_subjects():
    st.title("Subjects & syllabus")
    with st.expander("Add a subject", expanded=not bool(list_subjects())):
        with st.form("add_subject_form"):
            name=st.text_input("Subject name")
            difficulty=st.selectbox("Difficulty",["Easy","Medium","Hard"])
            submitted=st.form_submit_button("Add subject")
        if submitted:
            try: add_subject(name,difficulty); st.success("Subject added."); st.rerun()
            except Exception as e: st.error(str(e))
    subjects=list_subjects()
    if not subjects:
        st.info("No subjects yet. Add your first subject above.")
        return
    options={f'{s["name"]} · {s["difficulty"]}':s for s in subjects}
    selected=st.selectbox("Select subject",list(options))
    subject=options[selected]
    col1,col2=st.columns([2,1])
    with col1:
        with st.form("edit_subject_form"):
            new_name=st.text_input("Edit subject name",subject["name"])
            new_diff=st.selectbox("Difficulty",["Easy","Medium","Hard"],index=["Easy","Medium","Hard"].index(subject["difficulty"]))
            if st.form_submit_button("Save subject changes"):
                try: update_subject(subject["id"],new_name,new_diff); st.success("Updated."); st.rerun()
                except Exception as e: st.error(str(e))
    with col2:
        st.write("")
        if st.button("Delete subject",type="secondary"):
            delete_subject(subject["id"]); st.success("Subject deleted."); st.rerun()
    with st.form("add_topic_form"):
        topic=st.text_input("New syllabus topic")
        if st.form_submit_button("Add topic"):
            try: add_topic(subject["id"],topic); st.success("Topic added."); st.rerun()
            except Exception as e: st.error(str(e))
    st.subheader(f'{subject["name"]} topics')
    topics=list_topics(subject["id"])
    if not topics: st.caption("No topics added yet.")
    for t in topics:
        checked=st.checkbox(t["name"],value=bool(t["completed"]),key=f'topic_{t["id"]}')
        if int(checked)!=t["completed"]:
            set_topic_complete(t["id"],checked); st.rerun()
