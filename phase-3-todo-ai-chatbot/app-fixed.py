# Hugging Face Spaces - Python SDK App
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

import uvicorn

if __name__ == "__main__":
    # Run the backend
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )
