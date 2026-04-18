# 專案規範

## 架構說明

純前端 HTML/CSS/JS，資料庫使用 Supabase（JS SDK via REST API）。

```
quiz-app/
├── notes/              # 規劃文件（ARCHITECTURE.md、UI規劃.md）
└── web/                # 網頁部署根目錄（GitHub Pages 從此資料夾部署）
    ├── index.html          # 首頁（登入 + 選主題/單元/題數）
    ├── quiz.html           # 測驗頁
    ├── dashboard.html      # 考生管理頁
    ├── css/style.css       # 共用樣式
    ├── js/
    │   ├── config.js       # Supabase URL + anon key
    │   ├── db.js           # Supabase CRUD 函式
    │   └── parser.js       # Markdown 題庫解析器
    └── questions/
        ├── manifest.json   # 主題與單元清單（題庫新增時需同步更新）
        └── {主題}/
            └── *.md        # 題庫檔案
```

---

## 禁止修改（保護考生紀錄）

### 1. `js/parser.js` — `_makeId()` 函式
- 禁止修改 `question_id` 的產生格式（格式：`主題__Day_N__題號`）
- 修改此格式會導致舊紀錄的題目 ID 對不上現有題庫

### 2. Supabase 資料表結構
- 禁止新增、刪除、重新命名 `users`、`quiz_sessions`、`question_results` 三張表的欄位
- 若需擴充欄位，必須先告知使用者並進行資料遷移

---

## 題庫新增流程

1. 在 Obsidian 建立新的 `.md` 題庫檔案（格式：題目區 + `解答與詳細解析` + 解析區）
2. 將檔案放入 `questions/{主題}/` 資料夾
3. **更新 `questions/manifest.json`**，新增對應的 `{ "unit": "Day N", "file": "完整檔名.md" }`
4. 推送至 GitHub → GitHub Pages 自動更新

---

## 可以自由修改

- `index.html`、`quiz.html`、`dashboard.html` 的 UI/UX、樣式、排版
- `css/style.css` 全部內容
- `js/db.js` 的查詢邏輯（但不包括表格結構）
- `js/parser.js` 的解析邏輯（但不包括 `_makeId()` 格式）

---

## 本地測試

瀏覽器直接開啟 `index.html` 無法 fetch 本地檔案（CORS 限制）。
需啟動本地伺服器：

```bash
cd C:\Users\Master\Projects\quiz-app\web
python -m http.server 8080
# 開啟 http://localhost:8080
```
