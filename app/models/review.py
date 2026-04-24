# app/models/review.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Review:
    text: str                          # raw review text
    business_id: str                   # which business this belongs to
    review_id: int = None              # assigned after analysis
    sentiment: str = None              # Positive / Negative / Neutral
    score: float = None                # 1.0 - 5.0
    issues: list[str] = field(default_factory=list)   # ["Delivery", "Food quality"]
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "review_id":   self.review_id,
            "text":        self.text,
            "business_id": self.business_id,
            "sentiment":   self.sentiment,
            "score":       self.score,
            "issues":      self.issues,
            "created_at":  self.created_at.isoformat()
        }