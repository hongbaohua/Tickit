import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import save_session

st.set_page_config(page_title="測驗中", page_icon="📝", layout="centered")

if "quiz_questions" not in st.session_state or not st.session_state.quiz_questions:
    st.warning("尚未選擇題目，請先回首頁設定測驗範圍。")
    if st.button("回首頁"):
        st.switch_page("app.py")
    st.stop()

questions = st.session_state.quiz_questions
total = len(questions)

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_saved" not in st.session_state:
    st.session_state.quiz_saved = False


def show_result():
    answers = st.session_state.quiz_answers
    correct_count = sum(
        1 for i, q in enumerate(questions)
        if answers.get(i) == q["answer"]
    )

    if not st.session_state.quiz_saved:
        answer_records = []
        for i, q in enumerate(questions):
            user_ans = answers.get(i, "")
            answer_records.append({
                "question_id": q["id"],
                "topic": q["topic"],
                "unit": q["unit"],
                "is_correct": user_ans == q["answer"],
                "user_answer": user_ans,
                "correct_answer": q["answer"],
            })

        save_session(
            user_id=st.session_state.user_id,
            topic=st.session_state.quiz_topic,
            units=st.session_state.quiz_units,
            total=total,
            correct=correct_count,
            answers=answer_records,
        )
        st.session_state.quiz_saved = True

    st.title(f"測驗結果：{correct_count} / {total} 題答對")
    accuracy = correct_count / total * 100 if total > 0 else 0
    st.progress(correct_count / total if total > 0 else 0)
    st.write(f"答對率：**{accuracy:.1f}%**")

    st.divider()

    wrong_questions = [
        (i, q) for i, q in enumerate(questions)
        if answers.get(i) != q["answer"]
    ]

    with st.expander(f"❌ 答錯題目（{len(wrong_questions)} 題）", expanded=True):
        if not wrong_questions:
            st.success("全部答對！")
        else:
            for i, q in wrong_questions:
                user_ans = answers.get(i, "（未作答）")
                st.markdown(f"**第 {q['number']} 題**")
                st.write(q["question"])
                st.markdown(
                    f"你的答案：<span style='color:red'>**({user_ans}) {q['options'].get(user_ans, '')}**</span>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"正確答案：<span style='color:green'>**({q['answer']}) {q['options'].get(q['answer'], '')}**</span>",
                    unsafe_allow_html=True
                )
                if q["explanation"]:
                    st.info(f"解析：{q['explanation']}")
                st.divider()

    with st.expander("📖 查看所有題目解析", expanded=False):
        for i, q in enumerate(questions):
            user_ans = answers.get(i, "（未作答）")
            is_correct = user_ans == q["answer"]
            icon = "✅" if is_correct else "❌"
            st.markdown(f"{icon} **第 {q['number']} 題**")
            st.write(q["question"])
            if is_correct:
                st.markdown(
                    f"你的答案：<span style='color:green'>**({user_ans}) {q['options'].get(user_ans, '')}**</span>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"你的答案：<span style='color:red'>**({user_ans}) {q['options'].get(user_ans, '')}**</span>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"正確答案：<span style='color:green'>**({q['answer']}) {q['options'].get(q['answer'], '')}**</span>",
                    unsafe_allow_html=True
                )
            if q["explanation"]:
                st.info(f"解析：{q['explanation']}")
            st.divider()

    if st.button("返回首頁", type="primary"):
        st.session_state.quiz_questions = []
        st.session_state.quiz_submitted = False
        st.session_state.quiz_saved = False
        st.switch_page("app.py")


if st.session_state.quiz_submitted:
    show_result()
    st.stop()

idx = st.session_state.quiz_index
q = questions[idx]

st.progress((idx) / total)
st.caption(f"第 {idx + 1} 題，共 {total} 題　｜　主題：{q['topic']}　單元：{q['unit']}")

st.subheader(f"Q{q['number']}. {q['question']}")

option_labels = [f"({k}) {v}" for k, v in q["options"].items()]
option_keys = list(q["options"].keys())

current_answer = st.session_state.quiz_answers.get(idx)
current_index = option_keys.index(current_answer) if current_answer in option_keys else None

selected = st.radio(
    "請選擇答案",
    option_labels,
    index=current_index,
    key=f"radio_{idx}"
)

if selected:
    letter = selected[1]
    st.session_state.quiz_answers[idx] = letter

st.divider()

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if idx > 0:
        if st.button("⬅ 上一題"):
            st.session_state.quiz_index -= 1
            st.rerun()

with col3:
    if idx < total - 1:
        if st.button("下一題 ➡", type="primary"):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再繼續。")
            else:
                st.session_state.quiz_index += 1
                st.rerun()
    else:
        if st.button("送出測驗 ✅", type="primary"):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再送出。")
            else:
                st.session_state.quiz_submitted = True
                st.rerun()
