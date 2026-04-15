import streamlit as st


def inject_css():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
              rel="stylesheet">

        <style>
        /* ── Global font ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Page background ── */
        .stApp { background-color: #F8FAFC !important; }

        /* ── Sidebar: dark slate ── */
        section[data-testid="stSidebar"] {
            background: #1E293B !important;
            border-right: none !important;
        }

        /* ── Hide only nav items / decoration / footer / menu ──
             NEVER touch stHeader — the collapsed control button lives inside it */
        [data-testid="stSidebarNavItems"]     { display: none !important; }
        [data-testid="stSidebarNavSeparator"] { display: none !important; }
        footer                                { visibility: hidden; }
        [data-testid="stDecoration"]          { display: none !important; }
        #MainMenu                             { display: none !important; }

        /* ── Sidebar collapsed control button ── */
        [data-testid="stSidebarCollapsedControl"] {
            background: #1E293B !important;
            border-radius: 0 8px 8px 0 !important;
            border: 1px solid #334155 !important;
            border-left: none !important;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.18) !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg {
            color: #CBD5E1 !important;
            fill: #CBD5E1 !important;
        }

        /* ── Sidebar page_link: light text on dark bg ── */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
            background: transparent !important;
            border-radius: 8px !important;
            color: #CBD5E1 !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 0.6rem !important;
            margin-bottom: 2px !important;
            transition: background 0.15s ease, color 0.15s ease !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
            background: rgba(255,255,255,0.08) !important;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: rgba(99,102,241,0.25) !important;
            color: #A5B4FC !important;
            font-weight: 700 !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.18s ease !important;
            font-size: 0.88rem !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(99,102,241,0.28) !important;
        }
        .stButton > button[kind="primary"] {
            background: #6366F1 !important;
            color: white !important;
            border: none !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: #4F46E5 !important;
        }
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #374151 !important;
            border: 1.5px solid #D1D5DB !important;
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: #6366F1 !important;
            color: #6366F1 !important;
        }

        /* ── Text inputs ── */
        .stTextInput input, .stNumberInput input {
            border-radius: 8px !important;
            border: 1.5px solid #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            background: white !important;
            font-size: 0.9rem !important;
            transition: border-color 0.15s, box-shadow 0.15s !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
            outline: none !important;
        }

        /* ── Selectbox / Multiselect ── */
        .stSelectbox > div > div, .stMultiSelect > div > div {
            border-radius: 8px !important;
            border: 1.5px solid #E2E8F0 !important;
            background: white !important;
        }
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
        }

        /* ── Radio options as white cards ── */
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
            border-color: #6366F1 !important;
            background: #F5F3FF !important;
        }

        /* ── Progress bar ── */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #6366F1, #818CF8) !important;
            border-radius: 999px !important;
        }
        .stProgress > div > div > div {
            background: #E2E8F0 !important;
            border-radius: 999px !important;
        }

        /* ── Metric cards ── */
        [data-testid="metric-container"] {
            background: white !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
            padding: 1rem 1.1rem !important;
        }
        [data-testid="metric-container"] label {
            font-weight: 600 !important;
            color: #64748B !important;
            font-size: 0.78rem !important;
        }
        [data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-weight: 800 !important;
        }

        /* ── Alert ── */
        .stAlert { border-radius: 10px !important; }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #1E293B !important;
        }

        /* ── Dataframe ── */
        .stDataFrame {
            border-radius: 10px !important;
            overflow: hidden !important;
            border: 1px solid #E2E8F0 !important;
        }

        /* ── Main content block ── */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 720px !important;
        }

        /* ── Wide layout (dashboard) override ── */
        [data-testid="stAppViewContainer"]
            .block-container[data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
        }

        hr { border-color: #E2E8F0 !important; margin: 1rem 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
