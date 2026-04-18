// Supabase REST API wrapper
const _headers = () => ({
  "apikey": SUPABASE_KEY,
  "Authorization": `Bearer ${SUPABASE_KEY}`,
  "Content-Type": "application/json",
  "Prefer": "return=representation",
});

const _url = (table) => `${SUPABASE_URL}/rest/v1/${table}`;

async function _check(res, context = "") {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(`Supabase 錯誤 [${context}] (${res.status}): ${err.message || res.statusText}`);
  }
  return res;
}

async function getOrCreateUser(name) {
  const res = await fetch(`${_url("users")}?name=eq.${encodeURIComponent(name)}&select=id`, {
    headers: _headers(),
  });
  await _check(res, "查詢使用者");
  const data = await res.json();
  if (data.length > 0) return data[0].id;

  const res2 = await fetch(_url("users"), {
    method: "POST",
    headers: _headers(),
    body: JSON.stringify({ name }),
  });
  await _check(res2, "建立使用者");
  const created = await res2.json();
  return created[0].id;
}

async function saveSession(userId, topic, units, total, correct, answers) {
  const res = await fetch(_url("quiz_sessions"), {
    method: "POST",
    headers: _headers(),
    body: JSON.stringify({
      user_id: userId,
      topic,
      units: JSON.stringify(units),
      total_questions: total,
      correct_count: correct,
      taken_at: new Date().toISOString(),
    }),
  });
  await _check(res, "儲存測驗紀錄");
  const session = await res.json();
  const sessionId = session[0].id;

  const records = answers.map((a) => ({
    session_id: sessionId,
    question_id: a.question_id,
    topic: a.topic,
    unit: a.unit,
    is_correct: a.is_correct,
    user_answer: a.user_answer,
    correct_answer: a.correct_answer,
  }));

  const res2 = await fetch(_url("question_results"), {
    method: "POST",
    headers: _headers(),
    body: JSON.stringify(records),
  });
  await _check(res2, "儲存題目結果");
  return sessionId;
}

async function getUserSessions(userId) {
  const res = await fetch(`${_url("quiz_sessions")}?user_id=eq.${userId}&order=taken_at.desc`, {
    headers: _headers(),
  });
  await _check(res, "讀取測驗紀錄");
  const rows = await res.json();
  return rows.map((r) => ({
    ...r,
    units: typeof r.units === "string" ? JSON.parse(r.units) : r.units,
  }));
}

async function getUserQuestionResults(userId) {
  const sessRes = await fetch(`${_url("quiz_sessions")}?user_id=eq.${userId}&select=id`, {
    headers: _headers(),
  });
  await _check(sessRes, "讀取 session IDs");
  const sessions = await sessRes.json();
  if (sessions.length === 0) return [];

  const ids = sessions.map((s) => s.id).join(",");
  const res = await fetch(`${_url("question_results")}?session_id=in.(${ids})`, {
    headers: _headers(),
  });
  await _check(res, "讀取題目結果");
  return res.json();
}

async function getAllUsers() {
  const res = await fetch(`${_url("users")}?select=id,name&order=name`, {
    headers: _headers(),
  });
  await _check(res, "讀取所有使用者");
  return res.json();
}
