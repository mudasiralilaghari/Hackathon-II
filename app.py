import os
from backend.src.main import app

# This creates the FastAPI app instance that Hugging Face Spaces will run
# The app is imported from the backend source code
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))