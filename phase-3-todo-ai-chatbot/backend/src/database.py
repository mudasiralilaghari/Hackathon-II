from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

load_dotenv()
# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with simple configuration for Neon
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()