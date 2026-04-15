import random
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from utils.database import get_or_create_user
from utils.nav import render_sidebar
from utils.question_parser import get_all_topics, get_units, load_questions
from utils.styles import inject_css

st.set_page_config(page_title="線上測驗平台", page_icon="📝", layout="centered")
inject_css()
render_sidebar()

# ── Session State 初始化 ──
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.user_name = None

# ══════════════════════════════════════════
# 未登入
# ══════════════════════════════════════════
if st.session_state.user_id is None:

    # Hero
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1E1B4B 0%,#4F46E5 60%,#6366F1 100%);
                    border-radius:16px;padding:2.5rem 2rem 2rem;margin-bottom:2rem;
                    position:relative;overflow:hidden;">
          <div style="position:absolute;top:-30px;right:-30px;width:140px;height:140px;
                      border-radius:50%;background:rgba(255,255,255,0.05);"></div>
          <div style="position:absolute;bottom:-40px;right:60px;width:100px;height:100px;
                      border-radius:50%;background:rgba(255,255,255,0.04);"></div>
          <div style="font-size:2.4rem;margin-bottom:0.6rem;">📝</div>
          <h1 style="color:white;font-size:1.7rem;font-weight:800;margin:0 0 0.3rem;letter-spacing:-0.5px;">
            線上測驗平台
          </h1>
          <p style="color:rgba(255,255,255,0.65);margin:0;font-size:0.88rem;">
            選擇主題與單元，隨時開始練習
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 登入卡片
    st.markdown(
        """
        <div style="background:white;border-radius:14px;padding:1.6rem 1.8rem 1.4rem;
                    border:1px solid #E2E8F0;box-shadow:0 2px 12px rgba(79,70,229,0.06);
                    margin-bottom:1rem;">
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1.2rem;">
            <div style="width:3px;height:18px;background:#4F46E5;border-radius:2px;"></div>
            <span style="font-weight:700;color:#1E1B4B;font-size:0.95rem;">登入系統</span>
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
        "<div style='font-size:0.75rem;color:#94A3B8;margin:-0.3rem 0 1rem;'>輸入代號即可識別身份，無需密碼</div>",
        unsafe_allow_html=True,
    )

    col_l, col_btn, col_r = st.columns([1, 3, 1])
    with col_btn:
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
# 已登入
# ══════════════════════════════════════════

# 頁首
st.markdown(
    f"""
    <div style="background:white;border-radius:14px;padding:1rem 1.4rem;
                border:1px solid #E2E8F0;margin-bottom:1.8rem;
                display:flex;align-items:center;justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:0.8rem;">
        <div style="width:36px;height:36px;border-radius:50%;
                    background:linear-gradient(135deg,#4F46E5,#818CF8);
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-weight:700;font-size:0.9rem;">
          {st.session_state.user_name[0].upper()}
        </div>
        <div>
          <div style="font-weight:700;color:#0F172A;font-size:0.9rem;">{st.session_state.user_name}</div>
          <div style="color:#94A3B8;font-size:0.72rem;">用戶代號</div>
        </div>
      </div>
      <div style="background:#F0FDF4;color:#10B981;border-radius:20px;
                  padding:3px 12px;font-size:0.72rem;font-weight:600;border:1px solid #BBF7D0;">
        ● 已登入
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 區塊標題 helper ──
def section_header(icon: str, title: str):
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:0.5rem;margin:0 0 0.8rem;">
          <div style="width:3px;height:18px;background:#4F46E5;border-radius:2px;flex-shrink:0;"></div>
          <span style="font-size:0.9rem;font-weight:700;color:#1E1B4B;">{icon} {title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Step 1：選擇主題 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:14px;padding:1.4rem 1.6rem;"
        "border:1px solid #E2E8F0;margin-bottom:1rem;'>",
        unsafe_allow_html=True,
    )
    section_header("🎯", "選擇測驗主題")

    topics = get_all_topics()
    if not topics:
        st.error("找不到任何題庫，請確認 questions/ 資料夾中有 Markdown 題目檔案。")
        st.stop()

    topic = st.selectbox(
        "主題",
        ["— 請選擇主題 —"] + topics,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

if topic == "— 請選擇主題 —":
    st.stop()

# ── Step 2：選擇單元 ──
units = get_units(topic)
if not units:
    st.error(f"主題「{topic}」下找不到任何單元。")
    st.stop()

with st.container():
    st.markdown(
        "<div style='background:white;border-radius:14px;padding:1.4rem 1.6rem;"
        "border:1px solid #E2E8F0;margin-bottom:1rem;'>",
        unsafe_allow_html=True,
    )
    section_header("📚", "選擇單元範圍")

    col_sel, col_all = st.columns([4, 1])
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
            f"<div style='font-size:0.75rem;color:#64748B;margin-top:0.3rem;'>"
            f"已選 {len(selected_units)} / {len(units)} 個單元</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Step 3：題數設定 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:14px;padding:1.4rem 1.6rem;"
        "border:1px solid #E2E8F0;margin-bottom:1.4rem;'>",
        unsafe_allow_html=True,
    )
    section_header("🔢", "題數設定")

    mode = st.radio(
        "題數模式",
        ["全部題目", "隨機抽取 N 題"],
        horizontal=True,
        label_visibility="collapsed",
    )
    random_n = None
    if mode == "隨機抽取 N 題":
        random_n = st.number_input("抽取題數", min_value=1, max_value=200, value=10, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

# ── 開始按鈕 ──
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
            n = min(int(random_n), len(questions))
            questions = random.sample(questions, n)

        st.session_state.quiz_questions = questions
        st.session_state.quiz_topic = topic
        st.session_state.quiz_units = selected_units
        st.session_state.quiz_index = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.switch_page("pages/1_quiz.py")

if start_disabled:
    st.markdown(
        "<div style='text-align:center;font-size:0.78rem;color:#94A3B8;margin-top:0.4rem;'>"
        "請先選擇至少一個單元</div>",
        unsafe_allow_html=True,
    )
