PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
    difficulty TEXT NOT NULL DEFAULT 'Medium',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name TEXT NOT NULL COLLATE NOCASE,
    completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0,1)),
    UNIQUE(subject_id, name)
);
CREATE TABLE IF NOT EXISTS plan_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_date TEXT NOT NULL,
    daily_hours REAL NOT NULL,
    preferences TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    session_type TEXT NOT NULL,
    start_time TEXT NOT NULL,
    duration REAL NOT NULL CHECK(duration > 0),
    objective TEXT DEFAULT '',
    revision_activity TEXT DEFAULT '',
    practice_activity TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'Not Started'
        CHECK(status IN ('Not Started','In Progress','Completed'))
);
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL CHECK(role IN ('user','model')),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
