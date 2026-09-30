"""Jewelry Budget Planner routes with multimodal outfit image upload."""
import os
import uuid
from typing import Optional
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.schemas.jewelry import JewelryPlannerRequest, JewelryPlannerResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter(tags=["Jewelry Planner"])
templates = Jinja2Templates(directory="templates")

@router.post("/api/generate-jewelry", response_model=JewelryPlannerResponse)
async def api_generate_jewelry(
    total_budget: float = Form(...),
    currency: str = Form("₹"),
    occasion: str = Form("Wedding"),
    jewelry_type: str = Form("Jewelry Set"),
    preferred_style: str = Form("Traditional"),
    metal_preference: str = Form("Gold"),
    color_preference: Optional[str] = Form(None),
    outfit_description: Optional[str] = Form(None),
    outfit_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate jewelry recommendations with optional multimodal outfit image analysis."""
    if total_budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than zero.")

    image_rel_path = None
    image_abs_path = None

    if outfit_image and outfit_image.filename:
        # Validate extension
        ext = Path(outfit_image.filename).suffix.lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{ext}'. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
            )

        # Read content and validate size
        content = await outfit_image.read()
        max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"Uploaded image exceeds maximum limit of {settings.MAX_IMAGE_SIZE_MB}MB."
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        saved_path = settings.UPLOAD_DIR / filename
        with open(saved_path, "wb") as f:
            f.write(content)

        image_rel_path = f"/uploads/{filename}"
        image_abs_path = str(saved_path)

    req = JewelryPlannerRequest(
        total_budget=total_budget,
        currency=currency,
        occasion=occasion,
        jewelry_type=jewelry_type,
        preferred_style=preferred_style,
        metal_preference=metal_preference,
        color_preference=color_preference,
        outfit_description=outfit_description,
        image_url=image_rel_path
    )

    plan = recommendation_service.create_jewelry_plan(
        db,
        current_user.id,
        req,
        image_relative_path=image_rel_path,
        image_absolute_path=image_abs_path
    )

    return JewelryPlannerResponse(
        plan_id=plan.id,
        title=plan.title,
        summary=plan.summary or "",
        outfit_analysis=plan.get_inputs().get("outfit_analysis"),
        budget=plan.budget,
        currency=plan.currency,
        occasion=occasion,
        jewelry_type=jewelry_type,
        budget_allocation=plan.get_allocation(),
        recommendations=plan.get_recommendations(),
        total_estimated_cost=plan.total_estimated_cost,
        remaining_budget=plan.remaining_budget,
        image_url=plan.image_url,
    )

@router.get("/jewelry-planner", response_class=HTMLResponse)
def view_jewelry_planner(request: Request, current_user: User = Depends(get_current_user)):
    """Render the Jewelry Budget Planner wizard page."""
    return templates.TemplateResponse(request=request, name="jewelry_planner.html", context={
        "request": request,
        "user": current_user,
        "title": "Jewelry Budget Planner - PocketSmart AI"
    })

@router.get("/jewelry-planner/results/{plan_id}", response_class=HTMLResponse)
def view_jewelry_results(
    plan_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render results for a specific jewelry plan."""
    plan = recommendation_service.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Jewelry plan not found.")

    return templates.TemplateResponse(request=request, name="jewelry_results.html", context={
        "request": request,
        "user": current_user,
        "plan": plan.to_dict(),
        "title": f"Results: {plan.title} - PocketSmart AI"
    })
