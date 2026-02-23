# Hugging Face Spaces - Python SDK App
# This file runs the backend using uvicorn

import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment (HF Spaces uses 7860)
    port = int(os.environ.get("PORT", 7860))
    
    # Run the backend
    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
