"""Party and Event Budget Planner routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.schemas.party import PartyPlannerRequest, PartyPlannerResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter(tags=["Party / Event Planner"])
templates = Jinja2Templates(directory="templates")

@router.post("/api/generate-party", response_model=PartyPlannerResponse)
def api_generate_party(
    request_data: PartyPlannerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate intelligent party/event budget allocation and vendor recommendations."""
    if request_data.total_budget <= 0:
        raise HTTPException(status_code=400, detail="Total budget must be greater than zero.")
    if request_data.number_of_guests <= 0:
        raise HTTPException(status_code=400, detail="Guest count must be at least 1.")

    plan = recommendation_service.create_party_plan(db, current_user.id, request_data)

    return PartyPlannerResponse(
        plan_id=plan.id,
        title=plan.title,
        summary=plan.summary or "",
        budget=plan.budget,
        currency=plan.currency,
        number_of_guests=request_data.number_of_guests,
        cost_per_guest=round(plan.total_estimated_cost / max(1, request_data.number_of_guests), 2),
        budget_allocation=plan.get_allocation(),
        recommendations=plan.get_recommendations(),
        total_estimated_cost=plan.total_estimated_cost,
        remaining_budget=plan.remaining_budget,
    )

@router.get("/party-planner", response_class=HTMLResponse)
def view_party_planner(request: Request, current_user: User = Depends(get_current_user)):
    """Render the Party & Event Planner wizard page."""
    return templates.TemplateResponse(request=request, name="party_planner.html", context={
        "request": request,
        "user": current_user,
        "title": "Party & Event Budget Planner - PocketSmart AI"
    })

@router.get("/party-planner/results/{plan_id}", response_class=HTMLResponse)
def view_party_results(
    plan_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render results for a specific party plan."""
    plan = recommendation_service.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Event plan not found.")

    return templates.TemplateResponse(request=request, name="party_results.html", context={
        "request": request,
        "user": current_user,
        "plan": plan.to_dict(),
        "title": f"Results: {plan.title} - PocketSmart AI"
    })
