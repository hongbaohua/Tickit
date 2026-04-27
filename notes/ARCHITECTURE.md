# Tickit 架構文件

## 專案概述

Tickit 是純前端 HTML/CSS/JS 的線上測驗練習平台。題庫由 Obsidian 管理的 Markdown 檔案組成，資料持久化至 Supabase（雲端 PostgreSQL），部署於 GitHub Pages（靜態網頁）。

---

## 技術選型

| 層級 | 工具 |
|------|------|
| 前端 | HTML5 / CSS3 / Vanilla JS |
| 題庫格式 | Markdown（Obsidian 產出） |
| 資料庫 | Supabase（PostgreSQL，REST API） |
| 圖表庫 | Chart.js 4.4.0 |
| 部署 | GitHub Pages（靜態，從 `docs/` 資料夾部署） |
| 版本控制 | GitHub |

---

## 資料夾結構

```
Tickit/
├── notes/
│   ├── ARCHITECTURE.md        # 本文件
│   └── UI規劃.md              # UI/UX 設計規劃
└── docs/                      # 網頁部署根目錄（GitHub Pages 從此資料夾部署）
    ├── index.html             # 首頁（登入 + 選主題/單元/練習模式）
    ├── quiz.html              # 測驗頁（一般模式 + 攻克模式）
    ├── dashboard.html         # 考生管理頁
    ├── css/
    │   └── style.css          # 共用樣式
    ├── js/
    │   ├── config.js          # Supabase URL + anon key
    │   ├── db.js              # Supabase CRUD 函式
    │   └── parser.js          # Markdown 題庫解析器
    └── questions/
        ├── manifest.json      # 主題與單元清單（新增題庫時需同步更新）
        └── {主題}/
            └── *.md           # 題庫檔案
```

---

## Markdown 題目格式規範

```markdown
1. 題目文字

   (A) 選項一

   (B) 選項二

   (C) 選項三

   (D) 選項四

2. 下一題...


解答與詳細解析

1. (B) 解析說明文字...

2. (A) 解析說明文字...
```

- 題目區與解析區以「解答與詳細解析」分隔
- 題號格式：`{n}.`
- 選項格式：`(A)` `(B)` `(C)` `(D)`
- 解析格式：`{n}. ({字母}) 解析文字`
- 題目 ID 格式：`主題__Day_N__題號`（由 `parser.js` 的 `_makeId()` 自動產生，**不得修改**）
- 選項末尾句號（`。`）在出題時自動刪除

---

## 頁面功能說明

### 首頁（index.html）— 選擇測驗範圍

1. **登入／識別使用者**：輸入使用者名稱（無需密碼，輕量識別）
2. **選擇主題**：從 `questions/manifest.json` 自動列出可用主題
3. **選擇單元**：列出該主題下所有單元，可勾選多個混搭，旁標題數
4. **選擇練習模式**（Step 03）：

   | 模式 | 說明 |
   |------|------|
   | 全部題目 | 所有題目，隨機打亂順序 |
   | 隨機抽取 N 題 | 隨機抽 N 題（承上題群組保持相鄰） |
   | 只練習錯題 | 載入歷史錯題，一次性測驗 |
   | 攻克模式 | 載入歷史錯題，循環練習直到全部答對 |

5. 開始前所有題目與選項皆隨機打亂（`sampleQuestions` + `shuffleOptions`）
6. **開始測驗** → 跳轉至測驗頁

---

### 測驗頁（quiz.html）

#### 一般模式（all / random / wrong-only）

1. **逐題顯示**：題目文字 + 四選項單選，不即時顯示對錯
2. **題組支援**：「承上題」自動連結上一題情境
3. **中斷恢復**：每次翻頁 / 答題後將 `{ idx, answers }` 存入 `localStorage`（key：`quiz_progress_{sessionId}`），刷新或返回後自動恢復並顯示 Toast
4. **結果呈現**：甜甜圈圖、分數、評等、弱點摘要（單元答對率 < 75%）
5. **錯題展開**：錯題列表預設開啟，含選項與解析
6. **儲存至資料庫**：非同步寫入 `quiz_sessions` + `question_results`

#### 攻克模式（mastery）

1. **題目點陣**：最多 30 題，每格顏色代表狀態（灰=未到、靛=目前、橙=曾錯、綠=攻克）
2. **即時揭曉**：選答案後按「確認答案」，選項立即變色並顯示解析
3. **動態佇列**：答錯則插回佇列（4 題後再出現）；答對則攻克
4. **再練提示**：曾答錯的題目頂部顯示「↩ 再練」徽章
5. **完成畫面**：攻克題數、重練次數、首答答對率，並儲存首次作答記錄至 DB

---

### 考生管理頁（dashboard.html）

1. **選擇考生**：可直接輸入或從下拉清單選取（`<input list="datalist">`）
2. **測驗紀錄**：顯示所有主題的歷史紀錄（日期、主題、單元、分數、答對率、回顧錯題）
3. **主題篩選 Tabs**：其他分析區塊依主題分開，點 Tab 切換
4. **關鍵指標**：測驗次數、平均答對率、累計作答題數、最高答對率（依選取主題過濾）
5. **答對率趨勢圖**：Chart.js 折線圖（需 ≥ 2 次）
6. **弱點診斷**：各單元三色分類（紅/黃/綠）+ 強化建議
7. **各單元答對率圖**：橫條圖，依準確率排序
8. **高頻錯題 Top 10**：歷次答錯次數統計

---

## JS 模組說明

### parser.js

| 函式 | 說明 |
|------|------|
| `parseMarkdown(text, topic, filename)` | 解析 MD 檔，回傳 Question 陣列 |
| `loadQuestions(topic, units)` | 依主題 + 單元 fetch 並解析所有題目 |
| `sampleQuestions(questions, n)` | Fisher-Yates 打亂題目順序，依承上題群組保持相鄰，取前 n 題 |
| `shuffleOptions(questions)` | 打亂每題選項順序，同步更新 answer 字母，刪末尾句號 |

> `_makeId()` 格式固定為 `主題__Day_N__題號`，**禁止修改**。

### db.js

| 函式 | 說明 |
|------|------|
| `getOrCreateUser(name)` | 查詢或建立使用者，回傳 userId |
| `saveSession(userId, topic, units, total, correct, answers)` | 儲存測驗紀錄與每題結果 |
| `getUserSessions(userId)` | 取得用戶所有測驗紀錄 |
| `getUserQuestionResults(userId)` | 取得用戶所有題目作答結果 |
| `getAllUsers()` | 取得所有使用者 |
| `getWrongQuestionIds(userId, topic, units)` | 回傳指定主題 + 單元中歷史答錯的 question_id Set |

---

## sessionStorage 格式

```js
// quizSession（index.html 寫入，quiz.html 讀取）
{
  questions: Question[],   // 已打亂題目與選項
  topic: string,
  units: string[],
  userId: number,
  userName: string,
  sessionId: string,       // Date.now().toString(36)
  mode: "all" | "random" | "wrong-only" | "mastery"
}

// quizUser（登入後保存，跨頁使用）
{ id: number, name: string }
```

---

## localStorage 格式

```js
// 答題進度（一般模式）
key: "quiz_progress_{sessionId}"
value: { idx: number, answers: { [idx]: string } }
// 測驗完成後自動刪除
```

---

## 資料庫結構（Supabase / PostgreSQL）

Supabase 專案：https://supabase.com/dashboard/project/svuqajwngmqseqobrkgk

### users 表
| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增 |
| name | TEXT UNIQUE | 使用者名稱 |
| created_at | TIMESTAMPTZ | 首次登入時間 |

### quiz_sessions 表
| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增 |
| user_id | BIGINT FK | 關聯 users |
| topic | TEXT | 主題名稱 |
| units | TEXT | 選擇的單元（JSON 陣列，內容為單元代號如 "Day 1"） |
| total_questions | INTEGER | 總題數 |
| correct_count | INTEGER | 答對題數（攻克模式為首答答對數） |
| taken_at | TIMESTAMPTZ | 測驗時間 |

### question_results 表
| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增 |
| session_id | BIGINT FK | 關聯 quiz_sessions |
| question_id | TEXT | 題目識別碼（格式：`主題__Day_N__題號`） |
| topic | TEXT | 主題 |
| unit | TEXT | 單元代號 |
| is_correct | BOOLEAN | 是否答對 |
| user_answer | TEXT | 使用者選擇（A/B/C/D） |
| correct_answer | TEXT | 正確答案（A/B/C/D） |

> **金鑰管理**：Supabase URL 與 anon key 存於 `docs/js/config.js`，已加入 `.gitignore`。

---

## 禁止修改（保護考生紀錄）

### 1. `js/parser.js` — `_makeId()` 函式
- 禁止修改 `question_id` 的產生格式（格式：`主題__Day_N__題號`）
- 修改後舊紀錄的 question_id 將無法對應現有題庫

### 2. Supabase 資料表結構
- 禁止新增、刪除、重新命名 `users`、`quiz_sessions`、`question_results` 三張表的欄位
- 若需擴充欄位，必須先告知使用者並進行資料遷移

---

## 本地測試

瀏覽器直接開啟 `index.html` 無法 fetch 本地檔案（CORS 限制），需啟動本地伺服器：

```bash
cd C:\Users\Master\Projects\Tickit\docs
python -m http.server 8080
# 開啟 http://localhost:8080
```

---

## GitHub

Repository：https://github.com/hongbaohua/Tickit.git

推送更新：
```bash
cd C:\Users\Master\Projects\Tickit
git add .
git commit -m "說明"
git push
```

---

## 線上部署（GitHub Pages）

管理頁面：https://github.com/hongbaohua/Tickit/settings/pages

部署設定：
- Repository：`hongbaohua/Tickit`
- Branch：`master`
- 來源資料夾：`/docs`

> 每次推送至 GitHub 後，GitHub Pages 會自動重新部署。

---

## 題庫更新流程

1. 在 Obsidian 建立或編輯 `.md` 題庫檔案
2. 將檔案放入 `docs/questions/{主題}/` 資料夾
3. **更新 `docs/questions/manifest.json`**，新增對應的 `{ "unit": "Day N", "file": "完整檔名.md" }`
4. 推送至 GitHub → GitHub Pages 自動重新部署，題庫即時生效
