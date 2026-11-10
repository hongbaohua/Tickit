// 代碼題庫（機場 / 航空公司 / 特殊需求）— 載入、出題、判分
// question_id 格式：{topic}__c2z__{id}（代碼→中文）／{topic}__z2c__{id}（中文→代碼）
// 已寫入 DB 的紀錄依賴此格式，請勿更改。

const CODES_TOPIC = "機場航空代碼";

// 簡體 / 異體字 → 本題庫用字（只需涵蓋題庫裡出現的字）
const _ZH_VARIANTS = {
  "臺": "台", "东": "東", "门": "門", "岛": "島", "庆": "慶", "连": "連", "宁": "寧",
  "乌": "烏", "鲁": "魯", "齐": "齊", "阳": "陽", "兰": "蘭", "汉": "漢", "广": "廣",
  "头": "頭", "丽": "麗", "长": "長", "滨": "濱", "尔": "爾", "萨": "薩", "贵": "貴",
  "郑": "鄭", "莱": "萊", "维": "維", "纳": "納", "罗": "羅", "伦": "倫", "华": "華",
  "达": "達", "马": "馬", "爱": "愛", "岘": "峴", "买": "買", "满": "滿", "迈": "邁",
  "馆": "館", "冈": "岡", "关": "關", "冲": "沖", "绳": "繩", "济": "濟", "湾": "灣",
  "区": "區", "国": "國", "厦": "廈", "荣": "榮", "桥": "橋", "烟": "煙", "温": "溫",
  "亚": "亞", "张": "張", "银": "銀", "黄": "黃", "婴": "嬰", "儿": "兒", "鲜": "鮮",
  "搀": "攙", "阶": "階", "楼": "樓", "机": "機", "园": "園", "航": "航", "陆": "陸",
  "沈": "瀋", "內": "內", "内": "內", "里": "里", "裡": "里", "萬": "萬", "幕": "慕",
  "龍": "隆", "苏": "蘇", "联": "聯", "义": "義", "兰": "蘭", "兹": "茲", "处": "處",
};

// 額外可接受的寫法（不改動原始題庫檔，只在判分時加入）
const _EXTRA_ACCEPT = {
  "003": ["巴塞羅那"],
  "009": ["布里斯托爾"],
  "019": ["佛羅倫薩", "翡冷翠"],
  "025": ["布吉"],
  "027": ["文萊"],
  "074": ["西安咸陽"],
  "121": ["瀋陽"],
};

function normalizeZh(s) {
  return [...String(s || "")]
    .map((ch) => _ZH_VARIANTS[ch] || ch)
    .join("")
    .replace(/[\s　（）()【】\[\]「」『』、，,。.．·・\-－—_/／:：;；!！?？'"]/g, "");
}

function normalizeCode(s) {
  return String(s || "")
    .toUpperCase()
    .replace(/[０-９Ａ-Ｚ]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\s+/g, "");
}

async function loadCodeBank() {
  const res = await fetch(`questions/${encodeURIComponent(CODES_TOPIC)}/${encodeURIComponent("題庫.json")}`);
  if (!res.ok) throw new Error("無法載入代碼題庫");
  const items = await res.json();
  return items.map((it) => ({
    ...it,
    accept: [...it.accept, ...(_EXTRA_ACCEPT[it.id] || [])],
  }));
}

// 代碼→中文 可接受的代碼寫法（BER/T 也接受 BER）
function _codeVariants(code) {
  const c = normalizeCode(code);
  const out = new Set([c]);
  if (c.includes("/")) {
    out.add(c.split("/")[0]);
    out.add(c.replace("/", ""));
  }
  return out;
}

// 由題庫建立題目。dir: "c2z" | "z2c"
// 中文→代碼：同一個中文名稱（如「札幌」有 3 個代碼）合併為一題，寫出任一個即可
function buildCodeQuestions(bank, categories, dir) {
  const items = bank.filter((it) => categories.includes(it.category));
  if (dir === "c2z") {
    return items.map((it) => ({
      id: `${CODES_TOPIC}__c2z__${it.id}`,
      dir: "c2z",
      unit: it.category,
      prompt: it.code,
      items: [it],
    }));
  }
  const groups = new Map();
  for (const it of items) {
    const key = `${it.category}|${it.zh}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  return [...groups.values()].map((g) => ({
    id: `${CODES_TOPIC}__z2c__${g[0].id}`,
    dir: "z2c",
    unit: g[0].category,
    prompt: g[0].zh,
    items: g,
  }));
}

// 判分：回傳 { ok, hint }
function judgeCodeAnswer(q, raw) {
  const input = String(raw || "").trim();
  if (!input) return { ok: false, hint: "" };

  if (q.dir === "z2c") {
    const valid = new Set();
    q.items.forEach((it) => _codeVariants(it.code).forEach((v) => valid.add(v)));
    // 可用空格 / 逗號 / 頓號分隔寫多個代碼，全部都要正確
    const tokens = input.split(/[\s,，、;；]+/).map(normalizeCode).filter(Boolean);
    const ok = tokens.length > 0 && tokens.every((t) => valid.has(t));
    return { ok, hint: "" };
  }

  // 代碼 → 中文：輸入裡只要包含任一關鍵字即算對（不限格式）
  const it = q.items[0];
  const norm = normalizeZh(input);
  const ok = it.accept.some((kw) => norm.includes(normalizeZh(kw)));
  let hint = "";
  if (!ok) {
    if (it.code === "SHA" || it.code === "PVG") {
      if (norm.includes("上海")) hint = "上海有兩個機場，要寫出「虹橋」或「浦東」";
    } else if (it.code.startsWith("WCH") && norm.includes("輪椅")) {
      hint = "三種輪椅代碼要寫出各自的說明";
    }
  }
  return { ok, hint };
}

// 正確答案的顯示文字
function codeAnswerText(q) {
  if (q.dir === "z2c") return q.items.map((it) => it.code).join(" / ");
  return q.items[0].zh;
}

// 給 dashboard 錯題回顧用：把 DB 的 question_id 轉成 parser.js 的題目物件形狀
async function loadCodeQuestionsForReview() {
  const bank = await loadCodeBank();
  const cats = [...new Set(bank.map((b) => b.category))];
  const all = [...buildCodeQuestions(bank, cats, "c2z"), ...buildCodeQuestions(bank, cats, "z2c")];
  return all.map((q) => ({
    id: q.id,
    topic: CODES_TOPIC,
    unit: q.unit,
    number: parseInt(q.items[0].id, 10),
    question: q.dir === "c2z" ? `代碼 → 中文：${q.prompt}` : `中文 → 代碼：${q.prompt}`,
    options: {},
    answer: codeAnswerText(q),
    explanation: `答案：${codeAnswerText(q)}　｜　${q.items.map((it) => it.mnemonic).join("；")}`,
    group_context: null,
    isCode: true,
  }));
}
