"""Authentication routes: Register, Login, Logout, Session Info, and Token Handling."""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from app.dependencies import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    get_optional_current_user
)

router = APIRouter(tags=["Authentication"])

# ==========================================
# JSON API ENDPOINTS
# ==========================================

@router.post("/api/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def api_register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        full_name=user_in.full_name.strip(),
        email=user_in.email.lower(),
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/api/login", response_model=Token)
def api_login(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Login and receive JWT token."""
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is disabled.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.email, "id": user.id, "name": user.full_name},
        expires_delta=access_token_expires
    )

    # Set HTTP-only cookie for web browser session convenience
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/api/token", response_model=Token)
def api_token(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    """OAuth2 compatible token endpoint."""
    return api_login(user_in, response, db)

@router.post("/api/logout")
def api_logout(response: Response):
    """Logout current user and clear token cookie."""
    res = JSONResponse(content={"message": "Successfully logged out."})
    res.delete_cookie(key="access_token")
    return res

@router.get("/api/session-info")
def api_session_info(current_user: User = Depends(get_current_user)):
    """Retrieve current session info."""
    return {
        "authenticated": True,
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None
        }
    }

@router.get("/api/session-data")
def api_session_data(current_user: User = Depends(get_current_user)):
    """Alias for session info data."""
    return api_session_info(current_user)

# ==========================================
# TOP-LEVEL CONVENIENCE ALIASES (Spec Section 5)
# ==========================================

@router.post("/register")
def root_register(user_in: UserRegister, db: Session = Depends(get_db)):
    return api_register(user_in, db)

@router.post("/login")
def root_login(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    return api_login(user_in, response, db)

@router.post("/token")
def root_token(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    return api_login(user_in, response, db)

@router.post("/logout")
def root_logout(response: Response):
    return api_logout(response)

@router.get("/session-info")
def root_session_info(current_user: User = Depends(get_current_user)):
    return api_session_info(current_user)

@router.get("/session-data")
def root_session_data(current_user: User = Depends(get_current_user)):
    return api_session_data(current_user)
