import streamlit as st
import yaml


def load_sidebar_config():
    """Load all configuration from sidebar"""
    st.sidebar.header("⚙️ Configuration")
    
    # API Keys
    st.sidebar.subheader("API Keys")
    groq_api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        help="Get your key from https://console.groq.com"
    )
    
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Get your key from https://platform.openai.com"
    )
    
    # LLM Selection
    st.sidebar.subheader("LLM Selection")
    llm_choice = st.sidebar.selectbox(
        "Choose LLM Provider",
        ["Groq", "OpenAI"],
        help="Select which LLM to use for interview"
    )
    
    # Model selection based on LLM choice
    if llm_choice == "Groq":
        groq_models = ["llama-3.1-8b-instant", "Gemma2-9b-It", "mixtral-8x7b-32768"]
        selected_model = st.sidebar.selectbox("Groq Model", groq_models)
        if not groq_api_key:
            st.sidebar.warning("⚠️ Groq API key is required")
    else:
        openai_models = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]
        selected_model = st.sidebar.selectbox("OpenAI Model", openai_models)
        if not openai_api_key:
            st.sidebar.warning("⚠️ OpenAI API key is required")
    
    # Interview settings
    st.sidebar.subheader("Interview Settings")
    max_followups = st.sidebar.slider("Max Follow-ups per Question", 0, 3, 1)
    
    # Load template
    st.sidebar.subheader("Interview Template")
    template_file = st.sidebar.selectbox(
        "Select Template",
        ["AI_engineer.yaml"]
    )
    
    try:
        with open(f"templates/{template_file}", "r") as f:
            template = yaml.safe_load(f)
    except Exception as e:
        st.sidebar.error(f"Error loading template: {e}")
        st.stop()
    
    return {
        "groq_api_key": groq_api_key,
        "openai_api_key": openai_api_key,
        "llm_choice": llm_choice,
        "selected_model": selected_model,
        "max_followups": max_followups,
        "template": template
    }


def initialize_session_state():
    """Initialize all session state variables"""
    if "session" not in st.session_state:
        st.session_state.session = None
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "session_store" not in st.session_state:
        st.session_state.session_store = {}
    if "report" not in st.session_state:
        st.session_state.report = None
    if "interview_complete" not in st.session_state:
        st.session_state.interview_complete = False
    if "followup_count" not in st.session_state:
        st.session_state.followup_count = 0
    if "max_followups_value" not in st.session_state:
        st.session_state.max_followups_value = 1
