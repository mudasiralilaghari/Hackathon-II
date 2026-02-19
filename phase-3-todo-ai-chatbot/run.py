# run.py
import sys
import os

# Add backend/src to Python path
backend_src_path = os.path.join(os.path.dirname(__file__), 'backend', 'src')
if backend_src_path not in sys.path:
    sys.path.insert(0, backend_src_path)

# Import main application
try:
    from main import app
except ImportError as e:
    print(f"Error importing main: {e}")
    # Try alternative import
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from src.main import app
    except ImportError as e2:
        print(f"Alternative import also failed: {e2}")
        sys.exit(1)

# Initialize database
try:
    from models.base import init_db
    init_db()
except Exception as e:
    print(f"Database init warning: {e}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Todo AI Chatbot Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)