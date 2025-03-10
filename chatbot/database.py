import sqlite3
from config import DB_PATH # Import database path from config.py

def create_table():
    """Creates the chat history table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    """Fetches chat history for a given session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chat_history WHERE session_id=? ORDER BY timestamp", 
                   (session_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def save_chat(session_id, user_message, bot_response):
    """Stores a chat message in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (session_id, user_message, bot_response) VALUES (?, ?, ?)", 
                   (session_id, user_message, bot_response))
    conn.commit()
    conn.close()

# Initialize the database
create_table()
