# app.py
import os
from pathlib import Path
from PIL import Image
import streamlit as st

from ui import login_page, recruiter_dashboard, candidate_dashboard

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
current_dir = Path(__file__).resolve().parent
logo_path = current_dir / "ui" / "logo.png"

if logo_path.exists():
    page_icon_img = Image.open(logo_path)
else:
    page_icon_img = "💼"

st.set_page_config(
    page_title="CareerConnect",
    page_icon=page_icon_img,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# DASHBOARD STYLING
# --------------------------------------------------
def apply_custom_styling():
    st.markdown(
        """
        <style>
        .stApp { background-color: #F8FAFC !important; }
        [data-testid="stAppViewContainer"] { color: #0F172A; }
        
        section[data-testid="stSidebar"] { background-color: #1E293B !important; }
        section[data-testid="stSidebar"] * { color: #F8FAFC !important; }
        
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"] > div,
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 6px !important;
        }
        
        div[data-baseweb="select"] * {
            background-color: transparent !important;
            color: #0F172A !important;
        }
        div[data-baseweb="select"] svg { fill: #0F172A !important; }
        
        input, textarea {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            caret-color: #000000 !important;
        }
        
        ul[data-baseweb="menu"] {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
        }
        ul[data-baseweb="menu"] li {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
        }
        ul[data-baseweb="menu"] li:hover { background-color: #F1F5F9 !important; }
        
        details[data-testid="stExpander"] {
            background-color: #ffffff !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }
        details[data-testid="stExpander"] summary {
            background-color: #ffffff !important;
            color: #0F172A !important;
        }
        details[data-testid="stExpander"] summary:hover { background-color: #F1F5F9 !important; }
        details[data-testid="stExpander"] summary svg { fill: #0F172A !important; }
        
        .stButton > button {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.5rem 1.5rem !important;
        }
        .stButton > button:hover {
            background-color: #1D4ED8 !important;
            color: #FFFFFF !important;
        }
        .stButton > button p { color: #FFFFFF !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
def logout():
    st.session_state.clear()

# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page.show()
        return

    user = st.session_state.get("user_data")
    if user is None:
        user = st.session_state.get("user")

    if not user:
        st.session_state.clear()
        st.session_state["logged_in"] = False
        st.rerun()
        return

    apply_custom_styling()
    role = user.get("role")

    if role == "recruiter":
        recruiter_dashboard.show()

    elif role == "candidate":
        candidate_dashboard.show()

    else:
        st.error("Your account role is missing or invalid. Please sign in again.")
        st.button("Return to Login", on_click=logout)

if __name__ == "__main__":
    main()