import streamlit as st


def inject_css():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
              rel="stylesheet">

        <style>
        /* ── 全域字型 ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── 背景 ── */
        .stApp { background-color: #F8FAFF !important; }
        section[data-testid="stSidebar"] { background: white !important; border-right: 1px solid #E2E8F0; }

        /* ── 隱藏預設頁面導航 ── */
        [data-testid="stSidebarNavItems"]    { display: none !important; }
        [data-testid="stSidebarNavSeparator"]{ display: none !important; }
        #MainMenu { visibility: hidden; }
        footer    { visibility: hidden; }
        header    { visibility: hidden; }
        [data-testid="stToolbar"]   { display: none; }
        [data-testid="stDecoration"]{ display: none; }

        /* ── 側欄 page_link ── */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
            background: transparent !important;
            border-radius: 8px !important;
            color: #374151 !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 0.6rem !important;
            margin-bottom: 2px !important;
            transition: background 0.15s ease, color 0.15s ease !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
            background: #EEF2FF !important;
            color: #4F46E5 !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: #EEF2FF !important;
            color: #4F46E5 !important;
            font-weight: 700 !important;
        }

        /* ── 按鈕 ── */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.18s ease !important;
            border: none !important;
            font-size: 0.88rem !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(79,70,229,0.25) !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg,#4F46E5 0%,#6366F1 100%) !important;
            color: white !important;
        }
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #4F46E5 !important;
            border: 1.5px solid #C7D2FE !important;
        }

        /* ── 文字輸入 ── */
        .stTextInput input, .stNumberInput input {
            border-radius: 8px !important;
            border: 1.5px solid #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            background: white !important;
            font-size: 0.9rem !important;
            transition: border-color 0.15s, box-shadow 0.15s !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
        }

        /* ── Selectbox / Multiselect ── */
        .stSelectbox > div > div, .stMultiSelect > div > div {
            border-radius: 8px !important;
            border: 1.5px solid #E2E8F0 !important;
            background: white !important;
        }
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: #4F46E5 !important;
        }

        /* ── Radio ── */
        .stRadio > div { gap: 0.4rem !important; }
        .stRadio label {
            background: white !important;
            border: 1.5px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 11px 15px !important;
            transition: border-color 0.15s, background 0.15s !important;
            cursor: pointer !important;
        }
        .stRadio label:hover {
            border-color: #4F46E5 !important;
            background: #F5F3FF !important;
        }

        /* ── Progress bar ── */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg,#4F46E5,#818CF8) !important;
            border-radius: 999px !important;
        }
        .stProgress > div > div > div {
            background: #E2E8F0 !important;
            border-radius: 999px !important;
        }

        /* ── Metric ── */
        [data-testid="metric-container"] {
            background: white !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
            padding: 1rem 1.1rem !important;
        }
        [data-testid="metric-container"] label {
            font-weight: 600 !important;
            color: #64748B !important;
            font-size: 0.78rem !important;
        }
        [data-testid="stMetricValue"] {
            color: #1E1B4B !important;
            font-weight: 800 !important;
        }

        /* ── Alert / Info ── */
        .stAlert { border-radius: 10px !important; }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #1E1B4B !important;
        }

        /* ── Dataframe ── */
        .stDataFrame {
            border-radius: 10px !important;
            overflow: hidden !important;
            border: 1px solid #E2E8F0 !important;
        }

        /* ── 主內容 padding ── */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 740px !important;
        }

        /* ── wide layout（dashboard）── */
        [data-testid="stAppViewContainer"]
            .block-container[data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
        }

        hr { border-color: #E2E8F0 !important; margin: 1rem 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
