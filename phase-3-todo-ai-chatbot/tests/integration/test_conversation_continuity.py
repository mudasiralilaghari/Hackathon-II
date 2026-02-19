# tests/integration/test_conversation_continuity.py
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
USER_ID = "test-user"

def test_conversation_creation_and_resume():
    """Test creating a conversation and resuming it later."""
    # Step 1: Create first conversation
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Buy groceries",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data1 = response.json()
    
    # Get conversation ID from first response
    conversation_id = data1["conversation_id"]
    assert conversation_id is not None
    
    # Step 2: Add another task in the same conversation
    chat_payload2 = {
        "user_id": USER_ID,
        "message": "Add another task: Call mom",
        "conversation_id": conversation_id
    }
    
    response2 = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload2)
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Verify same conversation ID
    assert data2["conversation_id"] == conversation_id
    
    # Step 3: Resume the conversation later (simulated by using same conversation_id)
    chat_payload3 = {
        "user_id": USER_ID,
        "message": "List all my tasks",
        "conversation_id": conversation_id
    }
    
    response3 = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload3)
    assert response3.status_code == 200
    data3 = response3.json()
    
    # Should contain tool call for list_tasks
    assert "tool_calls" in data3
    if data3["tool_calls"]:
        assert data3["tool_calls"][0]["name"] == "list_tasks"
    
    # Verify conversation continuity metadata
    assert "conversation_continuity" in data3
    assert "created_at" in data3["conversation_continuity"]
    assert "last_activity" in data3["conversation_continuity"]
    assert "total_messages" in data3["conversation_continuity"]

def test_recent_conversation_auto_selection():
    """Test that recent conversation is auto-selected when no conversation_id provided."""
    # First, create a conversation
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Test task",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data1 = response.json()
    
    conversation_id_1 = data1["conversation_id"]
    
    # Wait a bit (simulated) and create another conversation
    chat_payload2 = {
        "user_id": USER_ID,
        "message": "Add another task: Second test",
        "conversation_id": None
    }
    
    response2 = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload2)
    assert response2.status_code == 200
    data2 = response2.json()
    
    conversation_id_2 = data2["conversation_id"]
    
    # Now request without conversation_id - should use most recent
    chat_payload3 = {
        "user_id": USER_ID,
        "message": "List my tasks",
        "conversation_id": None
    }
    
    response3 = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload3)
    assert response3.status_code == 200
    data3 = response3.json()
    
    # Should use the most recent conversation (conversation_id_2)
    assert data3["conversation_id"] == conversation_id_2

if __name__ == "__main__":
    pytest.main([__file__])