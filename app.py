import streamlit as st
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.question_parser import get_all_topics, get_units, load_questions
from utils.database import get_or_create_user
from utils.styles import inject_css

st.set_page_config(page_title="線上測驗平台", page_icon="📝", layout="centered")

inject_css()

# ── Hero Banner ──
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #4F46E5 100%);
                border-radius: 20px; padding: 2.5rem 2rem; margin-bottom: 2rem; text-align: center;">
      <div style="font-size: 2.5rem;">📝</div>
      <h1 style="color:white; font-size:1.8rem; font-weight:800; margin:0.3rem 0 0; letter-spacing:-0.5px;">線上測驗平台</h1>
      <p style="color:rgba(255,255,255,0.7); margin:0.4rem 0 0; font-size:0.9rem;">品牌企劃師備考系統</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session State 初始化 ──
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.user_name = None

# ── 未登入：登入區塊 ──
if st.session_state.user_id is None:
    st.markdown(
        "<p style='font-size:0.95rem; font-weight:600; color:#1E1B4B; margin-bottom:0.6rem;'>👋 歡迎，請先登入</p>",
        unsafe_allow_html=True,
    )

    name = st.text_input(
        "姓名",
        label_visibility="collapsed",
        placeholder="輸入你的姓名",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_btn = st.button("進入系統 →", type="primary", use_container_width=True)

    if login_btn:
        if not name.strip():
            st.warning("請輸入姓名。")
        else:
            user_id = get_or_create_user(name.strip())
            st.session_state.user_id = user_id
            st.session_state.user_name = name.strip()
            st.rerun()

    st.stop()

# ── 已登入：用戶頭像列 ──
first_letter = st.session_state.user_name[0].upper()
st.markdown(
    f"""
    <div style="background:white; border-radius:14px; padding:0.9rem 1.2rem;
                border:1px solid #E2E8F0; margin-bottom:1.5rem;
                display:flex; align-items:center; gap:0.8rem;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);">
      <div style="width:38px; height:38px; border-radius:50%;
                  background:linear-gradient(135deg,#4F46E5,#818CF8);
                  display:flex; align-items:center; justify-content:center;
                  color:white; font-weight:700; font-size:1rem; flex-shrink:0;">
        {first_letter}
      </div>
      <div>
        <div style="font-weight:700; color:#0F172A; font-size:0.92rem;">{st.session_state.user_name}</div>
        <div style="color:#64748B; font-size:0.78rem;">已登入</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 測驗設定 ──
st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:0 0 0.6rem;'>🎯 選擇測驗範圍</p>",
    unsafe_allow_html=True,
)

topics = get_all_topics()
if not topics:
    st.error("找不到任何題庫，請確認 questions/ 資料夾中有 Markdown 題目檔案。")
    st.stop()

topic = st.selectbox("主題", topics)

units = get_units(topic)
if not units:
    st.error(f"主題「{topic}」下找不到任何單元。")
    st.stop()

selected_units = st.multiselect(
    "單元（可複選）",
    units,
    default=[units[0]] if units else [],
)

st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:1rem 0 0.6rem;'>🔢 題數設定</p>",
    unsafe_allow_html=True,
)

mode = st.radio("題數模式", ["全部題目", "隨機抽取 N 題"], horizontal=True)

random_n = None
if mode == "隨機抽取 N 題":
    random_n = st.number_input("抽取題數", min_value=1, max_value=200, value=10, step=1)

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

if st.button("開始測驗 →", type="primary", use_container_width=True, disabled=len(selected_units) == 0):
    if not selected_units:
        st.warning("請至少選擇一個單元。")
    else:
        questions = load_questions(topic, selected_units)
        if not questions:
            st.error("選取的單元中找不到題目，請確認題庫格式正確。")
        else:
            if mode == "隨機抽取 N 題" and random_n:
                n = min(int(random_n), len(questions))
                questions = random.sample(questions, n)

            st.session_state.quiz_questions = questions
            st.session_state.quiz_topic = topic
            st.session_state.quiz_units = selected_units
            st.session_state.quiz_index = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False

            st.switch_page("pages/1_quiz.py")
