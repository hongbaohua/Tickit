import streamlit as st


def inject_css():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

        <style>
        /* ── 全域字型 ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── 背景 ── */
        .stApp {
            background-color: #F0F4FF !important;
        }

        /* ── 隱藏 Streamlit 預設 UI ── */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }

        /* ── 按鈕 ── */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
            border: none !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 16px rgba(79, 70, 229, 0.3) !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
            color: white !important;
        }
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #4F46E5 !important;
            border: 2px solid #E2E8F0 !important;
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: #4F46E5 !important;
            background: #EEF2FF !important;
        }

        /* ── 文字輸入 ── */
        .stTextInput input,
        .stNumberInput input {
            border-radius: 10px !important;
            border: 2px solid #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            background: white !important;
        }
        .stTextInput input:focus,
        .stNumberInput input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
        }

        /* ── Selectbox / Multiselect ── */
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            border-radius: 10px !important;
            border: 2px solid #E2E8F0 !important;
            background: white !important;
            transition: border-color 0.2s ease !important;
        }
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: #4F46E5 !important;
        }

        /* ── Radio ── */
        .stRadio > div {
            gap: 0.5rem !important;
        }
        .stRadio label {
            background: white !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            transition: border-color 0.2s ease, background 0.2s ease !important;
            cursor: pointer !important;
            font-family: 'Inter', sans-serif !important;
        }
        .stRadio label:hover {
            border-color: #4F46E5 !important;
            background: #EEF2FF !important;
        }
        [data-baseweb="radio"] input:checked + div + span,
        .stRadio label[data-selected="true"] {
            border-color: #4F46E5 !important;
            background: #EEF2FF !important;
        }

        /* ── Progress bar ── */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #4F46E5, #818CF8) !important;
            border-radius: 999px !important;
        }
        .stProgress > div > div > div {
            background: #E2E8F0 !important;
            border-radius: 999px !important;
        }

        /* ── Metric 卡片 ── */
        [data-testid="metric-container"] {
            background: white !important;
            border-radius: 16px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06) !important;
            padding: 1rem 1.2rem !important;
        }
        [data-testid="metric-container"] label {
            font-weight: 600 !important;
            color: #64748B !important;
            font-size: 0.82rem !important;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: #1E1B4B !important;
            font-weight: 800 !important;
        }

        /* ── Alert ── */
        .stAlert {
            border-radius: 12px !important;
        }

        /* ── 分隔線 ── */
        hr {
            border-color: #E2E8F0 !important;
            margin: 1.2rem 0 !important;
        }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            color: #1E1B4B !important;
        }
        .streamlit-expanderHeader:hover {
            color: #4F46E5 !important;
        }

        /* ── Dataframe ── */
        .stDataFrame {
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid #E2E8F0 !important;
        }

        /* ── 主內容區 padding ── */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 720px !important;
        }

        /* ── wide layout（dashboard）── */
        [data-testid="stAppViewContainer"] .block-container[data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
