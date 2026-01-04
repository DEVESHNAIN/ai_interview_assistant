from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory

# Session storage for conversation history
session_store = {}

def build_interview_chain(llm_provider, api_key, model):
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

    if llm_provider == "Groq":
        llm = ChatGroq(model=model, groq_api_key=api_key, temperature=0.3)
    else:
        llm = ChatOpenAI(model=model, api_key=api_key, temperature=0.3)

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
