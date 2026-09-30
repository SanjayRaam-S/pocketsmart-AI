from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator

class ProductQuantities(BaseModel):
    lights: int = Field(0, ge=0)
    ceiling_fans: int = Field(0, ge=0)
    sofa: int = Field(0, ge=0)
    dining_table: int = Field(0, ge=0)
    chairs: int = Field(0, ge=0)
    bed: int = Field(0, ge=0)
    wardrobe: int = Field(0, ge=0)
    curtains: int = Field(0, ge=0)
    rugs: int = Field(0, ge=0)
    wall_art: int = Field(0, ge=0)
    storage: int = Field(0, ge=0)
    decorative_items: int = Field(0, ge=0)

class HomePlannerRequest(BaseModel):
    total_budget: float = Field(..., gt=0, description="Total budget must be greater than zero")
    currency: str = Field("₹", description="Currency symbol or code (e.g., ₹, $, €)")
    home_type: str = Field("2BHK", description="e.g. 1BHK, 2BHK, 3BHK, Villa, Studio Apartment, Single Room")
    number_of_rooms: int = Field(2, ge=1, le=20, description="Number of rooms to plan")
    selected_rooms: List[str] = Field(
        default_factory=lambda: ["Living Room", "Bedroom"],
        description="Rooms selected for interior planning"
    )
    quantities: ProductQuantities = Field(default_factory=ProductQuantities)
    preferred_style: str = Field("Modern", description="Modern, Minimalist, Scandinavian, Traditional, Industrial, Bohemian, Luxury")
    preferred_colors: Optional[str] = Field(None, description="e.g., Warm neutrals, earthy tones, navy & gold")
    brand_preferences: Optional[str] = Field(None, description="e.g., IKEA, Urban Ladder, Pepperfry, Amazon")
    min_item_price: Optional[float] = Field(None, ge=0)
    max_item_price: Optional[float] = Field(None, ge=0)
    additional_requirements: Optional[str] = Field(None, description="Special needs or constraints")

    @field_validator("selected_rooms")
    @classmethod
    def validate_selected_rooms(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one room must be selected")
        return v

class BudgetAllocationItem(BaseModel):
    category: str
    allocated: float
    percentage: float

class RecommendationItem(BaseModel):
    category: str
    name: str
    description: str
    estimated_price: float
    platform: str = "Amazon"
    url: str = "#"
    reason: str
    priority: str = "medium"  # high, medium, low
    image_url: Optional[str] = None

class HomePlannerResponse(BaseModel):
    plan_id: Optional[int] = None
    title: str = "Home Interior Budget Plan"
    summary: str
    budget: float
    currency: str = "₹"
    budget_allocation: List[BudgetAllocationItem]
    recommendations: List[RecommendationItem]
    total_estimated_cost: float
    remaining_budget: float
    warning: Optional[str] = None
