# backend/src/agents/mcp/mcp_config.py
from agents import MCPServerStdio
import os

def create_mcp_server_config():
    """
    Create MCP server configuration following OpenAI Agents SDK specification.
    
    Based on official documentation:
    https://platform.openai.com/docs/guides/tools-mcp
    
    Returns a dictionary of MCP server configurations that can be passed to Agent.
    """
    # Get the path to the MCP server script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_src_dir = os.path.dirname(os.path.dirname(current_dir))
    mcp_server_path = os.path.join(backend_src_dir, 'mcp', 'server.py')
    
    # Create MCP server configuration
    # This tells the Agent how to connect to the MCP server
    mcp_config = {
        "todo_mcp_server": MCPServerStdio(
            name="Todo MCP Server",
            command="python",
            args=[mcp_server_path],
            # Optional: environment variables for the MCP server
            env={
                "PYTHONPATH": backend_src_dir,
            }
        )
    }
    
    return mcp_config
