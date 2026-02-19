import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try different import approaches to find the correct one
try:
    # First try: Direct import from backend
    from backend.src.main import app
    print("Successfully imported app from backend.src.main")
except ImportError as e:
    print(f"Failed to import from backend.src.main: {e}")
    try:
        # Second try: Import from phase-2-fullstack-todo-app.backend.src.main
        from phase_2_fullstack_todo_app.backend.src.main import app
        print("Successfully imported app from phase_2_fullstack_todo_app.backend.src.main")
    except ImportError as e2:
        print(f"Failed to import from phase_2_fullstack_todo_app.backend.src.main: {e2}")
        try:
            # Third try: Navigate to the nested directory structure
            import importlib.util
            # Find the main.py file in the nested directory
            main_path = os.path.join(project_root, "phase-2-fullstack-todo-app", "backend", "src", "main.py")
            spec = importlib.util.spec_from_file_location("main", main_path)
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            app = main_module.app
            print("Successfully imported app using importlib from nested directory")
        except Exception as e3:
            print(f"Failed to import using importlib: {e3}")
            # If all imports fail, create a minimal app for testing
            from fastapi import FastAPI
            app = FastAPI()

            @app.get("/")
            def read_root():
                return {"error": "Could not import backend application", "message": "Check backend configuration"}

            @app.get("/health")
            def health_check():
                return {"status": "error", "message": "Backend not properly configured"}

# This creates the FastAPI app instance that Hugging Face Spaces will run
# The app is imported from the backend source code
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))