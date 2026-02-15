import sqlite3
from typing import List, Tuple


class MemoryStore:
    def __init__(self, db_path: str = "chat.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                user_id TEXT,
                role TEXT,
                message TEXT
            )
        """)
        self.conn.commit()

    def save_message(self, user_id: str, role: str, message: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, role, message),
        )
        self.conn.commit()

    def get_conversation(self, user_id: str, limit: int = 6) -> List[Tuple[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT role, message
            FROM conversations
            WHERE user_id = ?
            ORDER BY rowid DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cursor.fetchall()
        return rows[::-1]
