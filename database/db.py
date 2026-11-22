import sqlite3
from contextlib import contextmanager
from config import DB_PATH

@contextmanager
def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with open("database/schema.sql", encoding="utf-8") as f:
        schema = f.read()
    with connection() as conn:
        conn.executescript(schema)

def add_subject(name, difficulty="Medium"):
    name = name.strip()
    if not name:
        raise ValueError("Subject name cannot be empty.")
    with connection() as conn:
        cur = conn.execute("INSERT INTO subjects(name,difficulty) VALUES(?,?)", (name, difficulty))
        return cur.lastrowid

def update_subject(subject_id, name, difficulty):
    if not name.strip():
        raise ValueError("Subject name cannot be empty.")
    with connection() as conn:
        conn.execute("UPDATE subjects SET name=?, difficulty=? WHERE id=?", (name.strip(), difficulty, subject_id))

def delete_subject(subject_id):
    with connection() as conn:
        conn.execute("DELETE FROM subjects WHERE id=?", (subject_id,))

def list_subjects():
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM subjects ORDER BY name")]

def add_topic(subject_id, name):
    if not name.strip():
        raise ValueError("Topic cannot be empty.")
    with connection() as conn:
        cur = conn.execute("INSERT INTO topics(subject_id,name) VALUES(?,?)", (subject_id, name.strip()))
        return cur.lastrowid

def list_topics(subject_id=None):
    with connection() as conn:
        if subject_id is None:
            rows = conn.execute("SELECT t.*,s.name AS subject FROM topics t JOIN subjects s ON s.id=t.subject_id ORDER BY s.name,t.name")
        else:
            rows = conn.execute("SELECT * FROM topics WHERE subject_id=? ORDER BY name", (subject_id,))
        return [dict(r) for r in rows]

def set_topic_complete(topic_id, completed):
    with connection() as conn:
        conn.execute("UPDATE topics SET completed=? WHERE id=?", (int(completed), topic_id))

def save_sessions(sessions, exam_date, daily_hours, preferences=""):
    with connection() as conn:
        conn.execute("INSERT INTO plan_metadata(exam_date,daily_hours,preferences) VALUES(?,?,?)",
                     (exam_date, daily_hours, preferences))
        conn.execute("DELETE FROM study_sessions")
        for s in sessions:
            conn.execute("""INSERT INTO study_sessions
                (session_date,subject,topic,session_type,start_time,duration,objective,revision_activity,practice_activity,notes)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (s["date"],s["subject"],s["topic"],s["session_type"],s["start_time"],s["duration"],
                 s.get("objective",""),s.get("revision_activity",""),s.get("practice_activity",""),s.get("notes","")))

def list_sessions():
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM study_sessions ORDER BY session_date,start_time,id")]

def update_session(session_id, **fields):
    allowed = {"session_date","subject","topic","session_type","start_time","duration","objective","revision_activity","practice_activity","notes","status"}
    fields = {k:v for k,v in fields.items() if k in allowed}
    if not fields: return
    sql = ", ".join(f"{k}=?" for k in fields)
    with connection() as conn:
        conn.execute(f"UPDATE study_sessions SET {sql} WHERE id=?", (*fields.values(), session_id))

def delete_session(session_id):
    with connection() as conn:
        conn.execute("DELETE FROM study_sessions WHERE id=?", (session_id,))

def save_chat(role, content):
    with connection() as conn:
        conn.execute("INSERT INTO chat_history(role,content) VALUES(?,?)", (role,content))

def get_chat():
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM chat_history ORDER BY id")]

def clear_chat():
    with connection() as conn:
        conn.execute("DELETE FROM chat_history")

def get_dashboard_data():
    subjects, topics, sessions = list_subjects(), list_topics(), list_sessions()
    total, done = len(sessions), sum(s["status"] == "Completed" for s in sessions)
    return {"subjects":subjects,"topics":topics,"sessions":sessions,"total_sessions":total,
            "completed":done,"percent":round(done/total*100) if total else 0}
