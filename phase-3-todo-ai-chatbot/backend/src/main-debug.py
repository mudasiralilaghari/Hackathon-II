# DEBUG VERSION - Prints import errors
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
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment variables")

# Create engine with simple configuration
from sqlalchemy.pool import QueuePool

connect_args = {
    "sslmode": "require",
    "connect_timeout": 30,
}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("=== Starting Todo AI Chatbot Backend ===")
    
    try:
        # Create database tables
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
    
    try:
        # Register MCP tools
        from mcp.tools_registry import register_tool, get_all_tools
        from mcp.tools.add_task import AddTaskTool
        from mcp.tools.list_tasks import ListTasksTool
        from mcp.tools.complete_task import CompleteTaskTool
        from mcp.tools.update_task import UpdateTaskTool
        from mcp.tools.delete_task import DeleteTaskTool

        register_tool("add_task", AddTaskTool)
        register_tool("list_tasks", ListTasksTool)
        register_tool("complete_task", CompleteTaskTool)
        register_tool("update_task", UpdateTaskTool)
        register_tool("delete_task", DeleteTaskTool)

        print(f"✓ MCP tools registered successfully: {list(get_all_tools().keys())}")
        
        # Create database tables
        from database_init import create_tables
        create_tables(engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Failed to register MCP tools: {e}")
        import traceback
        traceback.print_exc()

    yield


# Create FastAPI app
app = FastAPI(lifespan=lifespan, redirect_slashes=False)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Import and include API routes WITH DEBUG PRINTS
print("\n=== IMPORTING ROUTES ===")
try:
    print("Importing auth_routes...")
    from api.auth_routes import router as auth_router
    print("✓ auth_routes imported")
    
    print("Importing task_routes...")
    from api.task_routes import router as task_router
    print("✓ task_routes imported")
    
    print("Importing chat router...")
    from api.chat import router as chat_router
    print("✓ chat imported")
    
    print("Importing chatkit router...")
    from api.chatkit import app as chatkit_router
    print("✓ chatkit imported")
    
    print("Importing mcp server...")
    from mcp.server import app as mcp_router, setup_startup_event
    print("✓ mcp imported")
    
    print("\n=== INCLUDING ROUTES ===")
    app.include_router(auth_router, prefix="/auth")
    print("✓ Included auth routes at /auth")
    
    app.include_router(task_router, prefix="/tasks")
    print("✓ Included task routes at /tasks")
    
    app.include_router(chat_router, prefix="/api")
    print("✓ Included chat routes at /api")
    
    app.include_router(chatkit_router)
    print("✓ Included chatkit routes at /")
    
    app.include_router(mcp_router, prefix="/mcp")
    print("✓ Included mcp routes at /mcp")
    
    setup_startup_event(app)
    print("✓ Setup MCP startup event")
    
    print("\n✅ ALL ROUTES IMPORTED AND INCLUDED SUCCESSFULLY!")
    
except ImportError as e:
    print(f"\n❌ CRITICAL ERROR: Could not import API routes: {e}")
    import traceback
    traceback.print_exc()
    raise e
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    raise e


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Neon DB Connected", "verification": "FASTAPI_RUNNING_12345"}

@app.get("/verify-execution")
def verify_execution():
    return {"status": "CONFIRMED", "execution": "FASTAPI_RUNNING_12345", "timestamp": 1234567890}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running correctly"}

@app.get("/test")
def test_endpoint():
    return {"status": "OK", "message": "Test endpoint working"}
