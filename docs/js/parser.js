// Port of utils/question_parser.py
// IMPORTANT: question_id format must stay identical to the Python version

function _safeStr(s) {
  // Match Python: re.sub(r"[^\w]", "_", s)
  // Python \w includes Unicode word chars (CJK, etc.)
  // JS: use \p{L}\p{N} with u flag to replicate Unicode \w behaviour
  return s.replace(/[^\p{L}\p{N}_]/gu, "_");
}

function _getUnitName(filename) {
  const m = filename.match(/Day\s*\d+/i);
  if (m) return m[0].replace(/\s+/g, " ").trim();
  const stem = filename.replace(/\.md$/i, "");
  return stem.length > 20 ? stem.slice(0, 20) : stem;
}

function _makeId(topic, unit, number) {
  return `${_safeStr(topic)}__${_safeStr(unit)}__${number}`;
}

function _parseQuestionsBlock(block) {
  const questions = [];
  // 支援 1. 1、 1 (空格) 等格式
  const pattern = /^\s*(\d+)[.、\s]\s*/gm;
  const matches = [...block.matchAll(pattern)];

  const optionPattern = /^\s*\(([A-D])\)\s*(.*)/;

  for (let i = 0; i < matches.length; i++) {
    const start = matches[i].index;
    const end = i + 1 < matches.length ? matches[i + 1].index : block.length;
    const chunk = block.slice(start, end).trim();
    const lines = chunk.split("\n");
    const number = parseInt(matches[i][1], 10);

    const options = {};
    let questionTextRaw = "";

    // 取得題目文字：從題號後開始，直到遇到第一個選項 (A)
    let headerLine = lines[0].replace(/^\s*\d+[.、\s]\s*/, "").trim();
    questionTextRaw = headerLine;

    let foundOptions = false;
    for (let j = 1; j < lines.length; j++) {
      const line = lines[j];
      const optMatch = line.match(optionPattern);
      if (optMatch) {
        options[optMatch[1]] = optMatch[2].trim();
        foundOptions = true;
      } else if (!foundOptions && line.trim()) {
        questionTextRaw += " " + line.trim();
      }
    }

    if (questionTextRaw && Object.keys(options).length > 0) {
      questions.push({ number, question: questionTextRaw.replace(/\s+/g, " ").trim(), options });
    }
  }
  return questions;
}

function _parseAnswersBlock(block) {
  const answers = {};
  // 匹配行首的題號 1. 1、 或 1 (空格)，接著是 (A) 或 (A/B) 等格式
  const pattern = /^\s*(\d+)[.、\s]?\s*(?:\*\*)?\(([^)]+)\)(?:\*\*)?\s*(.*)/gm;
  const matches = [...block.matchAll(pattern)];

  for (let i = 0; i < matches.length; i++) {
    const number = parseInt(matches[i][1], 10);
    const letter = matches[i][2].trim();
    let initialExp = matches[i][3].trim();

    const start = matches[i].index + matches[i][0].length;
    const end = i + 1 < matches.length ? matches[i + 1].index : block.length;
    const continuation = block.slice(start, end).trim();

    let fullExplanation = initialExp;
    if (continuation) {
      fullExplanation = fullExplanation ? (fullExplanation + " " + continuation) : continuation;
    }
    
    answers[number] = { 
      letter: letter, 
      explanation: fullExplanation.replace(/\s+/g, " ").trim() 
    };
  }
  return answers;
}

function parseMarkdown(text, topic, filename) {
  // 更加靈活的切割點，支援各種標題與分隔線組合
  const separatorKeywords = ["解答與詳細解析", "答案與解析"];
  let sepIndex = -1;
  let sepLength = 0;

  for (const kw of separatorKeywords) {
    const regex = new RegExp(`(?:^|\\n)[#\\s\\-]*${kw}[#\\s\\-]*`, "i");
    const match = text.match(regex);
    if (match) {
      sepIndex = match.index;
      sepLength = match[0].length;
      break;
    }
  }
  
  if (sepIndex === -1) {
    console.warn("未能在檔案中找到解答區段標記:", filename);
    return [];
  }

  const questionsBlock = text.slice(0, sepIndex);
  const answersBlock = text.slice(sepIndex + sepLength);
  
  const questions = _parseQuestionsBlock(questionsBlock);
  const answers = _parseAnswersBlock(answersBlock);
  const unit = _getUnitName(filename);

  const result = questions.map((q) => {
    const ans = answers[q.number] || { letter: "", explanation: "" };
    return {
      id: _makeId(topic, unit, q.number),
      topic,
      unit,
      number: q.number,
      question: q.question,
      options: q.options,
      answer: ans.letter || "",
      explanation: ans.explanation || "",
      group_context: null,
    };
  });

  // 承上題 group context
  for (let i = 1; i < result.length; i++) {
    if (result[i].question.includes("承上題")) {
      result[i].group_context = result[i - 1].question;
    }
  }

  return result;
}

async function loadQuestions(topic, selectedUnits) {
  const manifestRes = await fetch("questions/manifest.json");
  const manifest = await manifestRes.json();

  // 規範化比對主題名稱，忽略空格與底線差異
  const normalize = s => s.trim().replace(/[_\s]+/g, "_");
  const targetTopic = normalize(topic);
  const topicData = manifest.topics.find((t) => normalize(t.name) === targetTopic);
  
  if (!topicData) {
    console.error("Topic not found in manifest:", topic);
    return [];
  }

  const units = topicData.units.filter((u) => selectedUnits.includes(u.unit));
  const allQuestions = [];

  for (const u of units) {
    const path = `questions/${encodeURIComponent(topicData.name)}/${encodeURIComponent(u.file)}`;
    const res = await fetch(path);
    if (!res.ok) {
      console.error("Failed to fetch unit file:", path);
      continue;
    }
    const text = await res.text();
    const qs = parseMarkdown(text, topicData.name, u.file);
    allQuestions.push(...qs);
  }

  return allQuestions;
}

function sampleQuestions(questions, n) {
  // Group 承上題 so they stay together
  const groups = [];
  for (const q of questions) {
    if (q.group_context !== null && groups.length > 0) {
      groups[groups.length - 1].push(q);
    } else {
      groups.push([q]);
    }
  }
  // Fisher-Yates shuffle of groups
  for (let i = groups.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [groups[i], groups[j]] = [groups[j], groups[i]];
  }
  const count = Math.min(n, groups.length);
  return groups.slice(0, count).flat();
}

// 打亂每題的選項順序，同步更新正確答案字母，並移除選項末尾的句號
function shuffleOptions(questions) {
  return questions.map(q => {
    const letters = Object.keys(q.options); // ["A","B","C","D"]
    const origValues = letters.map(l => q.options[l]);
    const correctOrigText = q.options[q.answer];

    // 若答案無法對應單一選項（如 C/D 多選題），僅清除句號，不打亂順序
    if (correctOrigText === undefined) {
      const newOptions = {};
      letters.forEach(l => {
        const v = q.options[l];
        newOptions[l] = v.endsWith("。") ? v.slice(0, -1) : v;
      });
      return { ...q, options: newOptions };
    }

    // Fisher-Yates shuffle of values
    const shuffled = [...origValues];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    // 移除末尾句號
    const cleaned = shuffled.map(v => v.endsWith("。") ? v.slice(0, -1) : v);

    // 建立新選項
    const newOptions = {};
    letters.forEach((letter, i) => { newOptions[letter] = cleaned[i]; });

    // 找正確答案在新排列中的字母
    const cleanCorrectText = correctOrigText.endsWith("。") ? correctOrigText.slice(0, -1) : correctOrigText;
    let newAnswer = q.answer;
    for (let i = 0; i < letters.length; i++) {
      if (cleaned[i] === cleanCorrectText) { newAnswer = letters[i]; break; }
    }

    return { ...q, options: newOptions, answer: newAnswer };
  });
}
