from datetime import date, datetime, timedelta
from collections import defaultdict

REQUIRED = {"date","subject","topic","session_type","start_time","duration"}

def days_remaining(exam_date, today=None):
    today = today or date.today()
    if isinstance(exam_date, str):
        exam_date = date.fromisoformat(exam_date)
    return (exam_date - today).days

def validate_sessions(sessions, exam_date, daily_hours, today=None):
    today = today or date.today()
    exam = date.fromisoformat(exam_date) if isinstance(exam_date, str) else exam_date
    if exam <= today:
        raise ValueError("Exam date must be in the future.")
    totals = defaultdict(float)
    for i, s in enumerate(sessions):
        missing = REQUIRED - set(s)
        if missing:
            raise ValueError(f"Session {i+1} missing fields: {', '.join(sorted(missing))}")
        day = date.fromisoformat(s["date"])
        if day < today:
            raise ValueError(f"Session date {day} is in the past.")
        if day >= exam:
            raise ValueError(f"Session date {day} must be before exam date {exam}.")
        duration = float(s["duration"])
        if duration <= 0:
            raise ValueError("Session duration must be positive.")
        datetime.strptime(s["start_time"], "%H:%M")
        totals[day] += duration
        if totals[day] > float(daily_hours) + 1e-6:
            raise ValueError(f"Daily limit exceeded on {day}: {totals[day]} hours.")
    return True

def rule_based_plan(subjects, exam_date, daily_hours, start_date=None):
    """Clearly labelled non-AI fallback for offline demonstrations."""
    start = start_date or date.today()
    exam = date.fromisoformat(exam_date) if isinstance(exam_date, str) else exam_date
    slots = []
    topics = [(s["name"], t["name"], s.get("difficulty","Medium")) for s in subjects for t in s["topics"]]
    if not topics: raise ValueError("Add at least one syllabus topic before planning.")
    available = (exam - start).days
    if available <= 0: raise ValueError("Exam date must be in the future.")
    cursor = 0
    for offset in range(available):
        day = start + timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        used, start_minutes = 0.0, 9*60
        while used + 0.5 <= daily_hours and cursor < len(topics):
            subject, topic, difficulty = topics[cursor % len(topics)]
            duration = min(1.0 if difficulty == "Hard" else 0.75, daily_hours-used)
            if duration < .5: break
            slots.append({"date":day.isoformat(),"subject":subject,"topic":topic,
                "session_type":"Learning","start_time":f"{start_minutes//60:02d}:{start_minutes%60:02d}",
                "duration":duration,"objective":f"Understand and summarize {topic}",
                "revision_activity":f"Recall key points from {topic}",
                "practice_activity":f"Solve practice questions on {topic}","notes":"Rule-based fallback — not AI-generated."})
            used += duration
            start_minutes += int(duration*60)+15
            cursor += 1
        if cursor >= len(topics): break
    return slots
