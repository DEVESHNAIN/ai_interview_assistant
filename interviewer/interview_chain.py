from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your .env file.")

# Session storage for conversation history
session_store = {}

def build_interview_chain():
    prompt = PromptTemplate(
        template="""
You are a technical interviewer conducting a {role} interview.

Rules:
- Ask ONE question at a time
- Ask follow-up questions if the answer lacks depth
- Stay professional and neutral
- Do not reveal scores or feedback
- Format your response as:
  QUESTION: [Your question or follow-up]
  EVALUATION: [Brief evaluation if this is a follow-up, otherwise write "Initial question"]

Conversation history:
{history}

Candidate response:
{input}
""",
        input_variables=["history", "input", "role"]
    )

    # llm = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0.3,
    #     api_key=OPENAI_API_KEY
    # )

    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)

    def get_session_history(session_id):
        if session_id not in session_store:
            session_store[session_id] = ChatMessageHistory()
        return session_store[session_id]

    chain = RunnableWithMessageHistory(
        runnable=prompt | llm,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    return chain
