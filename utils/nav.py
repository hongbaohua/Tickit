import streamlit as st


def render_sidebar():
    with st.sidebar:
        # ── Brand mark ──
        st.markdown(
            """
            <div style="padding: 1.4rem 0.4rem 1rem;">
              <div style="display:flex; align-items:center; gap:0.75rem;">
                <div style="width:28px;height:28px;background:#4F46E5;border-radius:5px;
                            display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <div style="width:12px;height:12px;border:2px solid white;border-radius:2px;"></div>
                </div>
                <div>
                  <div style="font-weight:800;color:#111827;font-size:0.88rem;letter-spacing:-0.2px;">線上測驗平台</div>
                  <div style="font-size:0.62rem;color:#9CA3AF;letter-spacing:1px;text-transform:uppercase;margin-top:1px;">Quiz System</div>
                </div>
              </div>
            </div>
            <div style="height:1px;background:#F3F4F6;margin-bottom:0.75rem;"></div>
            """,
            unsafe_allow_html=True,
        )

        # ── Nav section label ──
        st.markdown(
            """
            <div style="font-size:0.65rem;font-weight:700;color:#9CA3AF;letter-spacing:1px;
                        text-transform:uppercase;padding:0 0.5rem;margin-bottom:0.4rem;">
              導覽
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Navigation links (no icon parameter) ──
        st.page_link("app.py",                  label="首頁")
        st.page_link("pages/1_quiz.py",         label="測驗進行")
        st.page_link("pages/2_dashboard.py",    label="用戶管理")

        # ── Logged-in user card ──
        if st.session_state.get("user_name"):
            st.markdown(
                "<div style='height:1px;background:#F3F4F6;margin:1rem 0 0.9rem;'></div>",
                unsafe_allow_html=True,
            )
            first = st.session_state.user_name[0].upper()
            name  = st.session_state.user_name
            st.markdown(
                f"""
                <div style="background:#F9FAFB;border-radius:8px;padding:0.6rem 0.75rem;
                            border:1px solid #E5E7EB;display:flex;align-items:center;gap:0.6rem;">
                  <div style="width:28px;height:28px;border-radius:4px;background:#4F46E5;
                              display:flex;align-items:center;justify-content:center;
                              color:white;font-weight:700;font-size:0.75rem;flex-shrink:0;">
                    {first}
                  </div>
                  <div>
                    <div style="font-weight:600;color:#111827;font-size:0.8rem;">{name}</div>
                    <div style="font-size:0.62rem;color:#9CA3AF;margin-top:1px;">已登入</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
