"""Gemini AI Recommendation Service with multimodal vision, JSON output, and robust fallbacks."""
import json
import logging
import re
from typing import Dict, Any, Optional
from PIL import Image
from app.config import settings
from app.services.product_service import ProductService
from app.services.budget_service import BudgetService

logger = logging.getLogger("pocketsmart.ai")

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.demo_mode = settings.DEMO_MODE or not bool(self.api_key.strip())
        self._client_initialized = False

        if not self.demo_mode:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.genai = genai
                self._client_initialized = True
            except Exception as e:
                logger.warning(f"Failed to initialize Google Gemini client: {e}. Falling back to demo mode.")
                self.demo_mode = True

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Safely extract and parse JSON from model output."""
        try:
            # First try direct parse
            return json.loads(text.strip())
        except Exception:
            pass

        # Try to match ```json ... ``` block
        pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # Try finding outer braces
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except Exception:
                pass

        return None

    def analyze_outfit(self, image_path: str) -> str:
        """
        Multimodal image analysis of outfit for jewelry styling.
        Section 9: Does NOT claim certainty, gracefully handles failures.
        """
        if self.demo_mode or not self._client_initialized:
            return "Visual Style Analysis (Demo Mode): Identified complementary palette with rich neutral/jewel tones. Recommended pairing with warm gold accents and refined crystal highlights."

        try:
            img = Image.open(image_path)
            model = self.genai.GenerativeModel(self.model_name)
            prompt = (
                "You are an expert fashion and jewelry stylist. Analyze this outfit image for jewelry matching. "
                "Describe the visible color palette, aesthetic style (e.g. traditional, modern, chic), "
                "neckline silhouette, and how jewelry metals and gemstones can harmonize with it. "
                "Keep your response concise, polite, and within 3-4 sentences. Do not claim absolute certainty."
            )
            response = model.generate_content([prompt, img])
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Outfit image analysis failed: {e}. Returning fallback aesthetic note.")

        return "Outfit Analysis: Based on the provided attire, traditional or contemporary metallic tones with balanced accents will complement the overall ensemble effectively."

    def generate_home_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured home interior recommendations using Gemini or Demo Fallback."""
        total_budget = float(request_data.get("total_budget", 50000))
        currency = request_data.get("currency", "₹")
        selected_rooms = request_data.get("selected_rooms", ["Living Room"])
        quantities = request_data.get("quantities", {})
        preferred_style = request_data.get("preferred_style", "Modern")

        # Baseline budget allocation
        calculated_allocation = BudgetService.calculate_home_allocation(total_budget, selected_rooms, quantities)

        if self.demo_mode or not self._client_initialized:
            return self._fallback_home_plan(total_budget, currency, preferred_style, calculated_allocation)

        prompt = f"""
You are PocketSmart AI, an expert home interior budget planner.
Analyze the following user input and generate a JSON response strictly adhering to the schema.
Total Budget: {currency}{total_budget}
Home Type: {request_data.get('home_type')}
Rooms: {', '.join(selected_rooms)}
Product Quantities: {json.dumps(quantities)}
Preferred Style: {preferred_style}
Preferred Colors: {request_data.get('preferred_colors')}
Brand Preferences: {request_data.get('brand_preferences')}
Additional Requirements: {request_data.get('additional_requirements')}

Safety rule:
- Do not fabricate live URLs; use "#" for url.
- Platforms should be realistic (Amazon, Flipkart, IKEA, Pepperfry, Urban Ladder).
- Total estimated cost MUST NOT exceed the total budget of {total_budget}.

Return ONLY a single valid JSON object with this exact structure:
{{
  "summary": "...",
  "budget": {total_budget},
  "budget_allocation": [
    {{"category": "Category Name", "allocated": 0.0, "percentage": 0.0}}
  ],
  "recommendations": [
    {{
      "category": "...",
      "name": "...",
      "description": "...",
      "estimated_price": 0.0,
      "platform": "...",
      "url": "#",
      "reason": "...",
      "priority": "high"
    }}
  ],
  "total_estimated_cost": 0.0,
  "remaining_budget": 0.0
}}
"""
        try:
            model = self.genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            data = self._extract_json(response.text)
            if data and "recommendations" in data and len(data["recommendations"]) > 0:
                # Recalculate totals with budget engine for strict safety
                total_est, remaining, warning = BudgetService.evaluate_budget_totals(total_budget, data["recommendations"])
                data["total_estimated_cost"] = total_est
                data["remaining_budget"] = remaining
                data["currency"] = currency
                data["warning"] = warning
                return data
        except Exception as e:
            logger.error(f"Gemini home generation error: {e}")

        return self._fallback_home_plan(total_budget, currency, preferred_style, calculated_allocation)

    def generate_party_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured party and event recommendations."""
        total_budget = float(request_data.get("total_budget", 50000))
        currency = request_data.get("currency", "₹")
        guest_count = int(request_data.get("number_of_guests", 30))
        event_type = request_data.get("event_type", "Birthday")
        accommodation = request_data.get("accommodation_required", False)

        calculated_allocation = BudgetService.calculate_party_allocation(total_budget, guest_count, accommodation)

        if self.demo_mode or not self._client_initialized:
            return self._fallback_party_plan(total_budget, currency, guest_count, event_type, calculated_allocation)

        prompt = f"""
You are PocketSmart AI, an expert event planner.
Analyze the following event requirements and budget:
Total Budget: {currency}{total_budget}
Event Type: {event_type}
Guests: {guest_count}
Location: {request_data.get('location')}
Indoor/Outdoor: {request_data.get('indoor_outdoor')}
Duration: {request_data.get('event_duration')}
Food Preference: {request_data.get('food_preference')}
Decoration Style: {request_data.get('decoration_style')}
Entertainment: {request_data.get('entertainment_preference')}
Accommodation Needed: {accommodation}
Additional Notes: {request_data.get('additional_notes')}

Safety Rule:
- Use "#" for URLs.
- Platforms: Swiggy, Zomato, OYO Banquets, Urban Company, Local Vendor Network.
- Total estimated cost must remain within budget {total_budget}.

Return ONLY valid JSON matching this schema:
{{
  "summary": "...",
  "budget": {total_budget},
  "number_of_guests": {guest_count},
  "cost_per_guest": 0.0,
  "budget_allocation": [
    {{"category": "...", "allocated": 0.0, "percentage": 0.0}}
  ],
  "recommendations": [
    {{
      "category": "...",
      "name": "...",
      "description": "...",
      "estimated_price": 0.0,
      "platform": "...",
      "url": "#",
      "reason": "...",
      "priority": "high"
    }}
  ],
  "total_estimated_cost": 0.0,
  "remaining_budget": 0.0
}}
"""
        try:
            model = self.genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            data = self._extract_json(response.text)
            if data and "recommendations" in data and len(data["recommendations"]) > 0:
                total_est, remaining, warning = BudgetService.evaluate_budget_totals(total_budget, data["recommendations"])
                data["total_estimated_cost"] = total_est
                data["remaining_budget"] = remaining
                data["currency"] = currency
                data["cost_per_guest"] = round(total_est / max(1, guest_count), 2)
                data["warning"] = warning
                return data
        except Exception as e:
            logger.error(f"Gemini party generation error: {e}")

        return self._fallback_party_plan(total_budget, currency, guest_count, event_type, calculated_allocation)

    def generate_jewelry_recommendations(self, request_data: Dict[str, Any], outfit_image_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate structured jewelry recommendations with optional outfit analysis."""
        total_budget = float(request_data.get("total_budget", 15000))
        currency = request_data.get("currency", "₹")
        occasion = request_data.get("occasion", "Wedding")
        jewelry_type = request_data.get("jewelry_type", "Jewelry Set")
        preferred_style = request_data.get("preferred_style", "Traditional")
        metal_preference = request_data.get("metal_preference", "Gold")

        # Multimodal analysis if image provided
        outfit_analysis = None
        if outfit_image_path:
            outfit_analysis = self.analyze_outfit(outfit_image_path)

        calculated_allocation = BudgetService.calculate_jewelry_allocation(total_budget, jewelry_type)

        if self.demo_mode or not self._client_initialized:
            return self._fallback_jewelry_plan(total_budget, currency, occasion, jewelry_type, calculated_allocation, outfit_analysis)

        prompt = f"""
You are PocketSmart AI, a fine jewelry styling and budget consultant.
User Request:
Total Budget: {currency}{total_budget}
Occasion: {occasion}
Jewelry Type: {jewelry_type}
Style: {preferred_style}
Metal: {metal_preference}
Color Preference: {request_data.get('color_preference')}
Outfit Description: {request_data.get('outfit_description')}
Outfit Visual Analysis: {outfit_analysis if outfit_analysis else "None provided"}

Safety Rule:
- Use "#" for placeholder URLs.
- Recommended platforms: Tanishq, CaratLane, Kalyan Jewellers, Mia by Tanishq, Amazon.
- Total cost must be within {total_budget}.

Return ONLY valid JSON matching this schema:
{{
  "summary": "...",
  "outfit_analysis": "{outfit_analysis or 'No outfit image provided. Recommendations based on specified occasion and style.'}",
  "budget": {total_budget},
  "budget_allocation": [
    {{"category": "...", "allocated": 0.0, "percentage": 0.0}}
  ],
  "recommendations": [
    {{
      "category": "...",
      "name": "...",
      "description": "...",
      "estimated_price": 0.0,
      "platform": "...",
      "url": "#",
      "reason": "...",
      "priority": "high",
      "metal": "...",
      "style": "..."
    }}
  ],
  "total_estimated_cost": 0.0,
  "remaining_budget": 0.0
}}
"""
        try:
            model = self.genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            data = self._extract_json(response.text)
            if data and "recommendations" in data and len(data["recommendations"]) > 0:
                total_est, remaining, warning = BudgetService.evaluate_budget_totals(total_budget, data["recommendations"])
                data["total_estimated_cost"] = total_est
                data["remaining_budget"] = remaining
                data["currency"] = currency
                if outfit_analysis:
                    data["outfit_analysis"] = outfit_analysis
                data["warning"] = warning
                return data
        except Exception as e:
            logger.error(f"Gemini jewelry generation error: {e}")

        return self._fallback_jewelry_plan(total_budget, currency, occasion, jewelry_type, calculated_allocation, outfit_analysis)

    def _fallback_home_plan(self, budget: float, currency: str, style: str, allocation: list) -> Dict[str, Any]:
        """Realistic curated fallback plan for Home Interior."""
        recommendations = ProductService.get_home_recommendations_catalog(budget)
        total_est, remaining, warning = BudgetService.evaluate_budget_totals(budget, recommendations)
        return {
            "title": f"{style} Home Interior Budget Plan",
            "summary": f"Intelligently allocated plan for a {style} interior style within {currency}{budget:,.0f} budget. Balances functional essentials, ambient lighting, and aesthetic accents.",
            "budget": budget,
            "currency": currency,
            "budget_allocation": allocation,
            "recommendations": recommendations,
            "total_estimated_cost": total_est,
            "remaining_budget": remaining,
            "warning": warning
        }

    def _fallback_party_plan(self, budget: float, currency: str, guest_count: int, event_type: str, allocation: list) -> Dict[str, Any]:
        """Realistic curated fallback plan for Party & Event."""
        recommendations = ProductService.get_party_recommendations_catalog(budget, guest_count)
        total_est, remaining, warning = BudgetService.evaluate_budget_totals(budget, recommendations)
        return {
            "title": f"{event_type} Celebration Budget Plan",
            "summary": f"Comprehensive budget blueprint for {guest_count} guests celebrating a {event_type}. Prioritizes premier catering, inviting venue ambiance, and memorable photography.",
            "budget": budget,
            "currency": currency,
            "number_of_guests": guest_count,
            "cost_per_guest": round(total_est / max(1, guest_count), 2),
            "budget_allocation": allocation,
            "recommendations": recommendations,
            "total_estimated_cost": total_est,
            "remaining_budget": remaining,
            "warning": warning
        }

    def _fallback_jewelry_plan(self, budget: float, currency: str, occasion: str, jewelry_type: str, allocation: list, outfit_analysis: Optional[str]) -> Dict[str, Any]:
        """Realistic curated fallback plan for Jewelry."""
        recommendations = ProductService.get_jewelry_recommendations_catalog(budget, occasion, jewelry_type)
        total_est, remaining, warning = BudgetService.evaluate_budget_totals(budget, recommendations)
        analysis_text = outfit_analysis or (
            f"Styled for a {occasion} occasion. The suggested palette highlights refined craftsmanship "
            f"and complementary metalwork tailored for {jewelry_type} styling."
        )
        return {
            "title": f"{occasion} {jewelry_type} Budget Plan",
            "summary": f"Expert jewelry styling plan for {occasion} within {currency}{budget:,.0f}. Features a standout statement piece supported by versatile accent items.",
            "outfit_analysis": analysis_text,
            "budget": budget,
            "currency": currency,
            "occasion": occasion,
            "jewelry_type": jewelry_type,
            "budget_allocation": allocation,
            "recommendations": recommendations,
            "total_estimated_cost": total_est,
            "remaining_budget": remaining,
            "warning": warning
        }

gemini_service = GeminiService()
