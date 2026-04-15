import re
import os
from pathlib import Path

QUESTIONS_DIR = Path(__file__).parent.parent / "questions"


def _parse_questions_block(block: str) -> list[dict]:
    questions = []
    pattern = re.compile(r"^(\d+)\.\s", re.MULTILINE)
    matches = list(pattern.finditer(block))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        chunk = block[start:end].strip()

        lines = chunk.split("\n")
        number = int(match.group(1))

        question_lines = []
        options = {}
        option_pattern = re.compile(r"^\s*\(([ABCD])\)\s*(.*)")

        for line in lines[1:]:
            opt_match = option_pattern.match(line)
            if opt_match:
                options[opt_match.group(1)] = opt_match.group(2).strip()
            elif line.strip() and not option_pattern.match(line):
                stripped = line.strip()
                if stripped and not re.match(r"^\([ABCD]\)", stripped):
                    question_lines.append(stripped)

        question_text_raw = lines[0][len(match.group(0)):].strip()
        for line in lines[1:]:
            if not option_pattern.match(line) and line.strip():
                if not re.match(r"^\s*\([ABCD]\)", line):
                    question_text_raw += " " + line.strip()
            elif option_pattern.match(line):
                break

        question_text = re.sub(r"\s+", " ", question_text_raw).strip()

        if question_text and len(options) == 4:
            questions.append({
                "number": number,
                "question": question_text,
                "options": options,
            })

    return questions


def _parse_answers_block(block: str) -> dict[int, tuple[str, str]]:
    answers = {}
    pattern = re.compile(r"^(\d+)\.\s+\(([ABCD])\)\s*(.*)", re.MULTILINE)

    matches = list(pattern.finditer(block))
    for i, match in enumerate(matches):
        number = int(match.group(1))
        answer_letter = match.group(2)
        explanation_start = match.group(3).strip()

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        continuation = block[start:end].strip()

        explanation = explanation_start
        if continuation:
            explanation = (explanation + " " + continuation).strip()

        explanation = re.sub(r"\s+", " ", explanation).strip()
        answers[number] = (answer_letter, explanation)

    return answers


def _get_unit_name(filename: str) -> str:
    match = re.search(r"(Day\s*\d+)", filename, re.IGNORECASE)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    stem = Path(filename).stem
    return stem[:20] if len(stem) > 20 else stem


def _make_id(topic: str, unit: str, number: int) -> str:
    safe_topic = re.sub(r"[^\w]", "_", topic)
    safe_unit = re.sub(r"[^\w]", "_", unit)
    return f"{safe_topic}__{safe_unit}__{number}"


def load_questions_from_file(filepath: Path, topic: str) -> list[dict]:
    text = filepath.read_text(encoding="utf-8")
    separator = "解答與詳細解析"

    if separator not in text:
        return []

    parts = text.split(separator, 1)
    questions_block = parts[0]
    answers_block = parts[1]

    questions = _parse_questions_block(questions_block)
    answers = _parse_answers_block(answers_block)

    unit = _get_unit_name(filepath.name)

    result = []
    for q in questions:
        num = q["number"]
        answer_letter, explanation = answers.get(num, ("", ""))
        result.append({
            "id": _make_id(topic, unit, num),
            "topic": topic,
            "unit": unit,
            "number": num,
            "question": q["question"],
            "options": q["options"],
            "answer": answer_letter,
            "explanation": explanation,
            "group_context": None,
        })

    # 偵測題組題：含「承上題」的題目需附帶上一題作為情境
    for i in range(1, len(result)):
        if "承上題" in result[i]["question"]:
            result[i]["group_context"] = result[i - 1]["question"]

    return result


def get_all_topics() -> list[str]:
    if not QUESTIONS_DIR.exists():
        return []
    return sorted([
        d.name for d in QUESTIONS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])


def get_units(topic: str) -> list[str]:
    topic_dir = QUESTIONS_DIR / topic
    if not topic_dir.exists():
        return []

    units = []
    for f in topic_dir.glob("*.md"):
        unit = _get_unit_name(f.name)
        if unit not in units:
            units.append(unit)

    return sorted(units)


def load_questions(topic: str, units: list[str]) -> list[dict]:
    topic_dir = QUESTIONS_DIR / topic
    if not topic_dir.exists():
        return []

    all_questions = []
    for f in sorted(topic_dir.glob("*.md")):
        unit = _get_unit_name(f.name)
        if unit in units:
            all_questions.extend(load_questions_from_file(f, topic))

    return all_questions
