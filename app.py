import random
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from utils.database import get_or_create_user
from utils.nav import render_sidebar
from utils.question_parser import get_all_topics, get_units, load_questions
from utils.styles import inject_css

st.set_page_config(page_title="線上測驗平台", page_icon="", layout="centered")
inject_css()
render_sidebar()

# ── Session State init ──
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.user_name = None

# ══════════════════════════════════════════
# Not logged in — centered login card
# ══════════════════════════════════════════
if st.session_state.user_id is None:

    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Brand mark
        st.markdown(
            """
            <div style="text-align:center;margin-bottom:1.8rem;">
              <div style="display:flex;justify-content:center;margin-bottom:0.9rem;">
                <div style="width:40px;height:40px;background:#4F46E5;border-radius:8px;
                            display:flex;align-items:center;justify-content:center;">
                  <div style="width:18px;height:18px;border:2.5px solid white;border-radius:3px;"></div>
                </div>
              </div>
              <div style="font-size:1.3rem;font-weight:800;color:#111827;
                          letter-spacing:-0.5px;margin-bottom:0.3rem;">線上測驗平台</div>
              <div style="font-size:0.82rem;color:#9CA3AF;font-weight:500;">
                選擇主題與單元，隨時開始練習
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Login card with indigo top accent
        st.markdown(
            """
            <div style="background:white;border-radius:8px;
                        border-top:3px solid #4F46E5;border-left:1px solid #E5E7EB;
                        border-right:1px solid #E5E7EB;border-bottom:1px solid #E5E7EB;
                        padding:1.75rem 1.75rem 1.5rem;">
              <div style="font-size:0.68rem;font-weight:700;color:#6B7280;
                          letter-spacing:0.8px;text-transform:uppercase;margin-bottom:0.6rem;">
                用戶代號
              </div>
            """,
            unsafe_allow_html=True,
        )

        name = st.text_input(
            "用戶代號",
            placeholder="輸入你的專屬代號",
            label_visibility="collapsed",
        )
        st.markdown(
            "<div style='font-size:0.74rem;color:#9CA3AF;margin:-0.3rem 0 1.2rem;'>"
            "輸入代號即可識別身份，無需密碼</div>",
            unsafe_allow_html=True,
        )
        login_btn = st.button("進入系統 →", type="primary", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    if login_btn:
        if not name.strip():
            st.warning("請輸入用戶代號。")
        else:
            try:
                user_id = get_or_create_user(name.strip())
                st.session_state.user_id = user_id
                st.session_state.user_name = name.strip()
                st.rerun()
            except Exception as e:
                st.error(f"無法連線至資料庫，請稍後再試。\n\n錯誤訊息：{e}")

    st.stop()

# ══════════════════════════════════════════
# Logged in
# ══════════════════════════════════════════

# ── Slim user status bar ──
st.markdown(
    f"""
    <div style="background:white;border-radius:8px;padding:0.6rem 1rem;
                border:1px solid #E5E7EB;margin-bottom:1.5rem;
                display:flex;align-items:center;justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:0.6rem;">
        <div style="width:28px;height:28px;border-radius:4px;
                    background:#4F46E5;
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-weight:700;font-size:0.75rem;flex-shrink:0;">
          {st.session_state.user_name[0].upper()}
        </div>
        <div>
          <div style="font-weight:700;color:#111827;font-size:0.85rem;line-height:1.3;">
            {st.session_state.user_name}
          </div>
          <div style="color:#9CA3AF;font-size:0.68rem;">用戶代號</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:0.4rem;
                  font-size:0.7rem;font-weight:600;color:#6B7280;">
        <span style="width:6px;height:6px;border-radius:50%;background:#10B981;
                     display:inline-block;"></span>
        已登入
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── Step card helper ──
def step_card_open(number: str, label: str):
    st.markdown(
        f"""
        <div style="background:white;border-radius:8px;padding:1.25rem 1.5rem;
                    border:1px solid #E5E7EB;margin-bottom:0.8rem;">
          <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
            <div style="background:#4F46E5;color:white;border-radius:3px;
                        padding:1px 7px;font-size:0.65rem;font-weight:700;
                        letter-spacing:1px;">{number}</div>
            <span style="font-size:0.85rem;font-weight:700;color:#111827;letter-spacing:-0.1px;">{label}</span>
          </div>
        """,
        unsafe_allow_html=True,
    )


def step_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


# ── Step 01: Topic ──
step_card_open("01", "主題")

topics = get_all_topics()
if not topics:
    st.error("找不到任何題庫，請確認 questions/ 資料夾中有 Markdown 題目檔案。")
    st.stop()

topic = st.selectbox(
    "主題",
    ["— 請選擇主題 —"] + topics,
    label_visibility="collapsed",
)
step_card_close()

if topic == "— 請選擇主題 —":
    st.stop()

# ── Step 02: Units ──
units = get_units(topic)
if not units:
    st.error(f"主題「{topic}」下找不到任何單元。")
    st.stop()

step_card_open("02", "單元")

col_sel, col_all = st.columns([5, 1])
with col_all:
    select_all = st.button("全選", use_container_width=True)

default_units = units if select_all else []
selected_units = st.multiselect(
    "單元（可複選）",
    units,
    default=default_units,
    label_visibility="collapsed",
)

if selected_units:
    st.markdown(
        f"<div style='font-size:0.74rem;color:#6B7280;margin-top:0.3rem;'>"
        f"已選 {len(selected_units)} / {len(units)} 個單元</div>",
        unsafe_allow_html=True,
    )

step_card_close()

# ── Step 03: Count ──
step_card_open("03", "題數")

mode = st.radio(
    "題數模式",
    ["全部題目", "隨機抽取 N 題"],
    horizontal=True,
    label_visibility="collapsed",
)
random_n = None
if mode == "隨機抽取 N 題":
    random_n = st.number_input("抽取題數", min_value=1, max_value=200, value=10, step=1)

step_card_close()

# ── Start CTA ──
st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)
start_disabled = len(selected_units) == 0

if st.button(
    "開始測驗 →",
    type="primary",
    use_container_width=True,
    disabled=start_disabled,
):
    questions = load_questions(topic, selected_units)
    if not questions:
        st.error("選取的單元中找不到題目，請確認題庫格式正確。")
    else:
        if mode == "隨機抽取 N 題" and random_n:
            # 將題組題（承上題）與前一題綁定為同一 group，抽題以 group 為單位
            groups: list[list] = []
            for q in questions:
                if q.get("group_context") is not None and groups:
                    groups[-1].append(q)
                else:
                    groups.append([q])
            n = min(int(random_n), len(groups))
            sampled = random.sample(groups, n)
            questions = [q for grp in sampled for q in grp]

        st.session_state.quiz_questions = questions
        st.session_state.quiz_topic = topic
        st.session_state.quiz_units = selected_units
        st.session_state.quiz_index = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.switch_page("pages/1_quiz.py")

if start_disabled:
    st.markdown(
        "<div style='text-align:center;font-size:0.76rem;color:#9CA3AF;margin-top:0.5rem;'>"
        "請先選擇至少一個單元</div>",
        unsafe_allow_html=True,
    )
