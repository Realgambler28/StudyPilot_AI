# StudyPilot AI — Your Personal AI Exam Command Center

**Student:** Shivam Mhamane · **Roll No.:** 25 · **Problem Statement:** 25  
**Class:** B.Tech Computer Engineering

StudyPilot AI generates a day-wise study timetable from a student's subjects, syllabus topics, exam date, and available study hours. It uses Python for date and schedule validation, Gemini for AI planning and study assistance, Streamlit for the interactive interface, and SQLite for local persistence.

## Features
- Overview dashboard with live counts and upcoming sessions.
- Subject and topic CRUD, difficulty labels, and topic completion tracking.
- Gemini-powered structured-JSON timetable generation with Python validation.
- Explicitly labelled deterministic offline fallback (never represented as AI output).
- Interactive timetable filters, session status updates, edits, deletion, and CSV export.
- Gemini study assistant with persisted multi-turn chat history.
- Progress metrics and Plotly charts.

## Technology
Python 3.11+, Streamlit, Google GenAI SDK (`google-genai`), Gemini 2.5 Flash, SQLite, Pandas, Plotly, python-dotenv, pytest.

## Architecture
- `app.py`: Streamlit entry point and navigation.
- `components/`: dashboard, subject manager, planner, assistant, timetable, analytics UI.
- `services/`: Gemini API integration and timetable/date validation.
- `database/`: SQLite schema and parameterized CRUD functions.
- `tests/`: unit tests for database operations and schedule validation.

## Windows PowerShell setup

```powershell
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Add your Gemini API key to `.env`:
```env
GEMINI_API_KEY=your_actual_key
GEMINI_MODEL=gemini-2.5-flash
```
Get a key from Google AI Studio. Keep `.env` private; it is excluded from Git.

## Run
From the project root:
```powershell
python -m streamlit run app.py
```
Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Test
```powershell
python -m pytest -q
python -m compileall -q .
```

## Workflow
1. Add subjects and syllabus topics in **Subjects & Syllabus**.
2. Open **AI Plan Generator**, set exam date, hours, start time, and preferences.
3. Generate a Gemini timetable. The app parses JSON and validates dates, time formats, positive durations, and daily-hour totals before saving.
4. Review or update sessions in **Timetable** and export CSV.
5. Use **AI Study Assistant** for explanations, MCQs, revision quizzes, and study guidance.
6. Monitor preparation in **Progress & Analytics**.

## Screenshots
Add genuine screenshots after running the application:
- `assets/dashboard.png`
- `assets/subjects.png`
- `assets/timetable.png`
- `assets/assistant.png`
- `assets/analytics.png`

No screenshots are included in this starter package because a live Streamlit browser session was not available during packaging.

## GitHub upload
Create an empty GitHub repository named `StudyPilot_AI`, then run:
```powershell
git init
git add .
git commit -m "Build StudyPilot AI GenAI mini project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/StudyPilot_AI.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your GitHub username. Update `github_link.txt` and the report with the real repository URL.

## Limitations / verification notes
- Live Gemini calls require your own API key and internet access; they were not exercised during offline packaging.
- UI/browser interaction and screenshots must be verified on your Windows machine.
- Gemini output is strictly validated; if invalid, the app reports the failure instead of silently saving it.
- This is a local single-user application, not a hosted multi-user service.
