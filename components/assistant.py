import streamlit as st
from database.db import get_chat, save_chat, clear_chat, list_subjects, list_sessions
from services.gemini_service import chat

def render_assistant():
    st.title("Gemini AI study assistant")
    st.caption("Ask for explanations, quizzes, mnemonics, revision strategies, or help catching up.")
    if st.button("Clear conversation"):
        clear_chat(); st.rerun()
    suggestions=["Explain a difficult topic in simple language.","Create 5 MCQs from my syllabus.","Make a quick revision quiz.","Suggest a plan if I am falling behind."]
    cols=st.columns(2)
    for i,p in enumerate(suggestions):
        if cols[i%2].button(p,key=f"suggest_{i}"):
            st.session_state.chat_input=p
    for m in get_chat():
        with st.chat_message(m["role"]): st.markdown(m["content"])
    prompt=st.chat_input("Ask StudyPilot AI...")
    if not prompt: prompt=st.session_state.pop("chat_input",None)
    if prompt:
        save_chat("user",prompt)
        subjects=list_subjects(); sessions=list_sessions()
        context=f"Subjects: {subjects}\nUpcoming sessions: {[s for s in sessions if s['status']!='Completed'][:10]}"
        history=get_chat()
        try:
            with st.spinner("StudyPilot is thinking..."):
                answer=chat(history,context)
            save_chat("model",answer)
            st.rerun()
        except Exception as e:
            st.error(f"Gemini request failed: {e}")
