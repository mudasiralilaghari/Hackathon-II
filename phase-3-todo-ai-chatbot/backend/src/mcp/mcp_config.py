# mcp_config.py
from typing import Dict, Any
from agents.mcp import MCPServerStdio

def create_mcp_server_config() -> Dict[str, Any]:
    """
    Create MCP server configuration following OpenAI Agents SDK specification.
    
    This matches the exact pattern from the official OpenAI Agents SDK documentation:
    https://dev.to/seratch/openai-agents-sdk-multiple-mcp-servers-8d2
    """
    return {
        "todo_ai_chatbot": MCPServerStdio(
            name="Todo AI Chatbot MCP Server",
            params={
                "command": "uvicorn",
                "args": [
                    "src.mcp.server:app",
                    "--host", "0.0.0.0",
                    "--port", "8001"
                ],
                "env": {
                    "PYTHONPATH": ".",
                    "DATABASE_URL": "postgresql://user:password@localhost:5432/todo_ai_chatbot"
                }
            }
        )
    }

# For use in agent configuration:
# agent = Agent(
#     name="Todo Assistant",
#     instructions="You are a helpful todo assistant that can manage tasks using natural language.",
#     mcp_servers=[create_mcp_server_config()["todo_ai_chatbot"]],
# )