# PocketSmart AI — Your Smart Budget & Recommendation Assistant

> **"Plan smarter. Spend better. Live better."**  
> An AI-powered full-stack budget planning and recommendation platform that helps users make purchasing, event-planning, and style decisions while strictly staying within their budget.

---

## 1. Project Overview

**PocketSmart AI** is a production-ready, full-stack web application designed to solve common budgeting dilemmas across three core domains:
1. **Home Interior Budget Planner**: Plan rooms, specify furniture & lighting quantities, and receive an intelligent category-by-category budget allocation with curated product recommendations from platforms like IKEA, Pepperfry, Urban Ladder, and Amazon.
2. **Party & Event Budget Planner**: Plan celebrations (birthdays, weddings, anniversaries, corporate events) with guest-count scaling, venue, catering, decor, sound, and accommodation allocation, calculating per-guest cost metrics.
3. **Jewelry Styling Planner**: Style jewelry sets and accent pieces tailored for occasions (weddings, parties, office, festivals) with multimodal vision analysis of user-uploaded outfit photos for neckline and palette harmony.

The core philosophy of PocketSmart AI:
$$\text{User Budget} + \text{Requirements} \longrightarrow \text{Gemini AI Analysis} \longrightarrow \text{Budget Allocation Engine} \longrightarrow \text{Strict Ceiling Enforced} \longrightarrow \text{Curated Recommendations}$$

---

## 2. Key Features

- **Three Specialized Planners in One Platform**:
  - Home Interior Planner with room selectors and product quantity steppers (sofa, bed, dining, lights, ceiling fans, curtains, rugs, art).
  - Party Planner with guest count scaling, catering style, venue type, and per-guest breakdown.
  - Jewelry Styling Planner with optional multimodal image upload for neckline and palette harmonization.
- **Budget Engine Safety Rule (Zero Silent Overruns)**:
  - Automatically calculates category percentage weights, allocated sums, estimated spend, and remaining cushion.
  - Never silently exceeds the user's budget.
- **AI Safety & Accuracy Standard**:
  - Eliminates fabricated prices and hallucinated external URLs.
  - Clear simulation and disclaimer labelling with modular `product_service.py` ready for live vendor API integration.
- **Dual Mode (Demo Mode & Live Gemini AI)**:
  - Works out of the box with zero external dependencies via `DEMO_MODE=true`.
  - Supports modern Gemini models (`gemini-1.5-flash`, `gemini-2.0-flash`, `gemini-2.5-flash`) when an API key is provided.
- **JWT Authentication & Protected User Sessions**:
  - Secure registration with password hashing via `bcrypt`.
  - JWT tokens handled via both Authorization headers and HTTP-only cookies for frictionless browser navigation.
  - User Dashboard with metrics, activity log, and quick action shortcuts.
- **Full History & Bookmark Management**:
  - Review, filter by category, bookmark ("Saved in Collection"), and delete past plans.

---

## 3. Technology Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, Python-dotenv, PyJWT, Bcrypt, Starlette.
- **AI Layer**: Google Gemini API (`google-generativeai`) with multimodal vision support and structured JSON extraction.
- **Database**: SQLite with SQLAlchemy ORM (configured for seamless migration to PostgreSQL).
- **Frontend**: Modern semantic HTML5, responsive CSS3 design system, JavaScript (Vanilla ES6+), Jinja2 server-rendered templates.
- **Testing**: Automated integration and regression test suite via `fastapi.testclient` and `httpx`.

---

## 4. Folder Structure

```text
pocketsmart-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app initialization, routes mounting & error handling
│   ├── config.py                   # Central settings, environment variables & upload paths
│   ├── database.py                 # SQLAlchemy engine, session maker & get_db dependency
│   ├── dependencies.py             # Bcrypt hashing, JWT tokens, OAuth2 & user extraction
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User SQLAlchemy model
│   │   ├── recommendation.py       # Plan model (parameters, allocations, recommendations)
│   │   └── history.py              # History aliases and queries
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                 # UserRegister, UserLogin, Token schemas
│   │   ├── home.py                 # HomePlannerRequest & HomePlannerResponse schemas
│   │   ├── party.py                # PartyPlannerRequest & PartyPlannerResponse schemas
│   │   └── jewelry.py              # JewelryPlannerRequest & JewelryPlannerResponse schemas
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # /api/register, /api/login, /api/logout, /session-info
│   │   ├── home.py                 # /api/generate-home, /home-planner views
│   │   ├── party.py                # /api/generate-party, /party-planner views
│   │   ├── jewelry.py              # /api/generate-jewelry, /jewelry-planner views
│   │   ├── recommendations.py      # /api/recommendations/{id}, /save bookmarking
│   │   └── history.py              # /api/history, /history page views
│   │
│   └── services/
│       ├── __init__.py
│       ├── budget_service.py       # Budget allocation, safety calculations & ceiling enforcement
│       ├── product_service.py      # Mock marketplace catalog (IKEA, Swiggy, CaratLane, Amazon)
│       ├── gemini_service.py       # Gemini API client, multimodal vision & fallback logic
│       └── recommendation_service.py # Database persistence, plan retrieval & dashboard statistics
│
├── templates/
│   ├── base.html                   # Master layout with responsive navbar, user badge & footer
│   ├── index.html                  # Landing page (hero, feature cards, how it works, testimonials)
│   ├── login.html                  # Sign-in page with validation
│   ├── register.html               # Registration page with confirmation checks
│   ├── dashboard.html              # Personalized user metrics and recent recommendations
│   ├── home_planner.html           # Home interior wizard (room chips, quantity steppers, style)
│   ├── home_results.html           # Home recommendations cards and category breakdown
│   ├── party_planner.html          # Party wizard (guest scale, catering, decor, sound)
│   ├── party_results.html          # Party recommendations with cost-per-guest metrics
│   ├── jewelry_planner.html        # Jewelry wizard with outfit image drag-and-drop
│   ├── jewelry_results.html        # Jewelry cards with multimodal visual analysis notes
│   └── history.html                # Plan archives with category filter pills, reuse, and delete
│
├── static/
│   ├── css/
│   │   └── style.css               # Modern SaaS CSS design system
│   └── js/
│       ├── app.js                  # Toast notifications, logout handler, navbar toggle
│       └── planners.js             # Interactive form controllers, image preview, AJAX loaders
│
├── tests/
│   └── test_full_suite.py          # Complete integration test suite
│
├── uploads/                        # Uploaded outfit images directory
├── .env.example                    # Template environment variables
├── .env                            # Active local environment variables
├── requirements.txt                # Python package dependencies
├── README.md                       # Complete documentation
└── run.py                          # Server launcher entrypoint
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- `pip` package manager

### Step 1: Navigate to Project Directory
```powershell
cd C:\Users\Home\.gemini\antigravity\scratch\pocketsmart-ai
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 6. Environment Variables

Create or update `.env` in the project root:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
DEMO_MODE=true

# Security & JWT
SECRET_KEY=pocketsmart-secure-secret-key-change-in-production-2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=sqlite:///./pocketsmart.db

# Storage
UPLOAD_DIR=uploads
```

### Switching from Demo Mode to Live Gemini AI
1. Set `GEMINI_API_KEY=AIzaSy...` with your active key from [Google AI Studio](https://aistudio.google.com/).
2. Set `DEMO_MODE=false`.
3. Save `.env`. The app will automatically connect to Gemini AI for live generation and multimodal outfit analysis.

---

## 7. Running Locally

### Option A: Using the Runner Script
```powershell
python run.py
```

### Option B: Using Uvicorn Directly
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The application will be live at:
- **Web Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 8. Running the Automated Test Suite

A comprehensive test suite verifies every route, authentication, validation errors, duplicate registrations, planners, multimodal uploads, bookmarking, and deletion:

```powershell
python tests/test_full_suite.py
```

Expected output:
```text
ALL TESTS PASSED SUCCESSFULLY!
```

---

## 9. API Reference & Examples

### 9.1 Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/register` | Register new user account |
| `POST` | `/api/login` | Authenticate user & receive JWT token |
| `POST` | `/api/logout` | Clear user cookie session |
| `GET` | `/api/session-info` | Verify authenticated session |

#### Register Request Example (`POST /api/register`)
```json
{
  "full_name": "Sarah Connor",
  "email": "sarah@example.com",
  "password": "Password123",
  "confirm_password": "Password123"
}
```

#### Login Request Example (`POST /api/login`)
```json
{
  "email": "sarah@example.com",
  "password": "Password123"
}
```

---

### 9.2 Home Interior Planner (`POST /api/generate-home`)

#### Request
```json
{
  "total_budget": 60000,
  "currency": "₹",
  "home_type": "2BHK Apartment",
  "number_of_rooms": 2,
  "selected_rooms": ["Living Room", "Bedroom"],
  "quantities": {
    "lights": 4,
    "ceiling_fans": 2,
    "sofa": 1,
    "dining_table": 1,
    "chairs": 4,
    "bed": 1,
    "wardrobe": 1,
    "curtains": 2,
    "rugs": 1,
    "wall_art": 2
  },
  "preferred_style": "Scandinavian",
  "preferred_colors": "Warm beige, sage green",
  "brand_preferences": "IKEA, Urban Ladder"
}
```

#### Response
```json
{
  "plan_id": 8,
  "title": "Scandinavian Home Interior Budget Plan",
  "summary": "Intelligently allocated plan for a Scandinavian interior style within ₹60,000 budget.",
  "budget": 60000.0,
  "currency": "₹",
  "budget_allocation": [
    {"category": "Furniture (Sofa, Bed, Dining, Storage)", "allocated": 27000.0, "percentage": 45.0},
    {"category": "Lighting & Electricals", "allocated": 9000.0, "percentage": 15.0},
    {"category": "Soft Furnishings & Curtains", "allocated": 9000.0, "percentage": 15.0},
    {"category": "Decor & Wall Art", "allocated": 9000.0, "percentage": 15.0},
    {"category": "Contingency & Installation", "allocated": 6000.0, "percentage": 10.0}
  ],
  "recommendations": [
    {
      "category": "Furniture (Sofa, Bed, Dining, Storage)",
      "name": "Nordic Solid Wood 3-Seater Fabric Sofa",
      "description": "Ergonomic high-density foam 3-seater couch with stain-resistant fabric and oak legs.",
      "estimated_price": 16298.0,
      "platform": "IKEA",
      "url": "#",
      "reason": "Offers optimum balance of durability and contemporary minimalist design within budget.",
      "priority": "high"
    }
  ],
  "total_estimated_cost": 55200.0,
  "remaining_budget": 4800.0,
  "warning": null
}
```

---

### 9.3 Party & Event Planner (`POST /api/generate-party`)

#### Request
```json
{
  "total_budget": 50000,
  "currency": "₹",
  "event_type": "Birthday",
  "number_of_guests": 35,
  "location": "Central Delhi",
  "indoor_outdoor": "Indoor",
  "event_duration": "4 hours",
  "food_preference": "Both",
  "decoration_style": "Fairy Lights",
  "entertainment_preference": "DJ & Sound System",
  "accommodation_required": false
}
```

---

### 9.4 Jewelry Styling Planner (`POST /api/generate-jewelry`)

Supports both JSON and `multipart/form-data` with optional outfit image upload:

```powershell
curl -X POST "http://127.0.0.1:8000/api/generate-jewelry" `
  -H "Authorization: Bearer <TOKEN>" `
  -F "total_budget=15000" `
  -F "occasion=Wedding" `
  -F "jewelry_type=Jewelry Set" `
  -F "preferred_style=Traditional" `
  -F "metal_preference=Gold Plated" `
  -F "outfit_image=@my_lehenga.jpg"
```

---

## 10. Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Missing token or expired session | Log in via `/login` or pass header `Authorization: Bearer <token>`. |
| `Unsupported file format` | Uploading non-image file | Upload files with extension `.jpg`, `.jpeg`, `.png`, or `.webp`. |
| `File exceeds 5MB` | Image file size too large | Resize image under 5MB before uploading. |
| `Gemini Quota Exceeded` | Google API rate limits reached | PocketSmart AI automatically falls back to curated mock recommendations without breaking the UI. |

---

## 11. License & Credits

Built with precision for modern shoppers and event planners. Powered by **Google Gemini AI**.
