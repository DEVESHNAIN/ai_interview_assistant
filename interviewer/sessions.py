from datetime import datetime


class InterviewSession:
    def __init__(self, role, candidate_name=None):
        self.role = role
        self.candidate_name = candidate_name or "Anonymous"
        self.transcript = []
        self.evaluations = []
        self.start_time = datetime.now()
        self.dimension_scores = {}  # Scores by dimension/category
        self.notable_quotes = []

    def add_turn(self, question, answer, evaluation, dimension=None):
        self.transcript.append({
            "question": question,
            "answer": answer,
            "score": evaluation,
            "dimension": dimension
        })
        self.evaluations.append(evaluation)
        
        # Track dimension scores
        if dimension:
            if dimension not in self.dimension_scores:
                self.dimension_scores[dimension] = []
            self.dimension_scores[dimension].append(evaluation)
        
        # Track notable quotes (answers with high or low scores)
        if evaluation >= 4 or evaluation <= 2:
            self.notable_quotes.append({
                "question": question,
                "answer": answer,
                "score": evaluation
            })
    
    def get_duration(self):
        """Get interview duration in minutes"""
        duration = datetime.now() - self.start_time
        return int(duration.total_seconds() / 60)

