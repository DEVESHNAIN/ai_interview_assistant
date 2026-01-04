import streamlit as st
from interviewer.sessions import InterviewSession
from .chain import build_interview_chain, parse_llm_response
from interviewer.evaluator import evaluate_answer


def get_next_question(template):
    """Get the next question from template"""
    idx = st.session_state.current_question_idx
    for section in template["sections"]:
        for question in section["questions"]:
            if idx == 0:
                section_name = section.get("name", "General")
                return question, section_name
            idx -= 1
    return None, None


def count_total_questions(template):
    """Count total questions in template"""
    count = 0
    for section in template["sections"]:
        count += len(section["questions"])
    return count


def render_interview_header(template):
    """Render the interview header with candidate info and controls"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        candidate_name = st.text_input(
            "Candidate Name",
            value="",
            placeholder="Enter candidate name",
            disabled=st.session_state.interview_started
        )
    
    with col2:
        interview_role = st.selectbox(
            "Interview Role",
            [template["role"]],
            disabled=st.session_state.interview_started
        )
    
    with col3:
        if st.button("🚀 Start Interview", key="start_btn", disabled=st.session_state.interview_started or not candidate_name):
            st.session_state.interview_started = True
            st.session_state.session = InterviewSession(
                role=template["role"],
                candidate_name=candidate_name or "Anonymous"
            )
            st.session_state.current_question_idx = 0
            st.session_state.messages = []
            st.session_state.followup_count = 0
            st.success(f"✅ Interview started for {candidate_name}!")
            st.rerun()
    
    return candidate_name


def render_interview_interface(config, template):
    """Render the main interview interface"""
    if st.session_state.interview_started and not st.session_state.interview_complete:
        if st.session_state.chain is None:
            st.session_state.chain = build_interview_chain(
                config["llm_choice"],
                config["groq_api_key"] if config["llm_choice"] == "Groq" else config["openai_api_key"],
                config["selected_model"]
            )
            st.session_state.max_followups_value = config["max_followups"]
        
        # Progress indicator
        total_questions = count_total_questions(template)
        progress_col1, progress_col2 = st.columns([3, 1])
        
        with progress_col1:
            st.progress(st.session_state.current_question_idx / total_questions, 
                       f"Progress: {st.session_state.current_question_idx}/{total_questions} questions")
        
        with progress_col2:
            if st.button("🏁 End Interview"):
                st.session_state.interview_complete = True
                from interviewer.report import generate_report
                st.session_state.report = generate_report(st.session_state.session)
                st.success("Interview completed!")
                st.rerun()
        
        st.divider()
        
        # Get current question
        question, section_name = get_next_question(template)
        
        if question and st.session_state.current_question_idx < total_questions:
            st.subheader(f"📋 {section_name}")
            st.info(f"**Question:** {question}")
            
            # Chat interface
            st.subheader("💬 Q&A Chat")
            
            # Display chat history
            chat_container = st.container(height=400)
            with chat_container:
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        st.chat_message("user").write(message["content"])
                    else:
                        st.chat_message("assistant").write(message["content"])
            
            # Chat input
            user_input = st.chat_input("Your answer...", key=f"chat_input_{st.session_state.current_question_idx}")
            
            if user_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                try:
                    # Get LLM response
                    response = st.session_state.chain.invoke(
                        {"input": user_input, "role": template["role"]},
                        config={"configurable": {"session_id": "streamlit-session"}}
                    )
                    
                    response_text = response.content
                    followup_question, _ = parse_llm_response(response_text)
                    
                    # Evaluate answer
                    api_key = config["groq_api_key"] if config["llm_choice"] == "Groq" else config["openai_api_key"]
                    score = evaluate_answer(user_input, api_key)
                    st.session_state.session.add_turn(question, user_input, score, dimension=section_name)
                    
                    # Display score
                    st.success(f"✓ Score: {score}/5")
                    
                    # Check if we should ask follow-up question based on limit
                    # Only ask follow-up if it's not empty and we haven't exceeded the limit
                    if (followup_question and 
                        followup_question.strip() and 
                        len(followup_question) > 10 and
                        st.session_state.followup_count < st.session_state.max_followups_value):
                        st.session_state.followup_count += 1
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Follow-up:** {followup_question}"
                        })
                        st.rerun()
                    else:
                        # Move to next question - ensure follow-up state is reset
                        st.session_state.current_question_idx += 1
                        st.session_state.messages = []
                        st.session_state.followup_count = 0
                        
                        if st.session_state.current_question_idx >= total_questions:
                            st.session_state.interview_complete = True
                            from interviewer.report import generate_report
                            st.session_state.report = generate_report(st.session_state.session)
                            st.info("✅ All questions completed!")
                            st.rerun()
                        else:
                            st.rerun()
                            
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            if st.session_state.current_question_idx >= total_questions:
                st.session_state.interview_complete = True
                from interviewer.report import generate_report
                st.session_state.report = generate_report(st.session_state.session)
                st.rerun()
