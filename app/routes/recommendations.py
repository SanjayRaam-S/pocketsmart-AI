"""Recommendation plan retrieval and save toggle routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.services.recommendation_service import recommendation_service

router = APIRouter(tags=["Recommendations"])

@router.get("/api/recommendations/{plan_id}")
def api_get_recommendation(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve full details of a saved or generated plan."""
    plan = recommendation_service.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return plan.to_dict()

@router.post("/api/recommendations/{plan_id}/save")
def api_toggle_save_recommendation(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle bookmark / save status for a recommendation plan."""
    plan = recommendation_service.toggle_save_plan(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {
        "success": True,
        "plan_id": plan.id,
        "is_saved": plan.is_saved,
        "message": "Plan saved successfully." if plan.is_saved else "Plan unsaved."
    }
