import uvicorn
import os
import sys
import importlib.util

# Try to import the app with multiple fallback options
try:
    # First try: Direct import
    from backend.src.main import app
except ImportError:
    try:
        # Second try: Import from nested directory
        from phase_2_fullstack_todo_app.backend.src.main import app
    except ImportError:
        # Third try: Use importlib to dynamically load
        import importlib.util
        import os

        # Try to find the main.py file in the correct location
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'backend', 'src', 'main.py'),
            os.path.join(os.path.dirname(__file__), 'phase-2-fullstack-todo-app', 'backend', 'src', 'main.py'),
            os.path.join(os.path.dirname(__file__), 'phase_2_fullstack_todo_app', 'backend', 'src', 'main.py')
        ]

        main_module = None
        for path in possible_paths:
            if os.path.exists(path):
                spec = importlib.util.spec_from_file_location("main", path)
                main_module = importlib.util.module_from_spec(spec)
                sys.modules["main"] = main_module
                spec.loader.exec_module(main_module)
                app = main_module.app
                break

        if main_module is None:
            # Create a fallback app if imports fail
            from fastapi import FastAPI
            app = FastAPI()

            @app.get("/")
            def fallback_home():
                return {"error": "Backend import failed", "message": "Check backend configuration"}

            @app.get("/health")
            def fallback_health():
                return {"status": "error", "message": "Backend not properly configured"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False
    )