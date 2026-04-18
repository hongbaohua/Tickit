# 線上測驗網站 架構文件

## 專案概述

以 Streamlit 建立的線上測驗平台。題庫由 Obsidian 匯出的 Markdown 檔案管理，支援多使用者紀錄與成績分析，部署於 Streamlit Community Cloud。

---

## 技術選型

| 層級 | 工具 |
|------|------|
| 前端／後端 | Streamlit（Python） |
| 題庫格式 | Markdown（Obsidian 產出） |
| 資料庫 | Supabase（PostgreSQL，雲端持久化） |
| 部署 | Streamlit Community Cloud |
| 版本控制 | GitHub |

---

## 資料夾結構

```
quiz-app/
├── app.py                     # 主入口（首頁）
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Streamlit 設定（主題等）
├── pages/
│   ├── 1_quiz.py              # 測驗頁
│   └── 2_dashboard.py         # 考生管理頁
├── questions/                 # Obsidian 匯出的 MD 題庫
│   └── 品牌企劃師初級備考/
│       ├── Day1.md
│       ├── Day2.md
│       └── ...
├── utils/
│   ├── question_parser.py     # 解析 MD 題目
│   ├── database.py            # Supabase REST API CRUD
│   └── styles.py              # 共用 CSS 注入
└── ARCHITECTURE.md
```

---

## Markdown 題目格式規範

Obsidian 上傳的 MD 檔案實際格式如下：

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
- 題目 ID 格式：`主題__Day_N__題號`（由解析器自動產生，**不得修改**）

---

## 頁面功能說明

### 首頁（app.py）— 選擇測驗範圍

1. **登入／識別使用者**
   - 輸入名字或使用者代碼（無需密碼，輕量識別）

2. **選擇主題**
   - 從 `questions/` 子資料夾自動列出可用主題（例如：品牌企劃師初級備考）

3. **選擇單元**
   - 列出該主題下所有 MD 檔案（例如：Day1、Day2…）
   - 可勾選多個單元混搭

4. **選擇題數**
   - 全部題目
   - 隨機抽取 N 題（使用者輸入數量）

5. **開始測驗** → 跳轉至測驗頁

---

### 測驗頁（pages/1_quiz.py）

1. **逐題顯示**
   - 題目文字 + 四選項單選按鈕
   - 不即時顯示對錯，考完才公布

2. **結束與結果**
   - 顯示「答對題數 / 總題數」
   - 預設列出所有**答錯題目**及解析
   - 可展開查看所有題目解析

3. **紀錄寫入資料庫**
   - 使用者名稱、主題、單元、日期時間、總題數、答對數、各題作答記錄

---

### 考生管理頁（pages/2_dashboard.py）

1. **選擇考生**
   - 下拉選單列出所有曾測驗的使用者

2. **過往測驗紀錄**
   - 列表顯示：日期、主題、單元、分數、答對率

3. **弱點分析**
   - 統計答錯次數最多的題目
   - 依主題／單元分組顯示答對率
   - 圖表呈現（折線圖：歷次分數趨勢；長條圖：各單元答對率）

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
| units | TEXT | 選擇的單元（JSON 陣列） |
| total_questions | INTEGER | 總題數 |
| correct_count | INTEGER | 答對題數 |
| taken_at | TIMESTAMPTZ | 測驗時間 |

### question_results 表
| 欄位 | 型別 | 說明 |
|------|------|------|
| id | BIGSERIAL PK | 自動遞增 |
| session_id | BIGINT FK | 關聯 quiz_sessions |
| question_id | TEXT | 題目識別碼（主題__Day_N__題號） |
| topic | TEXT | 主題 |
| unit | TEXT | 單元 |
| is_correct | BOOLEAN | 是否答對 |
| user_answer | TEXT | 使用者選擇 |
| correct_answer | TEXT | 正確答案 |

> **金鑰管理**：Supabase URL 與 anon key 存於 `.streamlit/secrets.toml`（本地，已 gitignore）及 Streamlit Cloud Secrets（線上），不進版本控制。

---

## 本地啟動

```bash
cd C:\Users\Master\Projects\quiz-app
streamlit run app.py
```

本地網址：http://localhost:8501

---

## GitHub

Repository：https://github.com/hongbaohua/quiz-app.git

推送更新：
```bash
cd C:\Users\Master\Projects\quiz-app
git add .
git commit -m "說明"
git push
```

---

## 線上部署（Streamlit Community Cloud）

管理頁面：https://share.streamlit.io

線上網址：https://quiz-app-tjny6p3phdsrrbci2cijtx.streamlit.app

部署設定：
- Repository：`hongbaohua/quiz-app`
- Branch：`master`
- Main file：`app.py`

> 每次推送至 GitHub 後，Streamlit Cloud 會自動重新部署。

---

## 題庫更新流程

1. 在 Obsidian 編輯或新增 MD 題目檔案
2. 將檔案放入 `questions/{主題}/` 資料夾
3. 推送至 GitHub → Streamlit 自動重新部署，題庫即時生效
