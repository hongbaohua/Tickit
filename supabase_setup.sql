-- ============================================================
-- 線上測驗平台 Supabase 初始化腳本
-- 在 Supabase Dashboard → SQL Editor 執行此腳本
-- ============================================================

-- ── 建立資料表 ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS users (
    id         BIGSERIAL PRIMARY KEY,
    name       TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS quiz_sessions (
    id               BIGSERIAL PRIMARY KEY,
    user_id          BIGINT REFERENCES users(id),
    topic            TEXT,
    units            TEXT,
    total_questions  INTEGER,
    correct_count    INTEGER,
    taken_at         TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS question_results (
    id              BIGSERIAL PRIMARY KEY,
    session_id      BIGINT REFERENCES quiz_sessions(id),
    question_id     TEXT,
    topic           TEXT,
    unit            TEXT,
    is_correct      BOOLEAN,
    user_answer     TEXT,
    correct_answer  TEXT
);

-- ── 啟用 RLS ────────────────────────────────────────────────

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_results ENABLE ROW LEVEL SECURITY;

-- ── 允許 anon 角色完整存取（先刪除再建立，避免重複執行錯誤）──

DROP POLICY IF EXISTS "anon_all" ON users;
DROP POLICY IF EXISTS "anon_all" ON quiz_sessions;
DROP POLICY IF EXISTS "anon_all" ON question_results;

CREATE POLICY "anon_all" ON users
    FOR ALL TO anon USING (true) WITH CHECK (true);

CREATE POLICY "anon_all" ON quiz_sessions
    FOR ALL TO anon USING (true) WITH CHECK (true);

CREATE POLICY "anon_all" ON question_results
    FOR ALL TO anon USING (true) WITH CHECK (true);
