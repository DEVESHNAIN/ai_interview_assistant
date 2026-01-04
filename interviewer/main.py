import yaml
from interview_chain import build_interview_chain
from evaluator import evaluate_answer
from sessions import InterviewSession
from report import generate_report


def load_template():
    with open("templates/AI_engineer.yaml", "r") as f:
        return yaml.safe_load(f)


def parse_llm_response(response_text):
    """Parse LLM response to extract question and evaluation"""
    lines = response_text.split('\n')
    question = ""
    evaluation = ""
    
    for i, line in enumerate(lines):
        if line.startswith("QUESTION:"):
            question = line.replace("QUESTION:", "").strip()
        elif line.startswith("EVALUATION:"):
            evaluation = line.replace("EVALUATION:", "").strip()
    
    return question, evaluation


def main():
    template = load_template()
    chain = build_interview_chain()
    
    # Collect candidate information
    print("="*50)
    print("Interview Setup")
    print("="*50)
    candidate_name = input("Enter candidate name: ").strip() or "Anonymous"
    
    session = InterviewSession(role=template["role"], candidate_name=candidate_name)

    session_id = "demo-session"
    max_followups = 1  # Max follow-ups per question

    print(f"\nStarting {session.role} interview for {candidate_name}\n")

    for section_idx, section in enumerate(template["sections"]):
        section_name = section.get("name", f"Section {section_idx + 1}")
        print(f"\n--- {section_name} ---\n")
        
        for question in section["questions"]:
            print("Interviewer:", question)
            answer = input("Candidate: ")
            
            # Evaluate the initial answer
            response = chain.invoke(
                {"input": answer, "role": template["role"]},
                config={"configurable": {"session_id": session_id}}
            )
            
            response_text = response.content
            followup_question, _ = parse_llm_response(response_text)
            
            # Evaluate candidate's answer using LLM
            score = evaluate_answer(answer)
            print(f"✓ Evaluation Score: {score}/5\n")
            session.add_turn(question, answer, score, dimension=section_name)
            
            # Ask follow-up questions
            followup_count = 0
            while followup_question and followup_count < max_followups:
                print(f"Interviewer: {followup_question}")
                followup_answer = input("Candidate: ")
                
                # Get next response (question or follow-up evaluation)
                response = chain.invoke(
                    {"input": followup_answer, "role": template["role"]},
                    config={"configurable": {"session_id": session_id}}
                )
                
                response_text = response.content
                next_question, _ = parse_llm_response(response_text)
                
                # Evaluate follow-up answer using LLM
                followup_score = evaluate_answer(followup_answer)
                print(f"✓ Evaluation Score: {followup_score}/5\n")
                session.add_turn(followup_question, followup_answer, followup_score, dimension=section_name)
                
                followup_question = next_question
                followup_count += 1
            
            print()

    report = generate_report(session)

    # Display comprehensive report
    print("\n" + "="*70)
    print("INTERVIEW REPORT")
    print("="*70)
    
    # Candidate Summary
    summary = report["candidate_summary"]
    print(f"\nCANDIDATE SUMMARY")
    print("-" * 70)
    print(f"Name: {summary['name']}")
    print(f"Position: {summary['position']}")
    print(f"Date: {summary['date']} at {summary['time']}")
    print(f"Duration: {summary['duration_minutes']} minutes")
    
    # Overall Recommendation
    print(f"\nOVERALL RECOMMENDATION: {report['overall_recommendation']}")
    print(f"Average Score: {report['average_score']}/5")
    
    # Dimension Scores
    if report["dimension_scores"]:
        print(f"\nDIMENSION SCORES")
        print("-" * 70)
        for dimension, scores in report["dimension_scores"].items():
            print(f"  {dimension}: {scores['average_score']}/5 ({scores['justification']})")
    
    # Key Strengths
    if report["key_strengths"]:
        print(f"\nKEY STRENGTHS")
        print("-" * 70)
        for i, strength in enumerate(report["key_strengths"], 1):
            print(f"  {i}. {strength['title']}")
            print(f"     Score: {strength['score']}/5")
    
    # Areas of Concern
    if report["areas_of_concern"]:
        print(f"\nAREAS OF CONCERN")
        print("-" * 70)
        for i, concern in enumerate(report["areas_of_concern"], 1):
            print(f"  {i}. {concern['title']}")
            print(f"     Score: {concern['score']}/5")
    
    # Notable Quotes
    if report["notable_quotes"]:
        print(f"\nNOTABLE QUOTES")
        print("-" * 70)
        for i, quote in enumerate(report["notable_quotes"][:3], 1):
            print(f"  {i}. Q: {quote['question'][:60]}...")
            print(f"     A: {quote['quote'][:80]}...")
            print(f"     Score: {quote['score']}/5 - {quote['significance']}")
    
    # Summary Statistics
    stats = report["summary_statistics"]
    print(f"\nSUMMARY STATISTICS")
    print("-" * 70)
    print(f"Highest Score: {stats['highest_score']}/5")
    print(f"Lowest Score: {stats['lowest_score']}/5")
    print(f"Total Q&A Turns: {report['total_turns']}")
    dist = stats['score_distribution']
    print(f"Score Distribution: 5★({dist[5]}) 4★({dist[4]}) 3★({dist[3]}) 2★({dist[2]}) 1★({dist[1]})")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

