import sqlite3
from typing import List, Tuple


def get_user_conversation_history(user_id: int) -> List[str]:
    conn = sqlite3.connect("user_conversation.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    history = []
    for row in cursor.execute("SELECT * FROM user_conversation WHERE user_id = ?", (user_id,)):
        history.append(row["message"])
    conn.close()
    return history


def get_conversation_history_from_storage(user_id):
    # Fetch conversation history for the specific user from a database
    conversation_history = get_user_conversation_history(user_id)
    return conversation_history
