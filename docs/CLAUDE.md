# 專案規範

## 架構說明

純前端 HTML/CSS/JS，資料庫使用 Supabase（JS SDK via REST API）。

```
Tickit/
├── notes/              # 規劃文件（ARCHITECTURE.md、UI規劃.md）
└── docs/               # 網頁部署根目錄（GitHub Pages 從此資料夾部署）
    ├── index.html          # 首頁（登入 + 選主題/單元/練習模式）
    ├── quiz.html           # 測驗頁（一般模式 + 攻克模式）
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

## 練習模式說明（index.html Step 03）

| 模式 | 說明 |
|------|------|
| 全部題目 | 所有選取單元的題目，隨機打亂順序 |
| 隨機抽取 N 題 | 從選取單元隨機抽 N 題（承上題群組保持相鄰） |
| 只練習錯題 | 從 DB 撈出歷史錯題，一次性完整測驗 |
| 攻克模式 | 從 DB 撈出歷史錯題，循環練習直到每題答對，即時揭曉對錯 |

每次開始測驗時，題目順序與選項順序皆隨機打亂（`sampleQuestions` + `shuffleOptions`）；選項末尾句號會自動刪除。

`shuffleOptions` 容錯：若答案字母無法對應任一選項（如題庫誤寫 `C/D`），該題選項不打亂、僅清除句號，不拋出例外。**題庫不應有多選答案，發現時需比對參考資料修正為單一字母。**

### 解答區段標記規範

`parser.js` 用 regex `(?:^|\n)[#\s\-]*解答與詳細解析[#\s\-]*` 尋找分隔行。

**允許格式（parser 可辨識）：**
- `## 解答與詳細解析`
- `### 解答與詳細解析`
- `解答與詳細解析`（無前綴）
- `解答與詳細解析：`（冒號結尾）

**禁止格式（parser 無法辨識，題目會全部載入失敗）：**
- `【解答與詳細解析】`（含全形括號）— Day 3 曾出現此問題，已修正

---

## sessionStorage 格式（quizSession）

```js
{
  questions: Question[],  // 已打亂題目與選項
  topic: string,
  units: string[],
  userId: number,
  userName: string,
  sessionId: string,      // Date.now().toString(36)，用於 localStorage 進度 key
  mode: "all" | "random" | "wrong-only" | "mastery"
}
```

---

## localStorage 答題進度（quiz.html）

- Key：`quiz_progress_{sessionId}`
- Value：`{ idx, answers }`
- 適用於一般模式（wrong-only / all / random），刷新或返回後自動恢復
- 攻克模式（mastery）不使用此機制，中斷後重新開始

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
cd C:\Users\Master\Projects\Tickit\docs
python -m http.server 8080
# 開啟 http://localhost:8080
```
