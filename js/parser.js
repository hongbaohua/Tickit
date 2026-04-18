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
  const pattern = /^(\d+)\.\s/gm;
  const matches = [...block.matchAll(pattern)];

  for (let i = 0; i < matches.length; i++) {
    const start = matches[i].index;
    const end = i + 1 < matches.length ? matches[i + 1].index : block.length;
    const chunk = block.slice(start, end).trim();
    const lines = chunk.split("\n");
    const number = parseInt(matches[i][1], 10);

    const optionPattern = /^\s*\(([ABCD])\)\s*(.*)/;
    const options = {};
    let questionTextRaw = lines[0].slice(matches[i][0].length).trim();

    for (let j = 1; j < lines.length; j++) {
      const line = lines[j];
      const optMatch = line.match(optionPattern);
      if (optMatch) {
        options[optMatch[1]] = optMatch[2].trim();
      } else if (line.trim() && !line.match(/^\s*\([ABCD]\)/)) {
        questionTextRaw += " " + line.trim();
      } else if (optMatch) {
        break;
      }
    }

    // Stop appending question text once options start
    questionTextRaw = (() => {
      let text = lines[0].slice(matches[i][0].length).trim();
      for (let j = 1; j < lines.length; j++) {
        if (lines[j].match(optionPattern)) break;
        if (lines[j].trim()) text += " " + lines[j].trim();
      }
      return text.replace(/\s+/g, " ").trim();
    })();

    if (questionTextRaw && Object.keys(options).length === 4) {
      questions.push({ number, question: questionTextRaw, options });
    }
  }
  return questions;
}

function _parseAnswersBlock(block) {
  const answers = {};
  const pattern = /^(\d+)\.\s+\(([ABCD])\)\s*(.*)/gm;
  const matches = [...block.matchAll(pattern)];

  for (let i = 0; i < matches.length; i++) {
    const number = parseInt(matches[i][1], 10);
    const letter = matches[i][2];
    let explanation = matches[i][3].trim();

    const start = matches[i].index + matches[i][0].length;
    const end = i + 1 < matches.length ? matches[i + 1].index : block.length;
    const continuation = block.slice(start, end).trim();

    if (continuation) explanation = (explanation + " " + continuation).trim();
    explanation = explanation.replace(/\s+/g, " ").trim();
    answers[number] = { letter, explanation };
  }
  return answers;
}

function parseMarkdown(text, topic, filename) {
  const SEPARATOR = "解答與詳細解析";
  if (!text.includes(SEPARATOR)) return [];

  const [questionsBlock, answersBlock] = text.split(SEPARATOR);
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
      answer: ans.letter,
      explanation: ans.explanation,
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

  const topicData = manifest.topics.find((t) => t.name === topic);
  if (!topicData) return [];

  const units = topicData.units.filter((u) => selectedUnits.includes(u.unit));
  const allQuestions = [];

  for (const u of units) {
    const path = `questions/${encodeURIComponent(topic)}/${encodeURIComponent(u.file)}`;
    const res = await fetch(path);
    if (!res.ok) continue;
    const text = await res.text();
    const qs = parseMarkdown(text, topic, u.file);
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
  const count = Math.min(n, groups.length);
  const shuffled = groups.sort(() => Math.random() - 0.5).slice(0, count);
  return shuffled.flat();
}
