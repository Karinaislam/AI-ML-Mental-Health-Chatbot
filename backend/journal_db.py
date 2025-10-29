import sqlite3

def init_db():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            sentiment TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_entry(message, sentiment, response):
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("INSERT INTO journal (message, sentiment, response) VALUES (?, ?, ?)",
              (message, sentiment, response))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM journal ORDER BY id DESC")
    entries = c.fetchall()
    conn.close()
    return entries
