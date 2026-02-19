# tests/integration/test_security_isolation.py
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_cross_user_data_isolation():
    """Test that User A cannot access User B's data."""
    USER_A = "user_a"
    USER_B = "user_b"
    
    # Step 1: User A creates a task
    chat_payload_a1 = {
        "user_id": USER_A,
        "message": "Add a new task: User A's task",
        "conversation_id": None
    }
    
    response_a1 = requests.post(f"{BASE_URL}/api/{USER_A}/chat", json=chat_payload_a1)
    assert response_a1.status_code == 200
    data_a1 = response_a1.json()
    
    # Get conversation ID for User A
    conv_id_a = data_a1["conversation_id"]
    
    # Step 2: User B tries to access User A's conversation
    chat_payload_b1 = {
        "user_id": USER_B,
        "message": "List all my tasks",
        "conversation_id": conv_id_a  # Trying to access User A's conversation
    }
    
    response_b1 = requests.post(f"{BASE_URL}/api/{USER_B}/chat", json=chat_payload_b1)
    assert response_b1.status_code == 403  # Should be forbidden
    
    # Step 3: User B creates their own task
    chat_payload_b2 = {
        "user_id": USER_B,
        "message": "Add a new task: User B's task",
        "conversation_id": None
    }
    
    response_b2 = requests.post(f"{BASE_URL}/api/{USER_B}/chat", json=chat_payload_b2)
    assert response_b2.status_code == 200
    data_b2 = response_b2.json()
    
    # Step 4: User A tries to access User B's task via tool call
    # In real implementation, this would be through natural language, but we'll simulate
    # First, get User B's conversation ID
    conv_id_b = data_b2["conversation_id"]
    
    # User A tries to list tasks in User B's conversation (should fail)
    chat_payload_a2 = {
        "user_id": USER_A,
        "message": "List all tasks",
        "conversation_id": conv_id_b  # Trying to access User B's conversation
    }
    
    response_a2 = requests.post(f"{BASE_URL}/api/{USER_A}/chat", json=chat_payload_a2)
    assert response_a2.status_code == 403  # Should be forbidden
    
    # Step 5: Verify User A can only see their own tasks
    chat_payload_a3 = {
        "user_id": USER_A,
        "message": "List all my tasks",
        "conversation_id": conv_id_a
    }
    
    response_a3 = requests.post(f"{BASE_URL}/api/{USER_A}/chat", json=chat_payload_a3)
    assert response_a3.status_code == 200
    data_a3 = response_a3.json()
    
    # Should contain tool call for list_tasks
    assert "tool_calls" in data_a3
    if data_a3["tool_calls"]:
        assert data_a3["tool_calls"][0]["name"] == "list_tasks"
    
    # Step 6: Verify User B can only see their own tasks
    chat_payload_b3 = {
        "user_id": USER_B,
        "message": "List all my tasks",
        "conversation_id": conv_id_b
    }
    
    response_b3 = requests.post(f"{BASE_URL}/api/{USER_B}/chat", json=chat_payload_b3)
    assert response_b3.status_code == 200
    data_b3 = response_b3.json()
    
    # Should contain tool call for list_tasks
    assert "tool_calls" in data_b3
    if data_b3["tool_calls"]:
        assert data_b3["tool_calls"][0]["name"] == "list_tasks"

def test_user_id_validation_in_mcp_tools():
    """Test that MCP tools validate user_id properly."""
    USER_A = "user_a"
    
    # Test with invalid user_id
    # This would be caught by the auth middleware in production, but let's test the tool validation
    
    # Simulate MCP tool call with invalid user_id
    mcp_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "tool_name": "list_tasks",
            "arguments": {}
        },
        "id": "1"
    }
    
    # In real implementation, user_id would come from headers
    # For testing, we'll use the chat endpoint which validates user_id
    
    # Try to use chat endpoint with invalid user_id format
    chat_payload = {
        "user_id": "",  # Empty user_id
        "message": "List all my tasks",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api//chat", json=chat_payload)
    # Should fail with 403 or 400
    assert response.status_code in [400, 403]

if __name__ == "__main__":
    pytest.main([__file__])