import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:1rem 0 0.8rem;">
              <div style="display:flex;align-items:center;gap:0.7rem;">
                <span style="font-size:1.5rem;">📝</span>
                <div>
                  <div style="font-weight:800;color:#1E1B4B;font-size:0.9rem;line-height:1.3;">線上測驗平台</div>
                  <div style="color:#94A3B8;font-size:0.65rem;letter-spacing:1px;">QUIZ SYSTEM</div>
                </div>
              </div>
            </div>
            <div style="height:2px;background:linear-gradient(90deg,#4F46E5 0%,#E2E8F0 100%);
                        border-radius:2px;margin-bottom:1rem;"></div>
            """,
            unsafe_allow_html=True,
        )

        st.page_link("app.py", label="首頁", icon="🏠")
        st.page_link("pages/1_quiz.py", label="測驗進行", icon="📋")
        st.page_link("pages/2_dashboard.py", label="用戶管理", icon="📊")

        if st.session_state.get("user_name"):
            st.markdown(
                "<div style='height:1px;background:#E2E8F0;margin:1rem 0 0.8rem;'></div>",
                unsafe_allow_html=True,
            )
            first = st.session_state.user_name[0].upper()
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:0.6rem;
                            background:#F0F4FF;border-radius:10px;
                            padding:0.55rem 0.7rem;border:1px solid #E2E8F0;">
                  <div style="width:28px;height:28px;border-radius:50%;
                              background:linear-gradient(135deg,#4F46E5,#818CF8);
                              display:flex;align-items:center;justify-content:center;
                              color:white;font-weight:700;font-size:0.78rem;flex-shrink:0;">
                    {first}
                  </div>
                  <div>
                    <div style="font-weight:600;color:#0F172A;font-size:0.8rem;line-height:1.3;">
                      {st.session_state.user_name}
                    </div>
                    <div style="color:#94A3B8;font-size:0.65rem;">已登入</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
