from datetime import datetime


def generate_report(session):
    """
    Generate a comprehensive interview report with all required sections
    """
    avg_score = sum(session.evaluations) / len(session.evaluations) if session.evaluations else 0
    
    # Determine recommendation
    if avg_score >= 4:
        recommendation = "Strong Hire"
    elif avg_score >= 3:
        recommendation = "Hire"
    elif avg_score >= 2:
        recommendation = "No Hire"
    else:
        recommendation = "Strong No Hire"
    
    # Extract key strengths (answers with score >= 4)
    key_strengths = []
    areas_of_concern = []
    
    for item in session.transcript:
        if item.get("score", 0) >= 4:
            key_strengths.append({
                "question": item["question"],
                "answer": item["answer"],
                "score": item["score"]
            })
        elif item.get("score", 0) <= 2:
            areas_of_concern.append({
                "question": item["question"],
                "answer": item["answer"],
                "score": item["score"]
            })
    
    # Calculate dimension scores with justification
    dimension_summaries = {}
    if session.dimension_scores:
        for dimension, scores in session.dimension_scores.items():
            avg_dim_score = sum(scores) / len(scores)
            dimension_summaries[dimension] = {
                "average_score": round(avg_dim_score, 2),
                "count": len(scores),
                "justification": f"Based on {len(scores)} question(s) in this dimension"
            }
    
    # Build comprehensive report
    report = {
        "candidate_summary": {
            "name": session.candidate_name,
            "position": session.role,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "duration_minutes": session.get_duration()
        },
        "overall_recommendation": recommendation,
        "average_score": round(avg_score, 2),
        "dimension_scores": dimension_summaries,
        "key_strengths": [
            {
                "title": f"Strong Answer to '{strength['question'][:50]}...'",
                "evidence": strength["answer"][:150] + "...",
                "score": strength["score"]
            }
            for strength in key_strengths[:3]  # Top 3 strengths
        ],
        "areas_of_concern": [
            {
                "title": f"Weak Answer to '{concern['question'][:50]}...'",
                "evidence": concern["answer"][:150] + "...",
                "score": concern["score"]
            }
            for concern in areas_of_concern[:3]  # Top 3 concerns
        ],
        "notable_quotes": [
            {
                "question": quote["question"],
                "quote": quote["answer"],
                "score": quote["score"],
                "significance": "Strong response" if quote["score"] >= 4 else "Needs improvement"
            }
            for quote in session.notable_quotes[:5]  # Top 5 notable quotes
        ],
        "transcript": session.transcript,
        "total_turns": len(session.transcript),
        "summary_statistics": {
            "highest_score": max(session.evaluations) if session.evaluations else 0,
            "lowest_score": min(session.evaluations) if session.evaluations else 0,
            "score_distribution": get_score_distribution(session.evaluations)
        }
    }
    
    return report


def get_score_distribution(evaluations):
    """
    Calculate distribution of scores
    """
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for score in evaluations:
        if 1 <= score <= 5:
            distribution[score] += 1
    return distribution
