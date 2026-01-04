# AI-Assisted Technical Interviewer

## Overview
This project implements a text-based AI-assisted interviewer that conducts structured technical interviews and generates an evaluation report.

The focus is on interview flow, consistent assessment, and evidence-backed reporting rather than real-time audio or video integration.

## Features
- 🎤 Interactive chat-based interview interface
- 🤖 Intelligent follow-up questions using LLMs (Groq or OpenAI)
- 📊 Comprehensive scoring system (1-5 scale)
- 📈 Detailed candidate assessment reports
- 💾 Download reports in JSON format
- 🎨 Streamlit-based UI for easy interaction

## Architecture
Candidate (Text Input) → Interview Controller → LLM (Questions & Evaluation) → Scoring → Structured Report

## Setup & Installation

### 1. Clone and Install Dependencies
```bash
cd ai_assistance_interviewer
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Or add them via the Streamlit sidebar when running the app.

### 3. Run the Streamlit App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

### Web Interface (Recommended)
1. **Configure Settings** (Sidebar):
   - Enter your Groq and/or OpenAI API keys
   - Select your preferred LLM provider and model
   - Adjust interview settings (max follow-ups, template)

2. **Start Interview**:
   - Enter candidate name
   - Click "🚀 Start Interview"
   - Answer questions in the chat interface
   - View score after each answer

3. **View Report**:
   - After all questions, view comprehensive report
   - Sections include: Summary, Strengths, Concerns, Notable Quotes, Follow-up Questions
   - Download report as JSON

### Command Line Interface (Legacy)
```bash
cd interviewer
python main.py
```

## Report Sections

The generated report includes:

- **Candidate Summary**: Name, position, date, duration
- **Overall Recommendation**: Strong Hire / Hire / No Hire / Strong No Hire
- **Dimension Scores**: Score per topic area with justification
- **Key Strengths**: High-scoring answers with supporting evidence
- **Areas of Concern**: Low-scoring answers identified for improvement
- **Notable Quotes**: Direct quotes from the interview
- **Full Transcript**: Complete Q&A record
- **Summary Statistics**: Score distribution and ranges

## Configuration

### Interview Templates
Templates are YAML files in `templates/` directory. Example:
```yaml
role: Backend Engineer
sections:
  - name: Python Fundamentals
    questions:
      - "Explain Python memory management"
      - "What are decorators?"
  - name: System Design
    questions:
      - "Design a caching layer"
```

### LLM Models Available

**Groq Models:**
- llama-3.1-8b-instant (fast, free tier)
- Gemma2-9b-It
- mixtral-8x7b-32768

**OpenAI Models:**
- gpt-4o-mini (recommended)
- gpt-4
- gpt-3.5-turbo

## Project Structure
```
ai_assistance_interviewer/
├── app.py                    # Streamlit web application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── interviewer/
│   ├── __init__.py
│   ├── main.py              # CLI interface
│   ├── interview_chain.py    # LLM chain setup
│   ├── evaluator.py         # Answer evaluation logic
│   ├── sessions.py          # Interview session management
│   └── report.py            # Report generation
└── templates/
    └── backend_engineer.yaml # Interview questions template
```

## Scoring System
- **5**: Excellent/comprehensive answer with deep understanding
- **4**: Good answer with clear explanation
- **3**: Adequate/acceptable answer
- **2**: Partially correct but lacks depth
- **1**: Completely wrong or no understanding

## API Keys

### Getting Groq API Key
1. Visit https://console.groq.com
2. Sign up/Login
3. Create API key in settings
4. Copy and paste in Streamlit sidebar or `.env` file

### Getting OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Copy and paste in Streamlit sidebar or `.env` file
Structured Interview Report

## How It Works
- Loads an interview template
- Asks predefined questions
- Generates follow-up prompts when needed
- Collects evaluation notes
- Produces a final recommendation

## Limitations
- Text-only interaction
- No direct video or voice integration
- Scoring is heuristic-based

## Future Improvements
- Speech-to-text integration
- Video call platforms
- More granular scoring rubrics
