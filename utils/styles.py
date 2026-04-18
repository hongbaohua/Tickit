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
        .stApp { background-color: #F9FAFB !important; }

        /* ── Sidebar: white ── */
        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
        }

        /* ── Hide nav items / decoration / footer / menu ──
             NEVER touch stHeader — the collapsed control button lives inside it */
        [data-testid="stSidebarNavItems"]     { display: none !important; }
        [data-testid="stSidebarNavSeparator"] { display: none !important; }
        footer                                { visibility: hidden; }
        [data-testid="stDecoration"]          { display: none !important; }
        #MainMenu                             { display: none !important; }

        /* ── Sidebar collapsed control button: match white sidebar ── */
        [data-testid="stSidebarCollapsedControl"] {
            background: #FFFFFF !important;
            border-radius: 0 8px 8px 0 !important;
            border: 1px solid #E5E7EB !important;
            border-left: none !important;
            box-shadow: 2px 0 6px rgba(0,0,0,0.06) !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg {
            color: #6B7280 !important;
            fill: #6B7280 !important;
        }

        /* ── Sidebar page_link ── */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
            background: transparent !important;
            border-radius: 6px !important;
            color: #6B7280 !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            padding: 0.42rem 0.6rem !important;
            margin-bottom: 2px !important;
            transition: background 0.12s ease, color 0.12s ease !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
            background: #F3F4F6 !important;
            color: #111827 !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: #EEF2FF !important;
            color: #4F46E5 !important;
            font-weight: 600 !important;
        }

        /* ── Primary button ── */
        .stButton > button {
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: background 0.15s ease, border-color 0.15s ease !important;
            font-size: 0.875rem !important;
        }
        .stButton > button[kind="primary"] {
            background: #4F46E5 !important;
            color: white !important;
            border: none !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: #4338CA !important;
        }

        /* ── Secondary button ── */
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #374151 !important;
            border: 1.5px solid #D1D5DB !important;
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: #4F46E5 !important;
            color: #4F46E5 !important;
        }

        /* ── Text inputs ── */
        .stTextInput input, .stNumberInput input {
            border-radius: 6px !important;
            border: 1.5px solid #E5E7EB !important;
            font-family: 'Inter', sans-serif !important;
            background: white !important;
            font-size: 0.9rem !important;
            transition: border-color 0.15s !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
            outline: none !important;
        }

        /* ── Selectbox / Multiselect ── */
        .stSelectbox > div > div, .stMultiSelect > div > div {
            border-radius: 6px !important;
            border: 1.5px solid #E5E7EB !important;
            background: white !important;
        }
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
        }

        /* ── Radio options as white cards ── */
        .stRadio > div { gap: 0.35rem !important; }
        .stRadio label {
            background: white !important;
            border: 1.5px solid #E5E7EB !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
            transition: border-color 0.12s, background 0.12s !important;
            cursor: pointer !important;
        }
        .stRadio label:hover {
            border-color: #4F46E5 !important;
            background: #F5F3FF !important;
        }

        /* ── Progress bar ── */
        .stProgress > div > div > div > div {
            background: #4F46E5 !important;
            border-radius: 999px !important;
        }
        .stProgress > div > div > div {
            background: #E5E7EB !important;
            border-radius: 999px !important;
        }

        /* ── Metric cards ── */
        [data-testid="metric-container"] {
            background: white !important;
            border-radius: 8px !important;
            border: 1px solid #E5E7EB !important;
            padding: 1rem 1.1rem !important;
        }
        [data-testid="metric-container"] label {
            font-weight: 600 !important;
            color: #6B7280 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        [data-testid="stMetricValue"] {
            color: #111827 !important;
            font-weight: 800 !important;
        }

        /* ── Alert ── */
        .stAlert { border-radius: 6px !important; }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #111827 !important;
        }

        /* ── Dataframe ── */
        .stDataFrame {
            border-radius: 6px !important;
            overflow: hidden !important;
            border: 1px solid #E5E7EB !important;
        }

        /* ── Main content block ── */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 740px !important;
        }

        /* ── Wide layout (dashboard) override ── */
        [data-testid="stAppViewContainer"]
            .block-container[data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
        }

        hr { border-color: #F3F4F6 !important; margin: 1rem 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
