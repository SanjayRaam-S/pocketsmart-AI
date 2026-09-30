"""Home Interior Budget Planner routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, get_optional_current_user
from app.schemas.home import HomePlannerRequest, HomePlannerResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter(tags=["Home Interior Planner"])
templates = Jinja2Templates(directory="templates")

@router.post("/api/generate-home", response_model=HomePlannerResponse)
def api_generate_home(
    request_data: HomePlannerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate intelligent Home Interior budget allocation and product recommendations."""
    if request_data.total_budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than zero.")
    if not request_data.selected_rooms:
        raise HTTPException(status_code=400, detail="Please select at least one room.")

    plan = recommendation_service.create_home_plan(db, current_user.id, request_data)

    return HomePlannerResponse(
        plan_id=plan.id,
        title=plan.title,
        summary=plan.summary or "",
        budget=plan.budget,
        currency=plan.currency,
        budget_allocation=plan.get_allocation(),
        recommendations=plan.get_recommendations(),
        total_estimated_cost=plan.total_estimated_cost,
        remaining_budget=plan.remaining_budget,
    )

@router.get("/home-planner", response_class=HTMLResponse)
def view_home_planner(request: Request, current_user: User = Depends(get_current_user)):
    """Render the Home Interior Planner wizard page."""
    return templates.TemplateResponse(request=request, name="home_planner.html", context={
        "request": request,
        "user": current_user,
        "title": "Home Interior Budget Planner - PocketSmart AI"
    })

@router.get("/home-planner/results/{plan_id}", response_class=HTMLResponse)
def view_home_results(
    plan_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the results page for a specific home plan."""
    plan = recommendation_service.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Home plan not found.")

    return templates.TemplateResponse(request=request, name="home_results.html", context={
        "request": request,
        "user": current_user,
        "plan": plan.to_dict(),
        "title": f"Results: {plan.title} - PocketSmart AI"
    })
