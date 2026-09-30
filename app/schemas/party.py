from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.home import BudgetAllocationItem, RecommendationItem

class PartyPlannerRequest(BaseModel):
    total_budget: float = Field(..., gt=0, description="Total budget must be greater than zero")
    currency: str = Field("₹", description="Currency symbol or code")
    event_type: str = Field("Birthday", description="Birthday, Wedding, Anniversary, Corporate, Engagement, Baby Shower, House Party, Other")
    number_of_guests: int = Field(..., gt=0, description="Number of guests must be positive")
    event_date: Optional[str] = Field(None, description="Planned date of the event")
    location: str = Field("New Delhi", description="City, locality, or venue area")
    indoor_outdoor: str = Field("Indoor", description="Indoor, Outdoor, Hybrid / Poolside")
    event_duration: str = Field("4 hours", description="e.g. 3 hours, 5 hours, Full day")
    food_preference: str = Field("Both", description="Vegetarian, Non-Vegetarian, Both, High-Tea, Buffet, Finger Foods")
    decoration_style: str = Field("Elegant Modern", description="Minimalist, Grand, Floral, Themed, Fairy Lights, Elegant Modern, Traditional")
    entertainment_preference: str = Field("DJ & Music", description="DJ & Music, Live Band, Emcee & Games, Acoustic, Background Music, None")
    accommodation_required: bool = Field(False, description="Whether guest accommodation is needed")
    additional_notes: Optional[str] = Field(None, description="Any dietary restrictions, theme colors, special requests")

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v):
        valid = ["Birthday", "Wedding", "Anniversary", "Corporate", "Engagement", "Baby Shower", "House Party", "Other"]
        if v not in valid:
            return "Other"
        return v

class PartyPlannerResponse(BaseModel):
    plan_id: Optional[int] = None
    title: str = "Party & Event Budget Plan"
    summary: str
    budget: float
    currency: str = "₹"
    number_of_guests: int
    cost_per_guest: float
    budget_allocation: List[BudgetAllocationItem]
    recommendations: List[RecommendationItem]
    total_estimated_cost: float
    remaining_budget: float
    warning: Optional[str] = None
