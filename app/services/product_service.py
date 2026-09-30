"""Product Catalog and Marketplace Service (Mock/Catalog layer for safety & fallback)."""
from typing import List, Dict, Any, Optional

class ProductService:
    DISCLAIMER = "Example / simulated recommendation for planning purposes. External live vendor APIs can be connected."

    MOCK_HOME_PRODUCTS = [
        {
            "id": "h1",
            "category": "Furniture (Sofa, Bed, Dining, Storage)",
            "name": "Nordic Solid Wood 3-Seater Fabric Sofa",
            "description": "Ergonomic high-density foam 3-seater couch with stain-resistant fabric and oak legs.",
            "estimated_price": 18500,
            "platform": "IKEA",
            "url": "#",
            "reason": "Offers optimum balance of durability and contemporary minimalist design within budget.",
            "priority": "high",
            "style": "Modern"
        },
        {
            "id": "h2",
            "category": "Furniture (Sofa, Bed, Dining, Storage)",
            "name": "Engineered Wood Queen Size Bed with Hydraulic Storage",
            "description": "Sturdy queen bed with hydraulic under-bed storage and upholstered headboard.",
            "estimated_price": 15999,
            "platform": "Pepperfry",
            "url": "#",
            "reason": "Maximizes bedroom floor space with easy lift hydraulic storage.",
            "priority": "high",
            "style": "Modern"
        },
        {
            "id": "h3",
            "category": "Furniture (Sofa, Bed, Dining, Storage)",
            "name": "Compact 4-Seater Sheesham Wood Dining Set",
            "description": "Solid Sheesham wood dining table with 4 cushioned high-back chairs.",
            "estimated_price": 12499,
            "platform": "Urban Ladder",
            "url": "#",
            "reason": "Durable hardwood construction designed for everyday family dining in compact spaces.",
            "priority": "medium",
            "style": "Traditional"
        },
        {
            "id": "h4",
            "category": "Lighting & Electricals",
            "name": "Smart Dimmable Warm LED Ceiling Chandelier & Spotlights",
            "description": "App-controlled flush-mount ceiling LED fixture with tunable white and ambient warm light.",
            "estimated_price": 4200,
            "platform": "Amazon",
            "url": "#",
            "reason": "Creates mood lighting effortlessly with energy-efficient A+ rated LEDs.",
            "priority": "high",
            "style": "Modern"
        },
        {
            "id": "h5",
            "category": "Lighting & Electricals",
            "name": "Silent BLDC 1200mm Decorative Ceiling Fan",
            "description": "Energy-saving BLDC motor ceiling fan with remote control and metallic finish.",
            "estimated_price": 3499,
            "platform": "Flipkart",
            "url": "#",
            "reason": "Reduces electricity costs up to 65% while maintaining silent airflow.",
            "priority": "medium",
            "style": "Modern"
        },
        {
            "id": "h6",
            "category": "Soft Furnishings & Curtains",
            "name": "Thermal Blackout Linen Textured Curtains (Set of 4)",
            "description": "Room-darkening grommet top curtains with soft drape and noise dampening.",
            "estimated_price": 2800,
            "platform": "Amazon",
            "url": "#",
            "reason": "Maintains temperature balance and delivers a clean hotel-quality finish.",
            "priority": "medium",
            "style": "Minimalist"
        },
        {
            "id": "h7",
            "category": "Soft Furnishings & Curtains",
            "name": "Boho Geometric Soft Touch Area Rug (5x7 ft)",
            "description": "Non-slip low pile decorative living room rug with geometric Scandinavian pattern.",
            "estimated_price": 3199,
            "platform": "IKEA",
            "url": "#",
            "reason": "Ties the room together with visual warmth and soft underfoot feel.",
            "priority": "low",
            "style": "Scandinavian"
        },
        {
            "id": "h8",
            "category": "Decor & Wall Art",
            "name": "Framed Botanical Abstract Canvas Art (Triptych)",
            "description": "Set of 3 minimalist framed canvas wall art prints with matte wood frame.",
            "estimated_price": 1950,
            "platform": "Pepperfry",
            "url": "#",
            "reason": "Adds focal point and sophisticated color accent to plain living room walls.",
            "priority": "low",
            "style": "Modern"
        }
    ]

    MOCK_PARTY_SERVICES = [
        {
            "category": "Venue Rental",
            "name": "Boutique AC Banquet Hall with Lawn Access",
            "description": "Air-conditioned indoor hall with attached open lawn, seating up to 80 guests.",
            "estimated_price": 15000,
            "platform": "OYO Banquets",
            "url": "#",
            "reason": "Spacious venue offering climate-controlled hall plus breezy garden photo-ops.",
            "priority": "high"
        },
        {
            "category": "Food & Beverage",
            "name": "Deluxe Multi-Cuisine Live Counter Buffet",
            "description": "3 Starters, 2 Main Curries, Breads, Biryani, Salad bar, and 2 Artisanal Desserts.",
            "estimated_price": 22000,
            "platform": "Swiggy Gourmet",
            "url": "#",
            "reason": "High guest satisfaction rating with curated hot live counters and hygienic prep.",
            "priority": "high"
        },
        {
            "category": "Decoration & Theme",
            "name": "Customized Fairy Light Canopy & Photo Backdrop",
            "description": "Floral arch, neon signage ('Celebration'), balloon garland, and LED mood par cans.",
            "estimated_price": 6500,
            "platform": "Urban Company",
            "url": "#",
            "reason": "Transforms the venue into an Instagram-worthy celebration space.",
            "priority": "medium"
        },
        {
            "category": "Entertainment & Sound",
            "name": "Professional DJ Setup with Sound & Wireless Mics",
            "description": "High-clarity JBL sound system, DJ console, dance floor lighting, and emcee support.",
            "estimated_price": 5000,
            "platform": "Local Vendor Network",
            "url": "#",
            "reason": "Keeps guest energy high with seamless curated playlists and announcements.",
            "priority": "medium"
        },
        {
            "category": "Photography & Memories",
            "name": "Event Highlights Candid Photography (3 Hours)",
            "description": "Professional photographer, 100+ edited high-res digital photos, and highlight reel.",
            "estimated_price": 3500,
            "platform": "Local Vendor Network",
            "url": "#",
            "reason": "Captures spontaneous guest memories without the host worrying about filming.",
            "priority": "low"
        }
    ]

    MOCK_JEWELRY_PRODUCTS = [
        {
            "category": "Primary Statement Piece (Necklace/Set)",
            "name": "Royal Polki Kundan Choker Necklace with Pearls",
            "description": "22k gold plated brass base with handcrafted uncut Polki stones and dangling cluster pearls.",
            "estimated_price": 8500,
            "metal": "Gold Plated Brass",
            "style": "Traditional Kundan",
            "platform": "Tanishq / Mia",
            "url": "#",
            "reason": "Perfect centerpiece that elevates deep-neck and bridal/festive silhouettes.",
            "priority": "high"
        },
        {
            "category": "Complementary Accents (Earrings/Bangles)",
            "name": "Matching Handcrafted Kundan Chandbali Earrings",
            "description": "Lightweight crescent-shaped chandelier earrings with enamel meenakari back.",
            "estimated_price": 3200,
            "metal": "Gold Plated Brass",
            "style": "Traditional",
            "platform": "CaratLane",
            "url": "#",
            "reason": "Harmonizes with the choker while remaining light on the ears for long events.",
            "priority": "high"
        },
        {
            "category": "Complementary Accents (Earrings/Bangles)",
            "name": "Adjustable Delicate Zircon Kada / Cuff Bracelet",
            "description": "Fine rhodium or rose gold plated cuff with sparkling prong-set American diamonds.",
            "estimated_price": 1800,
            "metal": "Rose Gold Plated 925 Silver",
            "style": "Contemporary",
            "platform": "CaratLane",
            "url": "#",
            "reason": "Subtle wrist sparkle that does not snag on embroidered fabrics.",
            "priority": "medium"
        },
        {
            "category": "Care Kit, Certification & Security Box",
            "name": "Velvet Jewelry Organizer with Anti-Tarnish Strips",
            "description": "Multi-compartment travel organizer with soft velvet lining and polishing cloth.",
            "estimated_price": 999,
            "metal": "N/A",
            "style": "Care & Storage",
            "platform": "Amazon",
            "url": "#",
            "reason": "Protects stones from moisture and scratches, keeping pieces heirloom fresh.",
            "priority": "low"
        }
    ]

    @classmethod
    def get_home_recommendations_catalog(cls, budget: float) -> List[Dict[str, Any]]:
        """Scale mock items proportionally to fit safely within user's exact budget target (92% target)."""
        results = []
        raw_total = sum(item["estimated_price"] for item in cls.MOCK_HOME_PRODUCTS)
        target_spend = budget * 0.92
        for item in cls.MOCK_HOME_PRODUCTS:
            new_item = dict(item)
            ratio = item["estimated_price"] / raw_total
            new_item["estimated_price"] = round(ratio * target_spend, 0)
            new_item["disclaimer"] = cls.DISCLAIMER
            results.append(new_item)
        return results

    @classmethod
    def get_party_recommendations_catalog(cls, budget: float, guest_count: int) -> List[Dict[str, Any]]:
        """Scale party mock items proportionally to fit safely within budget (93% target)."""
        results = []
        raw_total = sum(item["estimated_price"] for item in cls.MOCK_PARTY_SERVICES)
        target_spend = budget * 0.93
        for item in cls.MOCK_PARTY_SERVICES:
            new_item = dict(item)
            ratio = item["estimated_price"] / raw_total
            new_item["estimated_price"] = round(ratio * target_spend, 0)
            new_item["disclaimer"] = cls.DISCLAIMER
            results.append(new_item)
        return results

    @classmethod
    def get_jewelry_recommendations_catalog(cls, budget: float, occasion: str, jewelry_type: str) -> List[Dict[str, Any]]:
        """Scale jewelry mock items proportionally to fit safely within budget (90% target)."""
        results = []
        raw_total = sum(item["estimated_price"] for item in cls.MOCK_JEWELRY_PRODUCTS)
        target_spend = budget * 0.90
        for item in cls.MOCK_JEWELRY_PRODUCTS:
            new_item = dict(item)
            ratio = item["estimated_price"] / raw_total
            new_item["estimated_price"] = round(ratio * target_spend, 0)
            new_item["disclaimer"] = cls.DISCLAIMER
            results.append(new_item)
        return results
