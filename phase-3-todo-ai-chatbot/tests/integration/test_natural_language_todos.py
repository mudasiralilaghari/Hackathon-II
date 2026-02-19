# tests/integration/test_natural_language_todos.py
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
USER_ID = "test-user"

def test_add_task_natural_language():
    """Test adding a task using natural language."""
    # First, create a conversation
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Buy groceries",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should contain tool call for add_task
    assert "tool_calls" in data
    if data["tool_calls"]:
        assert data["tool_calls"][0]["name"] == "add_task"
        assert "title" in data["tool_calls"][0]["arguments"]
        assert "Buy groceries" in data["tool_calls"][0]["arguments"]["title"]

def test_list_tasks():
    """Test listing tasks."""
    # First, ensure we have tasks
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Call mom",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    
    # Now list tasks
    chat_payload = {
        "user_id": USER_ID,
        "message": "List all my tasks",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should contain tool call for list_tasks
    assert "tool_calls" in data
    if data["tool_calls"]:
        assert data["tool_calls"][0]["name"] == "list_tasks"

def test_complete_task():
    """Test completing a task."""
    # Add a task first
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Finish report",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    
    # Complete the task
    chat_payload = {
        "user_id": USER_ID,
        "message": "Complete the task about finishing the report",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should contain tool call for complete_task
    assert "tool_calls" in data
    if data["tool_calls"]:
        assert data["tool_calls"][0]["name"] == "complete_task"

def test_update_task():
    """Test updating a task."""
    # Add a task first
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Call client",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    
    # Update the task
    chat_payload = {
        "user_id": USER_ID,
        "message": "Update the task to 'Call client about project'",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should contain tool call for update_task
    assert "tool_calls" in data
    if data["tool_calls"]:
        assert data["tool_calls"][0]["name"] == "update_task"

def test_delete_task():
    """Test deleting a task."""
    # Add a task first
    chat_payload = {
        "user_id": USER_ID,
        "message": "Add a new task: Delete this task",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    
    # Delete the task
    chat_payload = {
        "user_id": USER_ID,
        "message": "Delete the task about deleting this task",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should contain tool call for delete_task
    assert "tool_calls" in data
    if data["tool_calls"]:
        assert data["tool_calls"][0]["name"] == "delete_task"

if __name__ == "__main__":
    pytest.main([__file__])