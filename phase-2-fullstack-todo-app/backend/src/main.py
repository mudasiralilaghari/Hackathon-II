from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
import uuid
from datetime import datetime, timedelta
import os
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import importlib


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_qg07lwzQrsbL@ep-broad-lake-ahts9zl6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")
engine = create_engine(DATABASE_URL, echo=True)


# Import models from the models module
from .models.user import User, UserCreate, UserBase
from .models.task import Task


# Password hashing - using argon2 instead of bcrypt to avoid 72-char limit
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
except ImportError:
    # Fallback to bcrypt with length handling if argon2 is not available
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(password: str) -> str:
        # Truncate password to 72 characters to comply with bcrypt limits
        truncated_password = password[:72] if len(password) > 72 else password
        return pwd_context.hash(truncated_password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "2f2f99a85c2ae5b883522a98cea7b0ae95a264af9a949a8a3a4e4bea2cae3942")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


# Lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield


# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
try:
    from src.api import auth_routes, task_routes
    app.include_router(auth_routes.router, prefix="", tags=["Authentication"])  # No prefix since auth_routes already has /auth
    app.include_router(task_routes.router, prefix="", tags=["Tasks"])  # No prefix since task_routes already has /tasks
except ImportError as e:
    print(f"Critical Error: Could not import API routes: {e}")
    raise e


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Neon DB Connected"}


