import json
from datetime import datetime

import requests
import streamlit as st


def _headers() -> dict:
    key = st.secrets["supabase"]["key"]
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _url(table: str) -> str:
    base = st.secrets["supabase"]["url"]
    return f"{base}/rest/v1/{table}"


def _check(r: requests.Response, context: str = "") -> None:
    """Supabase API 回傳錯誤時拋出易讀的例外。"""
    if not r.ok:
        try:
            err = r.json()
            msg = err.get("message", r.text)
            code = err.get("code", r.status_code)
        except Exception:
            msg = r.text
            code = r.status_code
        label = f" [{context}]" if context else ""
        raise RuntimeError(
            f"Supabase 錯誤{label} (HTTP {r.status_code}, code={code}): {msg}"
        )


def get_or_create_user(name: str) -> int:
    r = requests.get(
        _url("users"),
        headers=_headers(),
        params={"name": f"eq.{name}", "select": "id"},
    )
    _check(r, "查詢使用者")
    data = r.json()
    if data:
        return data[0]["id"]
    r = requests.post(
        _url("users"),
        headers=_headers(),
        json={"name": name},
    )
    _check(r, "建立使用者")
    return r.json()[0]["id"]


def save_session(
    user_id: int,
    topic: str,
    units: list[str],
    total: int,
    correct: int,
    answers: list[dict],
) -> int:
    r = requests.post(
        _url("quiz_sessions"),
        headers=_headers(),
        json={
            "user_id": user_id,
            "topic": topic,
            "units": json.dumps(units, ensure_ascii=False),
            "total_questions": total,
            "correct_count": correct,
            "taken_at": datetime.now().isoformat(),
        },
    )
    _check(r, "儲存測驗紀錄")
    session_id = r.json()[0]["id"]

    records = [
        {
            "session_id": session_id,
            "question_id": a["question_id"],
            "topic": a["topic"],
            "unit": a["unit"],
            "is_correct": bool(a["is_correct"]),
            "user_answer": a["user_answer"],
            "correct_answer": a["correct_answer"],
        }
        for a in answers
    ]
    r2 = requests.post(_url("question_results"), headers=_headers(), json=records)
    _check(r2, "儲存題目結果")
    return session_id


def get_user_sessions(user_id: int) -> list[dict]:
    r = requests.get(
        _url("quiz_sessions"),
        headers=_headers(),
        params={"user_id": f"eq.{user_id}", "order": "taken_at.desc"},
    )
    _check(r, "讀取測驗紀錄")
    rows = r.json()
    for row in rows:
        if isinstance(row.get("units"), str):
            row["units"] = json.loads(row["units"])
    return rows


def get_user_question_results(user_id: int) -> list[dict]:
    r = requests.get(
        _url("quiz_sessions"),
        headers=_headers(),
        params={"user_id": f"eq.{user_id}", "select": "id"},
    )
    _check(r, "讀取 session IDs")
    session_ids = [s["id"] for s in r.json()]
    if not session_ids:
        return []
    ids_str = f"in.({','.join(str(i) for i in session_ids)})"
    r = requests.get(
        _url("question_results"),
        headers=_headers(),
        params={"session_id": ids_str},
    )
    _check(r, "讀取題目結果")
    return r.json()


def get_all_users() -> list[dict]:
    r = requests.get(
        _url("users"),
        headers=_headers(),
        params={"select": "id,name", "order": "name"},
    )
    _check(r, "讀取所有使用者")
    return r.json()
