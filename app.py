import streamlit as st
from pathlib import Path
import sys

# Add interviewer module to path
sys.path.insert(0, str(Path(__file__).parent))

from streamlit_app.config import load_sidebar_config, initialize_session_state
from streamlit_app.ui import render_interview_header, render_interview_interface
from streamlit_app.report import render_report

# Page config
st.set_page_config(
    page_title="AI Assistance Interviewer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎤 AI Assistance Interviewer")

# Initialize session state
initialize_session_state()

# Load sidebar configuration
config = load_sidebar_config()

# Render interview header
render_interview_header(config["template"])

# Render interview interface
render_interview_interface(config, config["template"])

# Render report if interview is complete
if st.session_state.interview_complete and st.session_state.report:
    render_report(st.session_state.report)
