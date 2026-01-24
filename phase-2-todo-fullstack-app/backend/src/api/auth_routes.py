from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlmodel import Session, select
from typing import Dict
from ..models.user import UserCreate, UserRead
from ..services.auth_service import authenticate_user, create_user, create_token_for_user
from ..database import get_session
from ..middleware.auth import get_current_user
from ..models.user import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserRead)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user with this email or username already exists
    existing_user_by_email = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    existing_user_by_username = session.exec(select(User).where(User.username == user_create.username)).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # If no existing user found, create the new user
    try:
        db_user = create_user(session, user_create)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists"
        )


@router.post("/signin")
def signin(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
) -> Dict[str, str]:
    """Authenticate a user and return a JWT token"""
    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token_for_user(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user