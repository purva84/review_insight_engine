# app/models/insight.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Issue:
    issue: str
    percentage: int
    count: int
    severity: str                      # High / Medium / Low
    sample_quote: str

    def to_dict(self) -> dict:
        return {
            "issue":        self.issue,
            "percentage":   self.percentage,
            "count":        self.count,
            "severity":     self.severity,
            "sample_quote": self.sample_quote
        }

@dataclass
class Sentiment:
    positive: int                      # percentage
    negative: int                      # percentage
    neutral: int                       # percentage
    label: str                         # Positive / Negative / Mixed

    def to_dict(self) -> dict:
        return {
            "positive": self.positive,
            "negative": self.negative,
            "neutral":  self.neutral,
            "label":    self.label
        }

@dataclass
class Insight:
    business_id: str
    total_reviews: int
    overall_sentiment: Sentiment
    top_issues: list[Issue] = field(default_factory=list)
    root_cause: str = ""
    business_impact: str = ""
    recommendations: list[str] = field(default_factory=list)
    priority_action: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "business_id":        self.business_id,
            "total_reviews":      self.total_reviews,
            "overall_sentiment":  self.overall_sentiment.to_dict(),
            "top_issues":         [i.to_dict() for i in self.top_issues],
            "root_cause":         self.root_cause,
            "business_impact":    self.business_impact,
            "recommendations":    self.recommendations,
            "priority_action":    self.priority_action,
            "created_at":         self.created_at.isoformat()
        }