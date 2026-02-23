from sqlmodel import Session, select
from ..models.user import User, UserCreate
from passlib.context import CryptContext
from ..middleware.auth import create_access_token
from typing import Optional
import uuid


# Password hashing context - using a more compatible bcrypt scheme
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        raise


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password"""
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        username=user_create.username,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_token_for_user(user: User) -> str:
    """Create an access token for a user"""
    return create_access_token(data={"sub": str(user.id)})