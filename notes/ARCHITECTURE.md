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
├── docs/                      # 網頁部署根目錄（GitHub Pages 從此資料夾部署）
│   ├── index.html             # 首頁（登入 + 選主題/單元/題數）
│   ├── quiz.html              # 測驗頁
│   ├── dashboard.html         # 考生管理頁
│   ├── css/
│   │   └── style.css          # 共用樣式
│   ├── js/
│   │   ├── config.js          # Supabase URL + anon key
│   │   ├── db.js              # Supabase CRUD 函式
│   │   └── parser.js          # Markdown 題庫解析器
│   └── questions/
│       ├── manifest.json      # 主題與單元清單（新增題庫時需同步更新）
│       └── {主題}/
│           └── *.md           # 題庫檔案
└── 待做筆記.md
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

---

## 頁面功能說明

### 首頁（index.html）— 選擇測驗範圍

1. **登入／識別使用者**：輸入使用者名稱（無需密碼，輕量識別）
2. **選擇主題**：從 `questions/manifest.json` 自動列出可用主題
3. **選擇單元**：列出該主題下所有單元，可勾選多個混搭
4. **選擇題數**：全部題目 or 隨機抽取 N 題
5. **開始測驗** → 跳轉至測驗頁

---

### 測驗頁（quiz.html）

1. **逐題顯示**：題目文字 + 四選項單選，不即時顯示對錯
2. **題組支援**：「承上題」自動連結上一題情境
3. **結果呈現**：甜甜圈圖、分數、評等、弱點摘要（單元答對率 < 75%）
4. **錯題展開**：錯題列表預設開啟，含選項與解析
5. **儲存至資料庫**：非同步寫入 `quiz_sessions` + `question_results`

---

### 考生管理頁（dashboard.html）

1. **選擇考生**：下拉選單列出所有曾測驗的使用者
2. **關鍵指標**：測驗次數、平均答對率、累計作答題數、最高答對率
3. **測驗紀錄表格**：日期、主題、完整單元名稱、分數、答對率、回顧按鈕
4. **回顧錯題**：每筆紀錄可展開查看該次錯題的題目、選項、解析
5. **答對率趨勢圖**：Chart.js 折線圖（需 ≥ 2 次）
6. **弱點診斷**：各單元三色分類（紅/黃/綠）+ 強化建議
7. **各單元答對率圖**：橫條圖，依準確率排序
8. **高頻錯題 Top 10**：歷次答錯次數統計

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
| correct_count | INTEGER | 答對題數 |
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

> **金鑰管理**：Supabase URL 與 anon key 存於 `docs/js/config.js`，已加入 `.gitignore` 中的 secrets.toml（本地開發用）。

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
