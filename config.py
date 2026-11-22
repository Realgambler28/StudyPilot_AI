import os
from dotenv import load_dotenv

load_dotenv()
APP_NAME = "StudyPilot AI"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
DB_PATH = os.getenv("STUDYPILOT_DB", "studypilot.db")
