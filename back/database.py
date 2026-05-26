import sqlite3

# Create/connect database
conn = sqlite3.connect(
    "study.db",
    check_same_thread=False
)

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam TEXT,
    weak TEXT,
    strong TEXT,
    days INTEGER,
    hours INTEGER,
    plan TEXT
)
""")

conn.commit()