import streamlit as st


def render_sidebar():
    with st.sidebar:
        # ── Brand mark ──
        st.markdown(
            """
            <div style="padding:1.2rem 0.2rem 0.8rem;">
              <div style="display:flex;align-items:center;gap:0.75rem;">
                <span style="font-size:1.5rem;line-height:1;">📝</span>
                <div>
                  <div style="font-weight:800;color:#FFFFFF;font-size:0.92rem;
                              line-height:1.3;letter-spacing:-0.2px;">線上測驗平台</div>
                  <div style="color:#64748B;font-size:0.62rem;letter-spacing:1.5px;
                              text-transform:uppercase;margin-top:1px;">Quiz System</div>
                </div>
              </div>
            </div>
            <div style="height:1px;
                        background:linear-gradient(90deg,rgba(255,255,255,0.18) 0%,transparent 100%);
                        margin-bottom:0.9rem;"></div>
            """,
            unsafe_allow_html=True,
        )

        # ── Navigation links ──
        st.page_link("app.py",            label="首頁",   icon="🏠")
        st.page_link("pages/1_quiz.py",   label="測驗進行", icon="📋")
        st.page_link("pages/2_dashboard.py", label="用戶管理", icon="📊")

        # ── Logged-in user card ──
        if st.session_state.get("user_name"):
            st.markdown(
                "<div style='height:1px;"
                "background:linear-gradient(90deg,rgba(255,255,255,0.12) 0%,transparent 100%);"
                "margin:1rem 0 0.9rem;'></div>",
                unsafe_allow_html=True,
            )
            first = st.session_state.user_name[0].upper()
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:0.65rem;
                            background:rgba(255,255,255,0.08);border-radius:10px;
                            padding:0.6rem 0.75rem;border:1px solid rgba(255,255,255,0.10);">
                  <div style="width:30px;height:30px;border-radius:50%;
                              background:#6366F1;
                              display:flex;align-items:center;justify-content:center;
                              color:white;font-weight:700;font-size:0.78rem;flex-shrink:0;">
                    {first}
                  </div>
                  <div>
                    <div style="font-weight:600;color:#FFFFFF;font-size:0.82rem;line-height:1.3;">
                      {st.session_state.user_name}
                    </div>
                    <div style="color:#64748B;font-size:0.63rem;margin-top:1px;">已登入</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
