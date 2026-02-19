# backend/src/api/chatkit.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
import sys
import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create router instance
app = APIRouter()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatKitSessionRequest(BaseModel):
    workflow_id: str
    user_id: str

@app.post("/api/chatkit/session")
async def create_chatkit_session(request: ChatKitSessionRequest):
    """
    Create ChatKit session by calling OpenAI's ChatKit Sessions API.
    
    This is REQUIRED - the frontend cannot work without a backend that creates sessions.
    """
    try:
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        
        if not request.workflow_id or not request.user_id:
            raise HTTPException(status_code=400, detail="workflow_id and user_id are required")

        # Call OpenAI's ChatKit Sessions API
        # This is the official endpoint as per OpenAI documentation
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chatkit/sessions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                    "OpenAI-Beta": "chatkit_beta=v1",  # Required header for ChatKit API
                },
                json={
                    "workflow": {"id": request.workflow_id},
                    "user": request.user_id
                }
            )
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    print(f"OpenAI ChatKit API error ({response.status_code}): {error_data}")
                except:
                    error_data = {"error": response.text}
                    
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenAI ChatKit error: {error_data}"
                )
            
            session_data = response.json()
            client_secret = session_data.get("client_secret")
            
            if not client_secret:
                raise HTTPException(status_code=500, detail="No client_secret in response")
            
            return {"client_secret": client_secret}
        
    except httpx.RequestError as e:
        print(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to OpenAI: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"ChatKit session creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create ChatKit session: {str(e)}")
