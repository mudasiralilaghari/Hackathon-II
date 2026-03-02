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
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    print("Starting Todo AI Chatbot Backend...")
    # Use port 7860 for Hugging Face
    uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)