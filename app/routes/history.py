"""Recommendation History routes: view, reuse, and delete past plans."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.services.recommendation_service import recommendation_service

router = APIRouter(tags=["History"])
templates = Jinja2Templates(directory="templates")

@router.get("/api/history")
def api_get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all previous recommendation plans for the authenticated user."""
    plans = recommendation_service.get_user_history(db, current_user.id)
    return [p.to_dict() for p in plans]

@router.get("/api/history/{plan_id}")
def api_get_history_entry(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get single history plan entry."""
    plan = recommendation_service.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="History entry not found.")
    return plan.to_dict()

@router.delete("/api/history/{plan_id}")
def api_delete_history_entry(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a plan from history."""
    deleted = recommendation_service.delete_plan(db, plan_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="History entry not found or cannot be deleted.")
    return {"success": True, "message": "Plan deleted successfully."}

@router.get("/history", response_class=HTMLResponse)
def view_history(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the user history dashboard page."""
    plans = recommendation_service.get_user_history(db, current_user.id)
    return templates.TemplateResponse(request=request, name="history.html", context={
        "request": request,
        "user": current_user,
        "plans": [p.to_dict() for p in plans],
        "title": "Plan History - PocketSmart AI"
    })
