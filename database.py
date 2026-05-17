import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "friday_chats.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def create_session(title="New Chat"):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO sessions (title) VALUES (?)', (title,))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_sessions():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, title, created_at FROM sessions ORDER BY created_at DESC')
    sessions = c.fetchall()
    conn.close()
    return [{"id": s["id"], "title": s["title"], "created_at": s["created_at"]} for s in sessions]

def get_session_messages(session_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY created_at ASC', (session_id,))
    messages = c.fetchall()
    conn.close()
    return [{"role": m["role"], "content": m["content"], "created_at": m["created_at"]} for m in messages]

def clear_all_history():
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    c.execute('DELETE FROM sessions')
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', (session_id, role, content))
    
    # If this is the first user message, update the session title
    if role == "user":
        c.execute('SELECT COUNT(*) FROM messages WHERE session_id = ? AND role = "user"', (session_id,))
        count = c.fetchone()[0]
        if count == 1:
            title = content[:30] + ("..." if len(content) > 30 else "")
            c.execute('UPDATE sessions SET title = ? WHERE id = ?', (title, session_id))
            
    conn.commit()
    conn.close()
