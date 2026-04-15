import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import get_all_users, get_user_question_results, get_user_sessions
from utils.nav import render_sidebar
from utils.question_parser import QUESTIONS_DIR, load_questions_from_file
from utils.styles import inject_css

st.set_page_config(page_title="用戶管理", page_icon="📊", layout="wide")
inject_css()
render_sidebar()


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


# ── 頁首 ──
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#1E1B4B 0%,#4F46E5 100%);
                border-radius:14px;padding:1.4rem 1.8rem;margin-bottom:1.5rem;
                display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="font-size:1.15rem;font-weight:800;color:white;margin-bottom:0.2rem;">
          📊 用戶管理
        </div>
        <div style="color:rgba(255,255,255,0.6);font-size:0.78rem;">
          查看測驗記錄與弱點診斷分析
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

users = get_all_users()
if not users:
    st.info("目前尚無任何用戶紀錄。請先至首頁進行測驗。")
    st.stop()

# ── 選擇用戶 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
        "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
        unsafe_allow_html=True,
    )
    section_header("👤", "選擇用戶")
    user_options = {u["name"]: u["id"] for u in users}
    selected_name = st.selectbox(
        "用戶",
        list(user_options.keys()),
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

user_id = user_options[selected_name]
sessions = get_user_sessions(user_id)
question_results = get_user_question_results(user_id)

# ── 統計概覽 ──
if sessions:
    total_sessions = len(sessions)
    avg_accuracy = (
        sum(s["correct_count"] / s["total_questions"] * 100
            for s in sessions if s["total_questions"] > 0)
        / total_sessions
    )
    total_q_done = sum(s["total_questions"] for s in sessions)
    best_score = max(
        (s["correct_count"] / s["total_questions"] * 100
         for s in sessions if s["total_questions"] > 0),
        default=0,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("測驗次數", f"{total_sessions} 次")
    with c2:
        st.metric("平均答對率", f"{avg_accuracy:.1f}%")
    with c3:
        st.metric("累計作答題數", f"{total_q_done} 題")
    with c4:
        st.metric("最高答對率", f"{best_score:.1f}%")
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

# ── 測驗紀錄 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
        "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
        unsafe_allow_html=True,
    )
    section_header("📋", "測驗紀錄")

    if not sessions:
        st.info("此用戶尚無測驗紀錄。")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    session_rows = []
    for s in sessions:
        acc = s["correct_count"] / s["total_questions"] * 100 if s["total_questions"] > 0 else 0
        units_str = "、".join(s["units"]) if isinstance(s["units"], list) else s["units"]
        session_rows.append({
            "日期": s["taken_at"][:16].replace("T", " "),
            "主題": s["topic"],
            "單元": units_str,
            "答對": s["correct_count"],
            "總題數": s["total_questions"],
            "答對率 (%)": round(acc, 1),
        })

    st.dataframe(pd.DataFrame(session_rows), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── 趨勢圖 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
        "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
        unsafe_allow_html=True,
    )
    section_header("📈", "答對率趨勢")

    if len(sessions) >= 2:
        trend_data = pd.DataFrame({
            "測驗次序": list(range(1, len(session_rows) + 1)),
            "答對率 (%)": [r["答對率 (%)"] for r in reversed(session_rows)],
            "日期": [r["日期"] for r in reversed(session_rows)],
        })
        fig = px.line(
            trend_data, x="測驗次序", y="答對率 (%)",
            markers=True, hover_data=["日期"],
            labels={"測驗次序": "測驗次序", "答對率 (%)": "答對率 (%)"},
        )
        fig.update_yaxes(range=[0, 105])
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="Inter", title_font_size=13,
            margin=dict(l=10, r=10, t=20, b=20), showlegend=False,
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#F1F5F9")
        fig.update_traces(line_color="#4F46E5", marker_color="#4F46E5", line_width=2.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        if session_rows:
            st.metric("最近一次答對率", f"{session_rows[0]['答對率 (%)']:.1f}%")
        st.caption("需要 2 次以上測驗紀錄才能顯示趨勢圖。")

    st.markdown("</div>", unsafe_allow_html=True)

# ── 弱點診斷 ──
with st.container():
    st.markdown(
        "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
        "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
        unsafe_allow_html=True,
    )
    section_header("🔍", "弱點診斷")

    if not question_results:
        st.info("尚無題目作答紀錄，完成測驗後即可查看弱點分析。")
    else:
        # 各單元統計
        unit_correct: dict[str, int] = defaultdict(int)
        unit_total: dict[str, int] = defaultdict(int)
        for r in question_results:
            key = r["unit"]
            unit_total[key] += 1
            if r["is_correct"]:
                unit_correct[key] += 1

        unit_acc = {
            u: unit_correct[u] / unit_total[u] * 100
            for u in unit_total
            if unit_total[u] >= 3
        }

        if not unit_acc:
            st.caption("作答題數尚不足以進行分析（每單元需至少 3 題）。")
        else:
            weak = {u: a for u, a in unit_acc.items() if a < 60}
            mid  = {u: a for u, a in unit_acc.items() if 60 <= a < 80}
            good = {u: a for u, a in unit_acc.items() if a >= 80}

            col_l, col_r = st.columns([1, 1])

            with col_l:
                # 需加強
                if weak:
                    st.markdown(
                        """
                        <div style="background:#FFF5F5;border-radius:10px;padding:1rem 1.1rem;
                                    border:1px solid #FED7D7;margin-bottom:0.8rem;">
                          <div style="font-weight:700;color:#C53030;font-size:0.82rem;margin-bottom:0.6rem;">
                            🔴 需要加強
                          </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for u, a in sorted(weak.items(), key=lambda x: x[1]):
                        st.markdown(
                            f"""
                            <div style="display:flex;justify-content:space-between;
                                        align-items:center;padding:0.3rem 0;
                                        border-bottom:1px solid #FED7D7;">
                              <span style="font-size:0.82rem;color:#374151;">{u}</span>
                              <span style="font-weight:700;color:#EF4444;font-size:0.85rem;">{a:.1f}%</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

                # 尚可
                if mid:
                    st.markdown(
                        """
                        <div style="background:#FFFBEB;border-radius:10px;padding:1rem 1.1rem;
                                    border:1px solid #FDE68A;margin-bottom:0.8rem;">
                          <div style="font-weight:700;color:#92400E;font-size:0.82rem;margin-bottom:0.6rem;">
                            🟡 尚可，可繼續加強
                          </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for u, a in sorted(mid.items(), key=lambda x: x[1]):
                        st.markdown(
                            f"""
                            <div style="display:flex;justify-content:space-between;
                                        align-items:center;padding:0.3rem 0;
                                        border-bottom:1px solid #FDE68A;">
                              <span style="font-size:0.82rem;color:#374151;">{u}</span>
                              <span style="font-weight:700;color:#F59E0B;font-size:0.85rem;">{a:.1f}%</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                # 掌握良好
                if good:
                    st.markdown(
                        """
                        <div style="background:#F0FDF4;border-radius:10px;padding:1rem 1.1rem;
                                    border:1px solid #BBF7D0;margin-bottom:0.8rem;">
                          <div style="font-weight:700;color:#166534;font-size:0.82rem;margin-bottom:0.6rem;">
                            🟢 掌握良好
                          </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for u, a in sorted(good.items(), key=lambda x: x[1], reverse=True):
                        st.markdown(
                            f"""
                            <div style="display:flex;justify-content:space-between;
                                        align-items:center;padding:0.3rem 0;
                                        border-bottom:1px solid #BBF7D0;">
                              <span style="font-size:0.82rem;color:#374151;">{u}</span>
                              <span style="font-weight:700;color:#10B981;font-size:0.85rem;">{a:.1f}%</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

                # 強化建議
                if weak or mid:
                    priority = list(sorted(weak.items(), key=lambda x: x[1]))
                    priority += list(sorted(mid.items(), key=lambda x: x[1]))
                    suggestions = [u for u, _ in priority[:3]]
                    suggestion_text = "、".join(suggestions)

                    st.markdown(
                        f"""
                        <div style="background:#EEF2FF;border-radius:10px;padding:1rem 1.1rem;
                                    border:1px solid #C7D2FE;">
                          <div style="font-weight:700;color:#3730A3;font-size:0.82rem;margin-bottom:0.6rem;">
                            💡 強化建議
                          </div>
                          <div style="font-size:0.8rem;color:#374151;line-height:1.7;">
                            建議優先複習 <strong>{suggestion_text}</strong> 等單元。<br>
                            可至首頁單獨選取這些單元進行針對性練習，
                            透過多次重複練習提升答對率。
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.markdown("</div>", unsafe_allow_html=True)

# ── 各單元答對率圖 ──
if question_results:
    with st.container():
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
            "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
            unsafe_allow_html=True,
        )
        section_header("📊", "各單元答對率")

        u_correct: dict[str, int] = defaultdict(int)
        u_total: dict[str, int] = defaultdict(int)
        for r in question_results:
            key = f"{r['topic']} / {r['unit']}"
            u_total[key] += 1
            if r["is_correct"]:
                u_correct[key] += 1

        unit_rows = [
            {
                "單元": k,
                "答對率 (%)": round(u_correct[k] / u_total[k] * 100, 1),
                "答對題數": u_correct[k],
                "總作答次數": u_total[k],
            }
            for k in u_total
        ]
        df_units = pd.DataFrame(unit_rows).sort_values("答對率 (%)")

        fig_bar = px.bar(
            df_units, x="答對率 (%)", y="單元",
            orientation="h", text="答對率 (%)",
            color="答對率 (%)",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_color=[0, 100],
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_bar.update_xaxes(range=[0, 115])
        fig_bar.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="Inter", title_font_size=13,
            margin=dict(l=10, r=10, t=20, b=20),
            coloraxis_showscale=False,
        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(gridcolor="#F1F5F9")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── 高頻錯題 ──
if question_results:
    with st.container():
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:1.2rem 1.4rem;"
            "border:1px solid #E2E8F0;margin-bottom:1.2rem;'>",
            unsafe_allow_html=True,
        )
        section_header("❌", "高頻錯題 Top 10")

        wrong_counts: dict[str, int] = defaultdict(int)
        for r in question_results:
            if not r["is_correct"]:
                wrong_counts[r["question_id"]] += 1

        if not wrong_counts:
            st.success("目前沒有答錯的題目！")
        else:
            all_qs: dict[str, dict] = {}
            if QUESTIONS_DIR.exists():
                for td in QUESTIONS_DIR.iterdir():
                    if td.is_dir():
                        for mf in td.glob("*.md"):
                            for q in load_questions_from_file(mf, td.name):
                                all_qs[q["id"]] = q

            top_wrong = sorted(wrong_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            rows = []
            for qid, cnt in top_wrong:
                q = all_qs.get(qid)
                text = (
                    q["question"][:60] + "..." if q and len(q["question"]) > 60
                    else (q["question"] if q else qid)
                )
                rows.append({"題目": text, "答錯次數": cnt})

            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)
