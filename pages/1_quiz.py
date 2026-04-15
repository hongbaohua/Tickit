import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import save_session
from utils.styles import inject_css

st.set_page_config(page_title="測驗中", page_icon="📝", layout="centered")

inject_css()

# ── 尚未選題 ──
if "quiz_questions" not in st.session_state or not st.session_state.quiz_questions:
    st.markdown(
        """
        <div style="background:white; border-radius:16px; padding:2rem; text-align:center;
                    border:1px solid #E2E8F0; box-shadow:0 2px 12px rgba(0,0,0,0.06);">
          <div style="font-size:2rem; margin-bottom:0.8rem;">⚠️</div>
          <p style="color:#64748B; font-size:0.95rem; margin:0;">尚未選擇題目，請先回首頁設定測驗範圍。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("回首頁", type="primary", use_container_width=True):
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

    # ── 儲存紀錄 ──
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

    pct = correct_count / total * 100 if total > 0 else 0
    score_color = "#10B981" if pct >= 80 else "#F59E0B" if pct >= 60 else "#EF4444"

    # ── 分數圓圈 ──
    conic = f"conic-gradient({score_color} 0% {pct:.1f}%, #E2E8F0 {pct:.1f}% 100%)"
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin:1.5rem 0 1rem;">
          <div style="width:160px; height:160px; border-radius:50%;
                      background:{conic};
                      display:flex; align-items:center; justify-content:center;">
            <div style="width:120px; height:120px; border-radius:50%; background:white;
                        display:flex; flex-direction:column; align-items:center; justify-content:center;
                        box-shadow:0 2px 12px rgba(0,0,0,0.08);">
              <div style="font-size:1.6rem; font-weight:800; color:#0F172A; line-height:1.1;">
                {correct_count}/{total}
              </div>
              <div style="font-size:0.85rem; font-weight:600; color:{score_color};">
                {pct:.0f}%
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h2 style='text-align:center; color:#0F172A; font-size:1.4rem; font-weight:800; margin:0;'>測驗完成</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center; color:#64748B; margin:0.3rem 0 1.2rem;'>答對率 {pct:.1f}%</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 答錯題目 expander ──
    wrong_questions = [
        (i, q) for i, q in enumerate(questions)
        if answers.get(i) != q["answer"]
    ]

    with st.expander(f"❌ 答錯題目（{len(wrong_questions)} 題）", expanded=True):
        if not wrong_questions:
            st.success("🎉 全部答對！")
        else:
            for i, q in wrong_questions:
                user_ans = answers.get(i, "（未作答）")
                user_ans_text = q["options"].get(user_ans, "") if user_ans != "（未作答）" else ""
                correct_text = q["options"].get(q["answer"], "")
                st.markdown(
                    f"""
                    <div style="background:#FFF5F5; border-left:4px solid #EF4444;
                                border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:1rem;">
                      <div style="font-weight:700; color:#0F172A; margin-bottom:0.5rem;">第 {q['number']} 題</div>
                      <div style="color:#374151; font-size:0.92rem; line-height:1.6; margin-bottom:0.7rem;">{q['question']}</div>
                      <div style="color:#EF4444; font-size:0.88rem; margin-bottom:0.3rem;">✗ 你的答案：({user_ans}) {user_ans_text}</div>
                      <div style="color:#10B981; font-size:0.88rem;">✓ 正確答案：({q['answer']}) {correct_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if q["explanation"]:
                    st.info(f"解析：{q['explanation']}")

    # ── 所有題目解析 expander ──
    with st.expander("📖 查看所有題目解析", expanded=False):
        for i, q in enumerate(questions):
            user_ans = answers.get(i, "（未作答）")
            is_correct = user_ans == q["answer"]
            user_ans_text = q["options"].get(user_ans, "") if user_ans != "（未作答）" else ""

            if is_correct:
                card_bg = "#F0FDF4"
                border_color = "#10B981"
                icon = "✓"
                ans_color = "#10B981"
                st.markdown(
                    f"""
                    <div style="background:{card_bg}; border-left:4px solid {border_color};
                                border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:1rem;">
                      <div style="font-weight:700; color:#0F172A; margin-bottom:0.5rem;">{icon} 第 {q['number']} 題</div>
                      <div style="color:#374151; font-size:0.92rem; line-height:1.6; margin-bottom:0.7rem;">{q['question']}</div>
                      <div style="color:{ans_color}; font-size:0.88rem;">你的答案：({user_ans}) {user_ans_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                correct_text = q["options"].get(q["answer"], "")
                st.markdown(
                    f"""
                    <div style="background:#FFF5F5; border-left:4px solid #EF4444;
                                border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:1rem;">
                      <div style="font-weight:700; color:#0F172A; margin-bottom:0.5rem;">✗ 第 {q['number']} 題</div>
                      <div style="color:#374151; font-size:0.92rem; line-height:1.6; margin-bottom:0.7rem;">{q['question']}</div>
                      <div style="color:#EF4444; font-size:0.88rem; margin-bottom:0.3rem;">✗ 你的答案：({user_ans}) {user_ans_text}</div>
                      <div style="color:#10B981; font-size:0.88rem;">✓ 正確答案：({q['answer']}) {correct_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            if q["explanation"]:
                st.info(f"解析：{q['explanation']}")

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("返回首頁", type="primary", use_container_width=True):
            st.session_state.quiz_questions = []
            st.session_state.quiz_submitted = False
            st.session_state.quiz_saved = False
            st.switch_page("app.py")


# ── 結果頁 ──
if st.session_state.quiz_submitted:
    show_result()
    st.stop()

# ── 測驗進行中 ──
idx = st.session_state.quiz_index
q = questions[idx]

# 進度區
st.markdown(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
      <span style="font-size:0.82rem; color:#64748B; font-weight:500;">第 {idx + 1} 題 / 共 {total} 題</span>
      <span style="font-size:0.82rem; color:#64748B;">{q['topic']} · {q['unit']}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.progress(idx / total)

# 題目卡片
st.markdown(
    f"""
    <div style="background:white; border-radius:16px; padding:1.5rem 1.8rem;
                border:1px solid #E2E8F0; box-shadow:0 2px 12px rgba(79,70,229,0.07); margin:1.2rem 0;">
      <div style="display:inline-block; background:#EEF2FF; color:#4F46E5;
                  border-radius:8px; padding:2px 10px; font-size:0.78rem; font-weight:700; margin-bottom:0.8rem;">
        Q{q['number']}
      </div>
      <p style="font-size:1rem; font-weight:600; color:#0F172A; line-height:1.7; margin:0;">
        {q['question']}
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 選項
option_labels = [f"({k}) {v}" for k, v in q["options"].items()]
option_keys = list(q["options"].keys())

current_answer = st.session_state.quiz_answers.get(idx)
current_index = option_keys.index(current_answer) if current_answer in option_keys else None

selected = st.radio(
    "請選擇答案",
    option_labels,
    index=current_index,
    key=f"radio_{idx}",
    label_visibility="collapsed",
)

if selected:
    letter = selected[1]
    st.session_state.quiz_answers[idx] = letter

st.divider()

# 導航按鈕
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if idx > 0:
        if st.button("⬅ 上一題", use_container_width=True):
            st.session_state.quiz_index -= 1
            st.rerun()

with col3:
    if idx < total - 1:
        if st.button("下一題 ➡", type="primary", use_container_width=True):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再繼續。")
            else:
                st.session_state.quiz_index += 1
                st.rerun()
    else:
        if st.button("送出 ✅", type="primary", use_container_width=True):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再送出。")
            else:
                st.session_state.quiz_submitted = True
                st.rerun()
