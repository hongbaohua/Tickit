# Tickit 資料庫備份

**備份日期**：2026-06-11
**備份來源**：Supabase 免費版（PostgreSQL）
**專案 ID**：`svuqajwngmqseqobrkgk`

---

## 資料夾結構

```
database-backup/
├── README.md              # 本文件（schema 說明 + 還原指南）
└── data/
    ├── users.json          # 3 筆（使用者）
    ├── quiz_sessions.json  # 43 筆（測驗紀錄）
    └── question_results.json # 1792 筆（每題作答結果）
```

---

## 資料表結構

### `users` — 使用者

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增主鍵 |
| name | TEXT UNIQUE NOT NULL | 使用者名稱（登入識別用，無密碼） |
| created_at | TIMESTAMPTZ DEFAULT now() | 首次登入時間 |

**約束**：`name` 欄位唯一，`getOrCreateUser()` 查無時自動建立。

---

### `quiz_sessions` — 測驗紀錄

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增主鍵 |
| user_id | BIGINT FK → users.id | 關聯使用者 |
| topic | TEXT NOT NULL | 主題名稱（例：`品牌企劃師初級備考`） |
| units | TEXT NOT NULL | 選擇的單元，JSON 陣列字串（例：`["Day 1","Day 2"]`） |
| total_questions | INTEGER NOT NULL | 本次測驗總題數 |
| correct_count | INTEGER NOT NULL | 答對題數（攻克模式為首答答對數） |
| taken_at | TIMESTAMPTZ DEFAULT now() | 測驗時間 |

**注意**：`units` 儲存為 TEXT，讀取時需 `JSON.parse()`。

---

### `question_results` — 每題作答結果

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增主鍵 |
| session_id | BIGINT FK → quiz_sessions.id | 關聯測驗紀錄 |
| question_id | TEXT NOT NULL | 題目識別碼（格式：`主題__Day_N__題號`，由 `parser.js` 的 `_makeId()` 產生，**禁止修改格式**） |
| topic | TEXT NOT NULL | 主題名稱 |
| unit | TEXT NOT NULL | 單元代號（例：`Day 1`） |
| is_correct | BOOLEAN NOT NULL | 是否答對 |
| user_answer | TEXT | 使用者選擇（A/B/C/D），未作答為 null |
| correct_answer | TEXT NOT NULL | 正確答案（A/B/C/D） |

---

## 資料統計（2026-06-11）

| 表 | 筆數 | 說明 |
|----|------|------|
| users | 3 | test、大美女、admin |
| quiz_sessions | 43 | 所有歷史測驗紀錄 |
| question_results | 1792 | 所有歷史作答記錄 |

---

## 未來如何使用這份備份

### 情境一：Supabase 被暫停，需要手動喚醒

1. 登入 [Supabase Dashboard](https://supabase.com/dashboard/project/svuqajwngmqseqobrkgk)
2. 點擊「Restore project」（免費版可自行恢復）
3. 恢復後資料**依然存在**，不需要重新匯入
4. 若超過 **90 天**未恢復，專案會被**永久刪除**，此時才需要使用本備份

### 情境二：Supabase 專案被刪除，需要重建

**Step 1：在 Supabase 建立新專案**
1. 前往 [supabase.com](https://supabase.com) 建立新專案
2. 記錄新的 Project URL 與 anon key

**Step 2：建立資料表（在 SQL Editor 執行）**

```sql
-- users 表
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- quiz_sessions 表
CREATE TABLE quiz_sessions (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id),
  topic TEXT NOT NULL,
  units TEXT NOT NULL,
  total_questions INTEGER NOT NULL,
  correct_count INTEGER NOT NULL,
  taken_at TIMESTAMPTZ DEFAULT now()
);

-- question_results 表
CREATE TABLE question_results (
  id BIGSERIAL PRIMARY KEY,
  session_id BIGINT REFERENCES quiz_sessions(id),
  question_id TEXT NOT NULL,
  topic TEXT NOT NULL,
  unit TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL,
  user_answer TEXT,
  correct_answer TEXT NOT NULL
);
```

**Step 3：設定 RLS 權限（在 SQL Editor 執行）**

```sql
-- 允許 anon key 讀寫（前端 JS 使用 anon key 直接存取）
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow all" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON quiz_sessions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON question_results FOR ALL USING (true) WITH CHECK (true);
```

**Step 4：匯入備份資料**

使用 Supabase Dashboard → Table Editor → Import，或執行以下 Python 腳本：

```python
# restore.py
# 執行前先安裝：pip install requests
import json, requests

NEW_URL = "https://YOUR_NEW_PROJECT.supabase.co"
NEW_KEY = "YOUR_NEW_ANON_KEY"
headers = {"apikey": NEW_KEY, "Authorization": f"Bearer {NEW_KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}

# 1. 匯入 users（注意：id 需手動指定以保持 FK 關聯）
with open("data/users.json", encoding="utf-8") as f:
    users = json.load(f)
r = requests.post(f"{NEW_URL}/rest/v1/users", json=users, headers=headers)
print("users:", r.status_code)

# 2. 匯入 quiz_sessions
with open("data/quiz_sessions.json", encoding="utf-8") as f:
    sessions = json.load(f)
r = requests.post(f"{NEW_URL}/rest/v1/quiz_sessions", json=sessions, headers=headers)
print("quiz_sessions:", r.status_code)

# 3. 匯入 question_results
with open("data/question_results.json", encoding="utf-8") as f:
    results = json.load(f)
# 分批匯入（每批 500 筆，避免超過 Supabase 請求大小上限）
batch = 500
for i in range(0, len(results), batch):
    chunk = results[i:i+batch]
    r = requests.post(f"{NEW_URL}/rest/v1/question_results", json=chunk, headers=headers)
    print(f"question_results batch {i//batch + 1}: {r.status_code}")

# 4. 重設序列（讓 BIGSERIAL 從正確的值繼續，而非從 1 開始）
# 在 Supabase SQL Editor 執行：
# SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
# SELECT setval('quiz_sessions_id_seq', (SELECT MAX(id) FROM quiz_sessions));
# SELECT setval('question_results_id_seq', (SELECT MAX(id) FROM question_results));
```

**Step 5：更新 `docs/js/config.js`**

```js
const SUPABASE_URL = "https://YOUR_NEW_PROJECT.supabase.co";
const SUPABASE_KEY = "YOUR_NEW_ANON_KEY";
const ADMIN_USERS = ["admin"];
```

---

## 注意事項

- 此備份為**靜態快照**，不會自動更新。如未來繼續使用 Tickit，建議定期重新備份。
- `question_id` 格式（`主題__Day_N__題號`）與題庫 `.md` 檔緊密綁定，還原後**禁止修改 `parser.js` 的 `_makeId()` 函式**，否則歷史紀錄將與題庫失去對應。
- 匯入時需按順序：`users` → `quiz_sessions` → `question_results`（外鍵依賴）。
- 匯入後必須執行 Step 4 末段的 `setval` 指令，否則新增紀錄時 id 會從 1 開始產生衝突。
