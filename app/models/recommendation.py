import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    planner_type = Column(String(50), nullable=False, index=True)  # 'home', 'party', 'jewelry'
    title = Column(String(200), nullable=False)
    budget = Column(Float, nullable=False)
    currency = Column(String(10), default="₹")
    summary = Column(Text, nullable=True)
    
    # JSON-encoded input parameters
    input_parameters = Column(Text, nullable=False)  # JSON string
    
    # JSON-encoded budget allocation and recommendations
    budget_allocation = Column(Text, nullable=False)  # JSON list
    recommendations = Column(Text, nullable=False)  # JSON list
    
    total_estimated_cost = Column(Float, nullable=False)
    remaining_budget = Column(Float, nullable=False)
    
    # Optional image path (e.g. for Jewelry Planner)
    image_url = Column(String(500), nullable=True)
    
    # Status
    is_saved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationship
    user = relationship("User", back_populates="plans")

    def get_inputs(self):
        try:
            return json.loads(self.input_parameters) if self.input_parameters else {}
        except Exception:
            return {}

    def get_allocation(self):
        try:
            return json.loads(self.budget_allocation) if self.budget_allocation else []
        except Exception:
            return []

    def get_recommendations(self):
        try:
            return json.loads(self.recommendations) if self.recommendations else []
        except Exception:
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planner_type": self.planner_type,
            "title": self.title,
            "budget": self.budget,
            "currency": self.currency,
            "summary": self.summary,
            "input_parameters": self.get_inputs(),
            "budget_allocation": self.get_allocation(),
            "recommendations": self.get_recommendations(),
            "total_estimated_cost": self.total_estimated_cost,
            "remaining_budget": self.remaining_budget,
            "image_url": self.image_url,
            "is_saved": self.is_saved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
