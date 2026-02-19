from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from dotenv import load_dotenv
import uuid
from datetime import datetime, timedelta
import os
from jose import jwt
from jose.exceptions import JWTError as PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
import importlib

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Database setup
# Load DATABASE_URL from .env file only (not hardcoded)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment variables")

# Create engine with proper SSL configuration for Neon
from sqlalchemy.pool import QueuePool

connect_args = {
    "sslmode": "require",
    "connect_timeout": 30,
}

engine = create_engine(
    DATABASE_URL, 
    echo=True,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args
)


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
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
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
    except PyJWTError:
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
    
    # Register MCP tools on startup (fix relative import issues by adding src to path)
    try:
        import sys
        import os
        # Add backend/src to Python path to fix relative imports
        backend_src_path = os.path.dirname(os.path.abspath(__file__))
        if backend_src_path not in sys.path:
            sys.path.insert(0, backend_src_path)

        from mcp.tools.add_task import AddTaskTool
        from mcp.tools.list_tasks import ListTasksTool
        from mcp.tools.complete_task import CompleteTaskTool
        from mcp.tools.update_task import UpdateTaskTool
        from mcp.tools.delete_task import DeleteTaskTool
        from mcp.tools_registry import register_tool, get_all_tools

        # Register tools in the shared registry
        register_tool("add_task", AddTaskTool)
        register_tool("list_tasks", ListTasksTool)
        register_tool("complete_task", CompleteTaskTool)
        register_tool("update_task", UpdateTaskTool)
        register_tool("delete_task", DeleteTaskTool)

        print(f"✓ MCP tools registered successfully: {list(get_all_tools().keys())}")
    except Exception as e:
        print(f"✗ Failed to register MCP tools: {e}")
        import traceback
        traceback.print_exc()
    
    yield


# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Import and include API routes
try:
    from .api.auth_routes import router as auth_router
    from .api.task_routes import router as task_router
    from .api.chat import router as chat_router
    from .api.chatkit import app as chatkit_router  # ChatKit router
    from .mcp.server import app as mcp_router, setup_startup_event  # MCP server as a router
    app.include_router(auth_router)  # auth_routes already has /auth prefix
    app.include_router(task_router)  # task_routes already has /tasks prefix
    app.include_router(chat_router)  # chat routes under /api/{user_id}/chat
    app.include_router(chatkit_router)  # ChatKit routes under root level
    app.include_router(mcp_router, prefix="/mcp")  # MCP routes under /mcp prefix
    # Setup startup event for MCP tools registration
    setup_startup_event(app)
except ImportError as e:
    print(f"Critical Error: Could not import API routes: {e}")
    raise e


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Neon DB Connected", "verification": "FASTAPI_RUNNING_12345"}

@app.get("/verify-execution")
def verify_execution():
    return {"status": "CONFIRMED", "execution": "FASTAPI_RUNNING_12345", "timestamp": 1234567890}

# Add a health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running correctly"}

# Add a test endpoint to verify API functionality
@app.get("/test")
def test_endpoint():
    return {"status": "success", "message": "API is responding correctly"}

# Add API documentation endpoints
@app.get("/docs")
def get_docs():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


