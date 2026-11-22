import json
import re
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is missing. Add GEMINI_API_KEY to your .env file.")
    return genai.Client(api_key=GEMINI_API_KEY)

def _text(response):
    return getattr(response, "text", None) or ""

def generate_plan(subjects, exam_date, days_left, daily_hours, preferences=""):
    prompt = f"""You are an expert academic study planner. Create a realistic day-wise study plan.
Return ONLY valid JSON with top-level key "sessions", an array of objects with:
date (YYYY-MM-DD), subject, topic, session_type, start_time (HH:MM), duration (number of hours),
objective, revision_activity, practice_activity, notes.
Use only supplied subjects and topics. Balance subjects by topic count and difficulty.
Include learning, active recall, practice, revision and mock tests where time permits.
Never schedule on/after the exam date. Daily total must not exceed {daily_hours} hours.
Exam date: {exam_date}; days remaining: {days_left}; daily limit: {daily_hours} hours.
Preferences: {preferences}
Subjects and topics: {json.dumps(subjects, ensure_ascii=False)}
"""
    response = _client().models.generate_content(model=GEMINI_MODEL, contents=prompt)
    raw = _text(response).strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    data = json.loads(raw)
    if not isinstance(data, dict) or not isinstance(data.get("sessions"), list):
        raise ValueError("Gemini returned an unexpected JSON structure.")
    return data["sessions"], prompt

def chat(messages, context=""):
    history = "\n".join(f'{m["role"]}: {m["content"]}' for m in messages[-12:])
    prompt = f"""You are StudyPilot AI, a supportive study coach. Explain clearly and accurately.
Use simple language unless asked for advanced detail. Use the user's syllabus context when relevant.
Context: {context}
Conversation:
{history}
assistant:"""
    response = _client().models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return _text(response).strip()

def improve_prompt(original_prompt, instruction):
    return original_prompt + "\nAdditional instruction: " + instruction
