# app/models/business.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Business:
    name: str                          # "Spice Garden"
    business_type: str                 # "restaurant"
    focus_areas: list[str] = field(default_factory=list)  # ["delivery", "quality"]
    business_id: str = None            # assigned on creation
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "business_id":   self.business_id,
            "name":          self.name,
            "business_type": self.business_type,
            "focus_areas":   self.focus_areas,
            "created_at":    self.created_at.isoformat()
        }