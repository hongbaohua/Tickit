# 專案規範

## 禁止修改（保護考生紀錄）

以下兩個檔案的關鍵部分**不得修改**，否則會導致考生過往測驗紀錄無法正常讀取：

### 1. `utils/database.py`
- 禁止新增、刪除、重新命名資料表欄位
- 禁止更改表格名稱（`users`、`quiz_sessions`、`question_results`）
- 若需要擴充欄位，必須先告知使用者並進行資料遷移

### 2. `utils/question_parser.py`
- 禁止修改 `question_id` 的產生格式（目前格式：`主題__Day_N__題號`）
- 修改此格式會導致舊紀錄的題目 ID 對不上現有題庫

---

## 可以自由修改

- `app.py`、`pages/` 下所有頁面的 UI/UX、樣式、排版
- `utils/question_parser.py` 的題目解析邏輯（但不包括 `question_id` 格式）
- `utils/analytics.py`、`utils/database.py` 的查詢邏輯（但不包括表格結構）
- `.streamlit/config.toml` 主題設定
- `questions/` 題庫內容
