import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DB_DIR / "quiz_results.db"


def _get_conn():
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            units TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            taken_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS question_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            topic TEXT NOT NULL,
            unit TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            user_answer TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES quiz_sessions(id)
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_user(name: str) -> int:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        conn.close()
        return row["id"]

    cur.execute(
        "INSERT INTO users (name, created_at) VALUES (?, ?)",
        (name, datetime.now().isoformat())
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def save_session(
    user_id: int,
    topic: str,
    units: list[str],
    total: int,
    correct: int,
    answers: list[dict]
) -> int:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO quiz_sessions (user_id, topic, units, total_questions, correct_count, taken_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, topic, json.dumps(units, ensure_ascii=False), total, correct, datetime.now().isoformat())
    )
    session_id = cur.lastrowid

    for a in answers:
        cur.execute(
            """
            INSERT INTO question_results
                (session_id, question_id, topic, unit, is_correct, user_answer, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                a["question_id"],
                a["topic"],
                a["unit"],
                1 if a["is_correct"] else 0,
                a["user_answer"],
                a["correct_answer"],
            )
        )

    conn.commit()
    conn.close()
    return session_id


def get_user_sessions(user_id: int) -> list[dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM quiz_sessions WHERE user_id = ? ORDER BY taken_at DESC",
        (user_id,)
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    for r in rows:
        r["units"] = json.loads(r["units"])
    return rows


def get_user_question_results(user_id: int) -> list[dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT qr.*
        FROM question_results qr
        JOIN quiz_sessions qs ON qr.session_id = qs.id
        WHERE qs.user_id = ?
        ORDER BY qs.taken_at DESC
        """,
        (user_id,)
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_all_users() -> list[dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY name")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


init_db()
