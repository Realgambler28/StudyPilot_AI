# 1–2 minute demo recording script

1. Start the app with `python -m streamlit run app.py`.
2. Show the Overview dashboard and explain that its metrics are database-backed.
3. Open Subjects & Syllabus. Add a sample subject and 2–3 topics; mark one topic complete.
4. Open AI Plan Generator. Enter a future exam date and daily study-hour limit, then generate a plan. Explain that Gemini returns JSON and Python validates dates and durations before saving.
5. Open Timetable. Filter by subject, change one session to Completed, and export the CSV.
6. Open AI Study Assistant. Ask it to explain one syllabus topic or generate MCQs.
7. Finish on Progress & Analytics and show the updated completion metrics.

Recording note: Use your own Gemini API key in `.env`. Do not show the key on screen. If live Gemini is unavailable, explain that the AI calls require internet/API credentials; do not present the rule-based fallback as AI-generated.
