from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def evaluate_answer(candidate_answer):
    """
    Use LLM to evaluate candidate answer on a scale of 1-5
    1: Completely wrong
    2: Partially correct/lacks depth
    3: Adequate/acceptable
    4: Good/clear explanation
    5: Excellent/comprehensive
    """
    if not candidate_answer or candidate_answer.strip() == "":
        return 1
    
    prompt = PromptTemplate(
        template="""
You are an expert technical interviewer. Evaluate the candidate's answer on a scale of 1-5:

1 - Completely wrong or no understanding
2 - Partially correct but lacks depth or contains errors
3 - Adequate/acceptable answer with basic understanding
4 - Good answer with clear explanation and relevant details
5 - Excellent/comprehensive answer with deep understanding and insightful details

Candidate's answer: {answer}

Respond with ONLY a single number (1-5) and a one-sentence reasoning.
Format: SCORE: [number] REASON: [reason]
""",
        input_variables=["answer"]
    )
    
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY, temperature=0.3)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"answer": candidate_answer})
        response_text = response.content
        
        # Extract score from response
        score_match = re.search(r'SCORE:\s*(\d+)', response_text)
        if score_match:
            score = int(score_match.group(1))
            score = max(1, min(5, score))  # Clamp between 1-5
            return score
    except Exception as e:
        print(f"Error in evaluation: {e}")
    
    return 3  # Default if evaluation fails
