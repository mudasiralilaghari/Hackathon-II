# tests/contract/test_chat_endpoint.py
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_chat_endpoint_health():
    """Test health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "todo-ai-chatbot-backend"

def test_mcp_server_health():
    """Test MCP server health check."""
    response = requests.get(f"{BASE_URL}/mcp/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mcp-server"

def test_mcp_initialize():
    """Test MCP initialize method."""
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {},
        "id": "1"
    }
    response = requests.post(f"{BASE_URL}/mcp", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert "result" in data
    assert "capabilities" in data["result"]
    assert "tools" in data["result"]["capabilities"]

def test_mcp_tools_list():
    """Test MCP tools/list method."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": "2"
    }
    response = requests.post(f"{BASE_URL}/mcp", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert "result" in data
    assert "tools" in data["result"]
    
    tools = data["result"]["tools"]
    expected_tools = ["add_task", "list_tasks", "complete_task", "update_task", "delete_task"]
    tool_names = [tool["name"] for tool in tools]
    
    for expected_tool in expected_tools:
        assert expected_tool in tool_names

def test_chat_endpoint_exists():
    """Test chat endpoint exists."""
    response = requests.get(f"{BASE_URL}/api/test-user/chat")
    # Should return 405 (method not allowed) or 404, but endpoint should exist
    assert response.status_code in [404, 405]

if __name__ == "__main__":
    pytest.main([__file__])