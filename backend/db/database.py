import sqlite3

conn = sqlite3.connect("functions.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS functions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            file_path TEXT NOT NULL,
            timeout INTEGER DEFAULT 5
        );
    """)
    conn.commit()
