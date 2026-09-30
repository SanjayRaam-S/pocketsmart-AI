from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.home import BudgetAllocationItem, RecommendationItem

class JewelryPlannerRequest(BaseModel):
    total_budget: float = Field(..., gt=0, description="Total budget must be positive")
    currency: str = Field("₹", description="Currency symbol")
    occasion: str = Field("Wedding", description="Wedding, Party, Office, Casual, Festival, Engagement, Date, Traditional Event")
    jewelry_type: str = Field("Jewelry Set", description="Necklace, Earrings, Bracelet, Ring, Bangles, Pendant, Jewelry Set")
    preferred_style: str = Field("Traditional", description="Minimalist, Traditional, Contemporary, Kundan/Polki, Diamond Solitaire, Vintage, Bohemian")
    metal_preference: str = Field("Gold", description="Yellow Gold, Rose Gold, White Gold, Platinum, Sterling Silver, Oxidized Silver, Brass/Alloy")
    color_preference: Optional[str] = Field(None, description="Preferred gemstones or enamel colors")
    outfit_description: Optional[str] = Field(None, description="Description of outfit, colors, neckline, fabric")
    image_url: Optional[str] = Field(None, description="Relative URL to uploaded outfit image if provided")

class JewelryRecommendationItem(RecommendationItem):
    metal: Optional[str] = None
    style: Optional[str] = None

class JewelryPlannerResponse(BaseModel):
    plan_id: Optional[int] = None
    title: str = "Jewelry Budget Recommendation Plan"
    summary: str
    outfit_analysis: Optional[str] = None
    budget: float
    currency: str = "₹"
    occasion: str
    jewelry_type: str
    budget_allocation: List[BudgetAllocationItem]
    recommendations: List[JewelryRecommendationItem]
    total_estimated_cost: float
    remaining_budget: float
    image_url: Optional[str] = None
    warning: Optional[str] = None
