import sys
from collections import Counter
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import save_session
from utils.nav import render_sidebar
from utils.styles import inject_css

st.set_page_config(page_title="測驗進行", page_icon="", layout="centered")
inject_css()
render_sidebar()

# ── No questions loaded ──
if "quiz_questions" not in st.session_state or not st.session_state.quiz_questions:
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background:white;border-radius:8px;padding:2.8rem 2rem;text-align:center;
                    border:1px solid #E5E7EB;">
          <div style="width:36px;height:36px;background:#4F46E5;border-radius:6px;
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 1rem;">
            <div style="width:16px;height:16px;border:2px solid white;border-radius:2px;"></div>
          </div>
          <div style="font-weight:700;color:#111827;font-size:1rem;margin-bottom:0.4rem;">
            尚未設定測驗
          </div>
          <div style="color:#6B7280;font-size:0.86rem;">請先回首頁選擇主題與單元。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
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


# ── Section label helper ──
def section_label(text: str):
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
          <div style="width:3px;height:14px;background:#4F46E5;border-radius:1px;flex-shrink:0;"></div>
          <span style="font-size:0.68rem;font-weight:700;color:#6B7280;
                       letter-spacing:0.8px;text-transform:uppercase;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════
# Results page
# ══════════════════════════════════════════
def show_result():
    answers = st.session_state.quiz_answers
    correct_count = sum(
        1 for i, q in enumerate(questions) if answers.get(i) == q["answer"]
    )
    wrong_questions = [
        (i, q) for i, q in enumerate(questions) if answers.get(i) != q["answer"]
    ]

    # ── Save record ──
    if not st.session_state.quiz_saved:
        answer_records = [
            {
                "question_id": q["id"],
                "topic": q["topic"],
                "unit": q["unit"],
                "is_correct": answers.get(i, "") == q["answer"],
                "user_answer": answers.get(i, ""),
                "correct_answer": q["answer"],
            }
            for i, q in enumerate(questions)
        ]
        try:
            save_session(
                user_id=st.session_state.user_id,
                topic=st.session_state.quiz_topic,
                units=st.session_state.quiz_units,
                total=total,
                correct=correct_count,
                answers=answer_records,
            )
        except Exception as e:
            st.warning(f"成績儲存失敗（資料庫錯誤），但你仍可查看本次結果。\n\n{e}")
        st.session_state.quiz_saved = True

    pct = correct_count / total * 100 if total > 0 else 0
    score_color = "#10B981" if pct >= 80 else "#F59E0B" if pct >= 60 else "#EF4444"
    score_label = "優秀" if pct >= 80 else "加油" if pct >= 60 else "需補強"

    # ── Score donut ──
    conic = f"conic-gradient({score_color} 0% {pct:.1f}%, #E5E7EB {pct:.1f}% 100%)"
    st.markdown(
        f"""
        <div style="background:white;border-radius:8px;padding:2rem 1.5rem 1.6rem;
                    border:1px solid #E5E7EB;margin-bottom:1rem;text-align:center;">
          <div style="display:flex;justify-content:center;margin-bottom:1.2rem;">
            <div style="width:150px;height:150px;border-radius:50%;background:{conic};
                        display:flex;align-items:center;justify-content:center;">
              <div style="width:112px;height:112px;border-radius:50%;background:white;
                          display:flex;flex-direction:column;align-items:center;
                          justify-content:center;">
                <div style="font-size:1.6rem;font-weight:800;color:#111827;line-height:1.1;">
                  {correct_count}/{total}
                </div>
                <div style="font-size:0.88rem;font-weight:700;color:{score_color};">
                  {pct:.0f}%
                </div>
              </div>
            </div>
          </div>
          <div style="font-size:1rem;font-weight:800;color:#111827;margin-bottom:1rem;">
            測驗完成
          </div>
          <div style="display:flex;justify-content:center;gap:0;
                      background:#F9FAFB;border-radius:6px;border:1px solid #E5E7EB;
                      overflow:hidden;max-width:300px;margin:0 auto;">
            <div style="flex:1;text-align:center;padding:0.8rem 0;">
              <div style="font-size:1.15rem;font-weight:800;color:#10B981;">{correct_count}</div>
              <div style="font-size:0.68rem;color:#6B7280;margin-top:2px;text-transform:uppercase;letter-spacing:0.4px;">答對</div>
            </div>
            <div style="width:1px;background:#E5E7EB;"></div>
            <div style="flex:1;text-align:center;padding:0.8rem 0;">
              <div style="font-size:1.15rem;font-weight:800;color:#EF4444;">
                {len(wrong_questions)}
              </div>
              <div style="font-size:0.68rem;color:#6B7280;margin-top:2px;text-transform:uppercase;letter-spacing:0.4px;">答錯</div>
            </div>
            <div style="width:1px;background:#E5E7EB;"></div>
            <div style="flex:1;text-align:center;padding:0.8rem 0;">
              <div style="font-size:1.15rem;font-weight:800;color:{score_color};">
                {score_label}
              </div>
              <div style="font-size:0.68rem;color:#6B7280;margin-top:2px;text-transform:uppercase;letter-spacing:0.4px;">評等</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Weakness summary (only when weak units exist) ──
    if wrong_questions:
        wrong_unit_counts = Counter(q["unit"] for _, q in wrong_questions)
        total_unit_counts = Counter(q["unit"] for q in questions)

        weak_units = []
        for unit, wrong_cnt in wrong_unit_counts.most_common():
            total_cnt = total_unit_counts[unit]
            acc = (total_cnt - wrong_cnt) / total_cnt * 100
            if acc < 75:
                weak_units.append((unit, acc, wrong_cnt, total_cnt))

        if weak_units:
            items_html = ""
            for unit, acc, wrong_cnt, total_cnt in weak_units:
                bar_color = "#EF4444" if acc < 50 else "#F59E0B"
                items_html += f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                            padding:0.5rem 0;border-bottom:1px solid #F3F4F6;">
                  <div>
                    <div style="font-weight:600;color:#111827;font-size:0.84rem;">{unit}</div>
                    <div style="font-size:0.7rem;color:#6B7280;margin-top:1px;">
                      答錯 {wrong_cnt} / {total_cnt} 題
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-weight:700;color:{bar_color};font-size:0.9rem;">{acc:.0f}%</div>
                    <div style="font-size:0.66rem;color:#6B7280;">答對率</div>
                  </div>
                </div>
                """

            top_unit = weak_units[0][0]
            st.markdown(
                f"""
                <div style="background:white;border-radius:8px;padding:1.1rem 1.3rem;
                            border:1px solid #E5E7EB;border-left:3px solid #F59E0B;
                            margin-bottom:1rem;">
                  <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;">
                    <div style="width:8px;height:8px;background:#F59E0B;border-radius:1px;flex-shrink:0;"></div>
                    <span style="font-weight:700;color:#111827;font-size:0.84rem;">
                      本次弱點摘要
                    </span>
                  </div>
                  {items_html}
                  <div style="margin-top:0.8rem;font-size:0.78rem;color:#6B7280;
                              background:#F9FAFB;border-radius:4px;padding:0.5rem 0.7rem;
                              border:1px solid #E5E7EB;">
                    建議優先複習 <strong style="color:#111827;">{top_unit}</strong>，該單元答對率偏低
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Wrong questions expander ──
    with st.expander(f"答錯題目（{len(wrong_questions)} 題）", expanded=True):
        if not wrong_questions:
            st.success("全部答對！")
        else:
            for i, q in wrong_questions:
                user_ans = answers.get(i, "（未作答）")
                user_ans_text = (
                    q["options"].get(user_ans, "") if user_ans != "（未作答）" else ""
                )
                correct_text = q["options"].get(q["answer"], "")
                st.markdown(
                    f"""
                    <div style="background:white;border-left:3px solid #EF4444;
                                border-radius:0 6px 6px 0;padding:0.9rem 1.1rem;
                                margin-bottom:0.8rem;border-top:1px solid #E5E7EB;
                                border-right:1px solid #E5E7EB;border-bottom:1px solid #E5E7EB;">
                      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                        <div style="background:#EF4444;color:white;border-radius:2px;
                                    padding:1px 5px;font-size:0.62rem;font-weight:700;letter-spacing:0.5px;">
                          第 {i + 1} 題
                        </div>
                        <span style="font-size:0.75rem;color:#6B7280;">{q['unit']}</span>
                      </div>
                      <div style="color:#111827;font-size:0.87rem;line-height:1.65;
                                  margin-bottom:0.6rem;font-weight:500;">
                        {q['question']}
                      </div>
                      <div style="font-size:0.81rem;color:#EF4444;margin-bottom:0.2rem;">
                        ✗ 你的答案：({user_ans}) {user_ans_text}
                      </div>
                      <div style="font-size:0.81rem;color:#10B981;">
                        ✓ 正確答案：({q['answer']}) {correct_text}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if q["explanation"]:
                    st.info(q["explanation"])

    # ── All questions expander ──
    with st.expander("查看所有題目解析", expanded=False):
        for i, q in enumerate(questions):
            user_ans = answers.get(i, "（未作答）")
            is_correct = user_ans == q["answer"]
            user_ans_text = (
                q["options"].get(user_ans, "") if user_ans != "（未作答）" else ""
            )

            if is_correct:
                st.markdown(
                    f"""
                    <div style="background:white;border-left:3px solid #10B981;
                                border-radius:0 6px 6px 0;padding:0.9rem 1.1rem;
                                margin-bottom:0.8rem;border-top:1px solid #E5E7EB;
                                border-right:1px solid #E5E7EB;border-bottom:1px solid #E5E7EB;">
                      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                        <div style="background:#10B981;color:white;border-radius:2px;
                                    padding:1px 5px;font-size:0.62rem;font-weight:700;letter-spacing:0.5px;">
                          第 {i + 1} 題
                        </div>
                        <span style="font-size:0.72rem;color:#10B981;font-weight:600;">答對</span>
                      </div>
                      <div style="color:#111827;font-size:0.87rem;line-height:1.65;
                                  margin-bottom:0.4rem;font-weight:500;">
                        {q['question']}
                      </div>
                      <div style="font-size:0.81rem;color:#10B981;">
                        ✓ 你的答案：({user_ans}) {user_ans_text}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                correct_text = q["options"].get(q["answer"], "")
                st.markdown(
                    f"""
                    <div style="background:white;border-left:3px solid #EF4444;
                                border-radius:0 6px 6px 0;padding:0.9rem 1.1rem;
                                margin-bottom:0.8rem;border-top:1px solid #E5E7EB;
                                border-right:1px solid #E5E7EB;border-bottom:1px solid #E5E7EB;">
                      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                        <div style="background:#EF4444;color:white;border-radius:2px;
                                    padding:1px 5px;font-size:0.62rem;font-weight:700;letter-spacing:0.5px;">
                          第 {i + 1} 題
                        </div>
                        <span style="font-size:0.72rem;color:#EF4444;font-weight:600;">答錯</span>
                      </div>
                      <div style="color:#111827;font-size:0.87rem;line-height:1.65;
                                  margin-bottom:0.6rem;font-weight:500;">
                        {q['question']}
                      </div>
                      <div style="font-size:0.81rem;color:#EF4444;margin-bottom:0.2rem;">
                        ✗ 你的答案：({user_ans}) {user_ans_text}
                      </div>
                      <div style="font-size:0.81rem;color:#10B981;">
                        ✓ 正確答案：({q['answer']}) {correct_text}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            if q["explanation"]:
                st.info(f"解析：{q['explanation']}")

    # ── Home button ──
    st.markdown("<div style='margin-top:1.4rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("返回首頁", type="primary", use_container_width=True):
            st.session_state.quiz_questions = []
            st.session_state.quiz_submitted = False
            st.session_state.quiz_saved = False
            st.switch_page("app.py")


# ── Show results if submitted ──
if st.session_state.quiz_submitted:
    show_result()
    st.stop()

# ══════════════════════════════════════════
# Quiz in progress
# ══════════════════════════════════════════
idx = st.session_state.quiz_index
q = questions[idx]
answered_count = len(st.session_state.quiz_answers)

# ── Progress bar + counter + badges ──
progress_pct = idx / total
st.markdown(
    f"""
    <div style="background:white;border-radius:8px;padding:0.9rem 1.2rem 0.75rem;
                border:1px solid #E5E7EB;margin-bottom:1.1rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;
                  margin-bottom:0.55rem;">
        <div style="display:flex;align-items:center;gap:0.5rem;">
          <div style="background:#4F46E5;color:white;border-radius:3px;
                      padding:1px 7px;font-size:0.7rem;font-weight:700;letter-spacing:0.5px;">
            Q{idx + 1}
          </div>
          <span style="color:#9CA3AF;font-weight:500;font-size:0.78rem;">/ {total}</span>
        </div>
        <div style="display:flex;gap:0.4rem;align-items:center;">
          <span style="background:#F3F4F6;color:#6B7280;border-radius:3px;
                       padding:2px 8px;font-size:0.68rem;font-weight:600;letter-spacing:0.3px;">
            {q['topic']}
          </span>
          <span style="background:#F3F4F6;color:#6B7280;border-radius:3px;
                       padding:2px 8px;font-size:0.68rem;font-weight:600;letter-spacing:0.3px;">
            {q['unit']}
          </span>
        </div>
      </div>
    """,
    unsafe_allow_html=True,
)
st.progress(progress_pct)
st.markdown("</div>", unsafe_allow_html=True)

# ── 題組上文（承上題）──
if q.get("group_context"):
    st.markdown(
        f"""
        <div style="background:#F9FAFB;border-radius:6px;padding:0.9rem 1.1rem;
                    border:1px solid #E5E7EB;border-left:3px solid #6B7280;
                    margin-bottom:0.6rem;">
          <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.4rem;">
            <div style="background:#6B7280;color:white;border-radius:2px;
                        padding:1px 6px;font-size:0.62rem;font-weight:700;letter-spacing:0.5px;">
              題組
            </div>
            <span style="font-size:0.68rem;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.5px;">上一題情境</span>
          </div>
          <div style="font-size:0.87rem;color:#374151;line-height:1.65;">
            {q['group_context']}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Question card ──
st.markdown(
    f"""
    <div style="background:white;border-radius:8px;padding:1.4rem 1.5rem;
                border:1px solid #E5E7EB;margin-bottom:1.1rem;">
      <div style="display:flex;align-items:flex-start;gap:0.75rem;">
        <div style="background:#4F46E5;color:white;border-radius:3px;
                    padding:3px 8px;font-size:0.7rem;font-weight:700;
                    flex-shrink:0;margin-top:3px;letter-spacing:0.3px;">
          Q{idx + 1}
        </div>
        <p style="font-size:0.96rem;font-weight:600;color:#111827;
                  line-height:1.7;margin:0;">
          {q['question']}
        </p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Options ──
option_labels = [f"({k})  {v}" for k, v in q["options"].items()]
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

# ── Navigation row: prev / answered count / next ──
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if idx > 0:
        if st.button("← 上一題", use_container_width=True):
            st.session_state.quiz_index -= 1
            st.rerun()

with col2:
    answered = len(st.session_state.quiz_answers)
    st.markdown(
        f"<div style='text-align:center;font-size:0.75rem;color:#9CA3AF;padding-top:0.4rem;'>"
        f"已作答 {answered} / {total} 題</div>",
        unsafe_allow_html=True,
    )

with col3:
    if idx < total - 1:
        if st.button("下一題 →", type="primary", use_container_width=True):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再繼續。")
            else:
                st.session_state.quiz_index += 1
                st.rerun()
    else:
        if st.button("送出", type="primary", use_container_width=True):
            if st.session_state.quiz_answers.get(idx) is None:
                st.warning("請先選擇答案再送出。")
            else:
                st.session_state.quiz_submitted = True
                st.rerun()
