"""PocketSmart AI - Main FastAPI Application."""
import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app.models.user import User
from app.dependencies import get_current_user, get_optional_current_user
from app.routes import (
    auth_router,
    home_router,
    party_router,
    jewelry_router,
    recommendations_router,
    history_router
)
from app.services.recommendation_service import recommendation_service

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Mount static and uploads
static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

uploads_dir = BASE_DIR / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include API and Feature Routers
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(party_router)
app.include_router(jewelry_router)
app.include_router(recommendations_router)
app.include_router(history_router)

# ==========================================
# CORE WEB PAGE CONTROLLERS
# ==========================================

@app.get("/", response_class=HTMLResponse)
def index_view(request: Request, current_user: User = Depends(get_optional_current_user)):
    """Render the high-converting Landing Page."""
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request,
        "user": current_user,
        "title": "PocketSmart AI — Plan smarter. Spend better. Live better."
    })

@app.get("/login", response_class=HTMLResponse)
def login_view(request: Request, current_user: User = Depends(get_optional_current_user)):
    """Render login page; redirects to dashboard if already authenticated."""
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="login.html", context={
        "request": request,
        "user": None,
        "title": "Login - PocketSmart AI"
    })

@app.get("/register", response_class=HTMLResponse)
def register_view(request: Request, current_user: User = Depends(get_optional_current_user)):
    """Render register page; redirects to dashboard if already authenticated."""
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="register.html", context={
        "request": request,
        "user": None,
        "title": "Create Account - PocketSmart AI"
    })

@app.get("/logout")
def logout_view():
    """Logout redirect helper."""
    response = RedirectResponse(url="/login?logged_out=1", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Personalized user dashboard with activity summary and quick planner links."""
    stats = recommendation_service.get_dashboard_stats(db, current_user.id)
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "request": request,
        "user": current_user,
        "stats": stats,
        "title": "Dashboard - PocketSmart AI"
    })

# ==========================================
# EXCEPTION HANDLERS
# ==========================================

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # If API request, return JSON
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    
    # If unauthorized browser request to a protected page, redirect to login
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url=f"/login?next={request.url.path}", status_code=status.HTTP_302_FOUND)

    # General error page or message
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
