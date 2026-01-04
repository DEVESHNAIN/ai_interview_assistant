import streamlit as st
import json
from datetime import datetime


def render_report(report):
    """Render the complete interview report"""
    st.divider()
    st.header("📊 Interview Report")
    
    # Candidate Summary
    with st.expander("📋 Candidate Summary", expanded=True):
        summary = report["candidate_summary"]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Name", summary["name"])
        with col2:
            st.metric("Position", summary["position"])
        with col3:
            st.metric("Date", summary["date"])
        with col4:
            st.metric("Duration", f"{summary['duration_minutes']} min")
    
    # Overall Recommendation
    with st.expander("🎯 Overall Assessment", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            recommendation = report["overall_recommendation"]
            color = "🟢" if "Hire" in recommendation else "🔴"
            st.metric("Recommendation", f"{color} {recommendation}")
        with col2:
            st.metric("Average Score", f"{report['average_score']}/5")
        with col3:
            stats = report["summary_statistics"]
            st.metric("Highest Score", f"{stats['highest_score']}/5")
    
    # Dimension Scores
    if report["dimension_scores"]:
        with st.expander("📈 Dimension Scores"):
            for dimension, scores in report["dimension_scores"].items():
                st.write(f"**{dimension}**: {scores['average_score']}/5")
                st.caption(scores['justification'])
    
    # Key Strengths
    if report["key_strengths"]:
        with st.expander("💪 Key Strengths"):
            for i, strength in enumerate(report["key_strengths"], 1):
                st.write(f"**{i}. {strength['title']}** (Score: {strength['score']}/5)")
                st.caption(strength['evidence'])
    
    # Areas of Concern
    if report["areas_of_concern"]:
        with st.expander("⚠️ Areas of Concern"):
            for i, concern in enumerate(report["areas_of_concern"], 1):
                st.write(f"**{i}. {concern['title']}** (Score: {concern['score']}/5)")
                st.caption(concern['evidence'])
    
    # Notable Quotes
    if report["notable_quotes"]:
        with st.expander("💬 Notable Quotes"):
            for i, quote in enumerate(report["notable_quotes"][:5], 1):
                st.write(f"**Q{i}:** {quote['question']}")
                st.info(f"**A:** {quote['quote']}")
                st.caption(f"Score: {quote['score']}/5 - {quote['significance']}")
    
    # Full Transcript
    with st.expander("📝 Full Transcript"):
        for i, turn in enumerate(report["transcript"], 1):
            st.write(f"**Q{i}:** {turn['question']}")
            st.write(f"**A:** {turn['answer']}")
            st.caption(f"Score: {turn['score']}/5 | Dimension: {turn.get('dimension', 'N/A')}")
            st.divider()
    
    # Download Report Button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start New Interview"):
            st.session_state.interview_started = False
            st.session_state.interview_complete = False
            st.session_state.session = None
            st.session_state.report = None
            st.session_state.messages = []
            st.session_state.current_question_idx = 0
            st.session_state.followup_count = 0
            st.rerun()
    
    with col2:
        report_json = json.dumps(report, indent=2, default=str)
        st.download_button(
            label="📥 Download Report (JSON)",
            data=report_json,
            file_name=f"interview_report_{report['candidate_summary']['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
