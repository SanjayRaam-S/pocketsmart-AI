"""Budget calculation and allocation service."""
from typing import List, Dict, Any, Tuple

class BudgetService:
    @staticmethod
    def calculate_home_allocation(
        total_budget: float,
        selected_rooms: List[str],
        quantities: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Intelligently calculate budget allocation across interior categories."""
        # Default baseline weights
        weights = {
            "Furniture (Sofa, Bed, Dining, Storage)": 0.45,
            "Lighting & Electricals": 0.15,
            "Soft Furnishings & Curtains": 0.15,
            "Decor & Wall Art": 0.15,
            "Contingency & Installation": 0.10,
        }

        # Dynamically adjust weights if specific items have heavy quantity requirements
        furniture_count = quantities.get("sofa", 0) + quantities.get("bed", 0) + quantities.get("dining_table", 0) + quantities.get("wardrobe", 0)
        lighting_count = quantities.get("lights", 0) + quantities.get("ceiling_fans", 0)
        decor_count = quantities.get("wall_art", 0) + quantities.get("decorative_items", 0) + quantities.get("rugs", 0)
        
        if furniture_count == 0 and (lighting_count > 0 or decor_count > 0):
            weights["Furniture (Sofa, Bed, Dining, Storage)"] = 0.20
            weights["Lighting & Electricals"] = 0.35
            weights["Decor & Wall Art"] = 0.25
            weights["Contingency & Installation"] = 0.20

        allocation = []
        for category, weight in weights.items():
            amount = round(total_budget * weight, 2)
            allocation.append({
                "category": category,
                "allocated": amount,
                "percentage": round(weight * 100, 1)
            })
        return allocation

    @staticmethod
    def calculate_party_allocation(
        total_budget: float,
        guest_count: int,
        accommodation_required: bool = False
    ) -> List[Dict[str, Any]]:
        """Calculate party budget allocation across categories."""
        if accommodation_required:
            weights = {
                "Food & Beverage": 0.35,
                "Venue Rental": 0.22,
                "Accommodation": 0.15,
                "Decoration & Theme": 0.12,
                "Entertainment & Sound": 0.08,
                "Photography & Memories": 0.05,
                "Miscellaneous & Emergency": 0.03
            }
        else:
            weights = {
                "Food & Beverage": 0.42,
                "Venue Rental": 0.25,
                "Decoration & Theme": 0.14,
                "Entertainment & Sound": 0.10,
                "Photography & Memories": 0.06,
                "Miscellaneous & Emergency": 0.03
            }

        allocation = []
        for category, weight in weights.items():
            amount = round(total_budget * weight, 2)
            allocation.append({
                "category": category,
                "allocated": amount,
                "percentage": round(weight * 100, 1)
            })
        return allocation

    @staticmethod
    def calculate_jewelry_allocation(
        total_budget: float,
        jewelry_type: str
    ) -> List[Dict[str, Any]]:
        """Calculate jewelry budget allocation."""
        if jewelry_type.lower() in ("jewelry set", "bridal set", "necklace set"):
            weights = {
                "Primary Statement Piece (Necklace/Set)": 0.65,
                "Complementary Accents (Earrings/Bangles)": 0.25,
                "Care Kit, Certification & Security Box": 0.10,
            }
        else:
            weights = {
                "Main Jewelry Piece": 0.80,
                "Complementary Minimal Accent": 0.12,
                "Care Kit, Certification & Box": 0.08,
            }

        allocation = []
        for category, weight in weights.items():
            amount = round(total_budget * weight, 2)
            allocation.append({
                "category": category,
                "allocated": amount,
                "percentage": round(weight * 100, 1)
            })
        return allocation

    @staticmethod
    def evaluate_budget_totals(
        total_budget: float,
        recommendations: List[Dict[str, Any]]
    ) -> Tuple[float, float, str]:
        """
        Calculates total estimated spending, remaining budget, and warning if exceeded.
        Enforces safety rule: never silently allow budget overruns.
        """
        total_estimated = sum(float(item.get("estimated_price", 0)) for item in recommendations)
        total_estimated = round(total_estimated, 2)
        remaining = round(total_budget - total_estimated, 2)
        
        warning = None
        if remaining < 0:
            overage = abs(remaining)
            warning = f"Estimated spending exceeds total budget by ₹{overage:,.2f}. Consider selecting lower-tier alternatives or adjusting quantities."
        elif remaining > 0 and remaining < (total_budget * 0.02):
            warning = "Budget is tightly utilized with minimal buffer."

        return total_estimated, remaining, warning
