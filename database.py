import sqlite3

def init_database():
    conn = sqlite3.connect("user_conversation.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    # Create user_conversation table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("user_conversation.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("user_conversation.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_conversation_history(user_id):
    conn = sqlite3.connect("user_conversation.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    history = []
    for row in cursor.execute("SELECT * FROM user_conversation WHERE user_id = ?", (user_id,)):
        history.append(row["message"])
    conn.close()
    return history

def store_conversation_history(user_id, history):
    conn = sqlite3.connect("user_conversation.db")
    cursor = conn.cursor()
    for message in history:
        cursor.execute("INSERT INTO user_conversation (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()