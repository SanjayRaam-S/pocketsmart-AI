"""Recommendation orchestration and persistence service."""
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.recommendation import Plan
from app.schemas.home import HomePlannerRequest
from app.schemas.party import PartyPlannerRequest
from app.schemas.jewelry import JewelryPlannerRequest
from app.services.gemini_service import gemini_service

class RecommendationService:
    @staticmethod
    def create_home_plan(db: Session, user_id: int, request_data: HomePlannerRequest) -> Plan:
        data_dict = request_data.model_dump()
        result = gemini_service.generate_home_recommendations(data_dict)

        plan = Plan(
            user_id=user_id,
            planner_type="home",
            title=result.get("title", f"{request_data.preferred_style} Home Interior Plan"),
            budget=request_data.total_budget,
            currency=request_data.currency,
            summary=result.get("summary", ""),
            input_parameters=json.dumps(data_dict),
            budget_allocation=json.dumps(result.get("budget_allocation", [])),
            recommendations=json.dumps(result.get("recommendations", [])),
            total_estimated_cost=result.get("total_estimated_cost", 0.0),
            remaining_budget=result.get("remaining_budget", 0.0),
            is_saved=False
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def create_party_plan(db: Session, user_id: int, request_data: PartyPlannerRequest) -> Plan:
        data_dict = request_data.model_dump()
        result = gemini_service.generate_party_recommendations(data_dict)

        plan = Plan(
            user_id=user_id,
            planner_type="party",
            title=result.get("title", f"{request_data.event_type} Event Plan"),
            budget=request_data.total_budget,
            currency=request_data.currency,
            summary=result.get("summary", ""),
            input_parameters=json.dumps(data_dict),
            budget_allocation=json.dumps(result.get("budget_allocation", [])),
            recommendations=json.dumps(result.get("recommendations", [])),
            total_estimated_cost=result.get("total_estimated_cost", 0.0),
            remaining_budget=result.get("remaining_budget", 0.0),
            is_saved=False
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def create_jewelry_plan(
        db: Session,
        user_id: int,
        request_data: JewelryPlannerRequest,
        image_relative_path: Optional[str] = None,
        image_absolute_path: Optional[str] = None
    ) -> Plan:
        data_dict = request_data.model_dump()
        result = gemini_service.generate_jewelry_recommendations(data_dict, outfit_image_path=image_absolute_path)

        plan = Plan(
            user_id=user_id,
            planner_type="jewelry",
            title=result.get("title", f"{request_data.occasion} {request_data.jewelry_type} Plan"),
            budget=request_data.total_budget,
            currency=request_data.currency,
            summary=result.get("summary", ""),
            input_parameters=json.dumps(data_dict),
            budget_allocation=json.dumps(result.get("budget_allocation", [])),
            recommendations=json.dumps(result.get("recommendations", [])),
            total_estimated_cost=result.get("total_estimated_cost", 0.0),
            remaining_budget=result.get("remaining_budget", 0.0),
            image_url=image_relative_path,
            is_saved=False
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def get_plan_by_id(db: Session, plan_id: int, user_id: Optional[int] = None) -> Optional[Plan]:
        query = db.query(Plan).filter(Plan.id == plan_id)
        if user_id is not None:
            query = query.filter(Plan.user_id == user_id)
        return query.first()

    @staticmethod
    def toggle_save_plan(db: Session, plan_id: int, user_id: int) -> Optional[Plan]:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan:
            plan.is_saved = not plan.is_saved
            db.commit()
            db.refresh(plan)
        return plan

    @staticmethod
    def get_user_history(db: Session, user_id: int, limit: int = 50) -> List[Plan]:
        return db.query(Plan).filter(Plan.user_id == user_id).order_by(desc(Plan.created_at)).limit(limit).all()

    @staticmethod
    def delete_plan(db: Session, plan_id: int, user_id: int) -> bool:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan:
            db.delete(plan)
            db.commit()
            return True
        return False

    @staticmethod
    def get_dashboard_stats(db: Session, user_id: int) -> Dict[str, Any]:
        plans = db.query(Plan).filter(Plan.user_id == user_id).order_by(desc(Plan.created_at)).all()
        total_plans = len(plans)
        saved_plans = sum(1 for p in plans if p.is_saved)
        total_budget = sum(p.budget for p in plans)
        recent_plans = plans[:5]

        # Breakdown by planner type
        home_count = sum(1 for p in plans if p.planner_type == "home")
        party_count = sum(1 for p in plans if p.planner_type == "party")
        jewelry_count = sum(1 for p in plans if p.planner_type == "jewelry")

        return {
            "total_plans": total_plans,
            "saved_plans": saved_plans,
            "total_budget": total_budget,
            "home_count": home_count,
            "party_count": party_count,
            "jewelry_count": jewelry_count,
            "recent_plans": [p.to_dict() for p in recent_plans]
        }

recommendation_service = RecommendationService()
