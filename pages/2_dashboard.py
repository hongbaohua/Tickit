import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import get_all_users, get_user_sessions, get_user_question_results
from utils.question_parser import load_questions_from_file, QUESTIONS_DIR
from utils.styles import inject_css

st.set_page_config(page_title="考生管理", page_icon="📊", layout="wide")

inject_css()

# ── Hero Banner（小版）──
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #4F46E5 100%);
                border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;">
      <h2 style="color:white; margin:0; font-size:1.3rem; font-weight:800;">📊 考生成績分析</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

users = get_all_users()
if not users:
    st.info("目前尚無任何考生紀錄。請先至首頁進行測驗。")
    st.stop()

user_options = {u["name"]: u["id"] for u in users}
selected_name = st.selectbox("選擇考生", list(user_options.keys()))
user_id = user_options[selected_name]

sessions = get_user_sessions(user_id)
question_results = get_user_question_results(user_id)

# ── 統計概覽 Metrics ──
if sessions:
    total_sessions = len(sessions)
    avg_accuracy = sum(
        s["correct_count"] / s["total_questions"] * 100
        for s in sessions if s["total_questions"] > 0
    ) / total_sessions if total_sessions > 0 else 0
    total_questions_done = sum(s["total_questions"] for s in sessions)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("測驗次數", f"{total_sessions} 次")
    with col_m2:
        st.metric("平均答對率", f"{avg_accuracy:.1f}%")
    with col_m3:
        st.metric("累計作答題數", f"{total_questions_done} 題")

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

# ── 測驗紀錄 ──
st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:0 0 0.6rem;'>📋 測驗紀錄</p>",
    unsafe_allow_html=True,
)

if not sessions:
    st.info("此考生尚無測驗紀錄。")
    st.stop()

session_rows = []
for s in sessions:
    accuracy = s["correct_count"] / s["total_questions"] * 100 if s["total_questions"] > 0 else 0
    units_str = "、".join(s["units"]) if isinstance(s["units"], list) else s["units"]
    session_rows.append({
        "日期": s["taken_at"][:16].replace("T", " "),
        "主題": s["topic"],
        "單元": units_str,
        "答對題數": s["correct_count"],
        "總題數": s["total_questions"],
        "答對率 (%)": round(accuracy, 1),
    })

df_sessions = pd.DataFrame(session_rows)
st.dataframe(df_sessions, use_container_width=True, hide_index=True)

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

# ── 趨勢圖 ──
st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:0 0 0.6rem;'>📈 答對率趨勢</p>",
    unsafe_allow_html=True,
)

if len(sessions) >= 2:
    trend_data = pd.DataFrame({
        "測驗次序": list(range(1, len(session_rows) + 1)),
        "答對率 (%)": [r["答對率 (%)"] for r in reversed(session_rows)],
        "日期": [r["日期"] for r in reversed(session_rows)],
    })
    fig = px.line(
        trend_data,
        x="測驗次序",
        y="答對率 (%)",
        markers=True,
        hover_data=["日期"],
        title="歷次答對率趨勢",
        labels={"測驗次序": "測驗次序", "答對率 (%)": "答對率 (%)"},
    )
    fig.update_yaxes(range=[0, 105])
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Inter",
        title_font_size=14,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#F1F5F9")
    fig.update_traces(line_color="#4F46E5", marker_color="#4F46E5")
    st.plotly_chart(fig, use_container_width=True)
else:
    if session_rows:
        st.metric("最近一次答對率", f"{session_rows[0]['答對率 (%)']:.1f}%")
    st.caption("需要 2 次以上測驗紀錄才能顯示趨勢圖。")

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

# ── 答錯次數前 10 題 ──
st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:0 0 0.6rem;'>❌ 答錯次數前 10 題</p>",
    unsafe_allow_html=True,
)

if not question_results:
    st.info("尚無題目作答紀錄。")
else:
    wrong_counts: dict[str, int] = defaultdict(int)

    for r in question_results:
        if not r["is_correct"]:
            wrong_counts[r["question_id"]] += 1

    if not wrong_counts:
        st.success("目前沒有答錯的題目！")
    else:
        all_loaded_questions: dict[str, dict] = {}
        if QUESTIONS_DIR.exists():
            for topic_dir in QUESTIONS_DIR.iterdir():
                if topic_dir.is_dir():
                    for md_file in topic_dir.glob("*.md"):
                        qs = load_questions_from_file(md_file, topic_dir.name)
                        for q in qs:
                            all_loaded_questions[q["id"]] = q

        top_wrong = sorted(wrong_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        rows = []
        for qid, count in top_wrong:
            q = all_loaded_questions.get(qid)
            question_text = (
                q["question"][:60] + "..."
                if q and len(q["question"]) > 60
                else (q["question"] if q else qid)
            )
            rows.append({"題目": question_text, "答錯次數": count})

        df_wrong = pd.DataFrame(rows)
        st.dataframe(df_wrong, use_container_width=True, hide_index=True)

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

# ── 各單元答對率 ──
st.markdown(
    "<p style='font-size:1rem; font-weight:700; color:#1E1B4B; margin:0 0 0.6rem;'>📊 各單元答對率</p>",
    unsafe_allow_html=True,
)

if question_results:
    unit_correct: dict[str, int] = defaultdict(int)
    unit_total: dict[str, int] = defaultdict(int)

    for r in question_results:
        key = f"{r['topic']} / {r['unit']}"
        unit_total[key] += 1
        if r["is_correct"]:
            unit_correct[key] += 1

    unit_rows = []
    for key in unit_total:
        total_count = unit_total[key]
        correct_count = unit_correct[key]
        accuracy = correct_count / total_count * 100 if total_count > 0 else 0
        unit_rows.append({
            "單元": key,
            "答對率 (%)": round(accuracy, 1),
            "答對題數": correct_count,
            "總作答次數": total_count,
        })

    df_units = pd.DataFrame(unit_rows).sort_values("答對率 (%)")
    fig_bar = px.bar(
        df_units,
        x="答對率 (%)",
        y="單元",
        orientation="h",
        text="答對率 (%)",
        title="各單元答對率",
        color="答對率 (%)",
        color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
        range_color=[0, 100],
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_xaxes(range=[0, 115])
    fig_bar.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Inter",
        title_font_size=14,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(gridcolor="#F1F5F9")
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("尚無題目作答紀錄。")
