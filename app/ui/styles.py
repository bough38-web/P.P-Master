import streamlit as st

def apply_styles():
    """
    Enterprise Professional UI v7.0.
    Focused on 'Quiet Luxury' - clean, sober, and highly functional.
    Eliminates excessive decorations for a mature business feel.
    """
    st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    /* Reset to Professional Baseline */
    * {
        font-family: 'Pretendard', -apple-system, sans-serif !important;
        letter-spacing: -0.01em;
    }

    .stApp {
        background-color: #fcfcfc;
    }

    /* Professional Dashboard Container */
    .main .block-container {
        max-width: 1200px !important;
        padding-top: 3rem !important;
    }

    /* Bento Card - Sober Style */
    .premium-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid #edf2f7;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Insight Result Box - Muted & Serious */
    .insight-header {
        background: #1a202c; /* Deep Slate Navy */
        border-radius: 20px;
        padding: 3rem 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid #2d3748;
    }

    .pp-value {
        font-size: 4.5rem; /* Reduced from excessive 8rem */
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.1;
        margin: 0.5rem 0;
        color: #ffffff;
    }

    .approver-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #a0aec0;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .status-badge {
        background: rgba(72, 187, 120, 0.15);
        color: #68d391;
        padding: 8px 16px;
        border-radius: 100px;
        font-size: 1rem;
        font-weight: 700;
        display: inline-block;
        border: 1px solid rgba(72, 187, 120, 0.3);
        margin-top: 1rem;
    }

    /* Buttons - Clean Solid Style */
    .stButton > button {
        border-radius: 8px !important;
        background: #ffffff !important;
        color: #2d3748 !important;
        border: 1px solid #e2e8f0 !important;
        font-weight: 600 !important;
        height: 44px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #f7fafc !important;
        border-color: #cbd5e0 !important;
        color: #1a202c !important;
        transform: none !important; /* Remove excessive jump */
    }

    /* Mode Selection Active Style */
    [data-testid="stBaseButton-secondary"]:active, [data-testid="stBaseButton-secondary"]:focus {
        border-color: #3182ce !important;
        color: #3182ce !important;
    }

    /* Sidebar - Corporate Clean */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #edf2f7;
    }

    /* Clean Inputs */
    input, select, .stSelectbox div {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    /* Hide UI noise */
    [data-testid="stHeader"], [data-testid="stFooter"], #MainMenu { display: none !important; }

    /* Compact Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #cbd5e0; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)
