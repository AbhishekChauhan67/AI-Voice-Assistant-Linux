import sqlite3


class ChatHistory:
    def __init__(self, path: str = "history.db"):
        self.path = path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _create_table(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    reply TEXT NOT NULL,
                    response_time REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()

    def add(self, prompt: str, reply: str, response_time: float) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO chat_history (prompt, reply, response_time)
                VALUES (?, ?, ?)
                """,
                (prompt, reply, response_time),
            )
            conn.commit()

    def get_recent(self, limit: int = 10):
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT prompt, reply, response_time, timestamp
                FROM chat_history
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            )
            return cursor.fetchall()

    def close(self) -> None:
        pass

