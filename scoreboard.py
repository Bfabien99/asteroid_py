import json
import os
from datetime import datetime


class Scoreboard:
    def __init__(self, filename="scoreboard.json"):
        self.filename = filename
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        """Load scores from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.scores = json.load(f)
            except:
                self.scores = []
        else:
            self.scores = []
    
    def save_scores(self):
        """Save scores to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def add_score(self, name, score):
        """Add a new score to the scoreboard"""
        entry = {
            "name": name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.scores.append(entry)
        # Sort by score descending
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10 scores
        self.scores = self.scores[:10]
        self.save_scores()
    
    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]
    
    def is_high_score(self, score):
        """Check if score qualifies for leaderboard"""
        if score == 0:
            return False
        if len(self.scores) < 10:
            return True
        return score > self.scores[-1]["score"] if self.scores else True