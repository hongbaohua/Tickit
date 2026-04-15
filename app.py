import streamlit as st
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.question_parser import get_all_topics, get_units, load_questions
from utils.database import get_or_create_user

st.set_page_config(page_title="線上測驗平台", page_icon="📝", layout="centered")
st.title("📝 線上測驗平台")

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.user_name = None

if st.session_state.user_id is None:
    st.subheader("登入")
    name = st.text_input("請輸入你的姓名", placeholder="例如：王小明")
    if st.button("開始 / 登入", type="primary"):
        if not name.strip():
            st.warning("請輸入姓名。")
        else:
            user_id = get_or_create_user(name.strip())
            st.session_state.user_id = user_id
            st.session_state.user_name = name.strip()
            st.rerun()
    st.stop()

st.success(f"歡迎回來，**{st.session_state.user_name}**！")

st.divider()
st.subheader("選擇測驗範圍")

topics = get_all_topics()
if not topics:
    st.error("找不到任何題庫，請確認 questions/ 資料夾中有 Markdown 題目檔案。")
    st.stop()

topic = st.selectbox("選擇主題", topics)

units = get_units(topic)
if not units:
    st.error(f"主題「{topic}」下找不到任何單元。")
    st.stop()

selected_units = st.multiselect(
    "選擇單元（可複選）",
    units,
    default=[units[0]] if units else []
)

st.subheader("選擇題數")
mode = st.radio("題數模式", ["全部題目", "隨機抽取 N 題"], horizontal=True)

random_n = None
if mode == "隨機抽取 N 題":
    random_n = st.number_input("抽取題數", min_value=1, max_value=200, value=10, step=1)

if st.button("開始測驗", type="primary", disabled=len(selected_units) == 0):
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
