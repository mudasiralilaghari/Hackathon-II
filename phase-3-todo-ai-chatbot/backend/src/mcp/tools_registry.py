# backend/src/mcp/tools_registry.py
"""
Shared tools registry for MCP server.
This module provides a central registry that both main.py and mcp/server.py can use.
"""

# Global tools dictionary - this is the single source of truth
TOOLS = {}

def register_tool(name: str, tool_class):
    """Register a tool in the global registry."""
    TOOLS[name] = tool_class

def get_tool(name: str):
    """Get a tool by name."""
    return TOOLS.get(name)

def get_all_tools():
    """Get all registered tools."""
    return TOOLS

def is_tool_registered(name: str) -> bool:
    """Check if a tool is registered."""
    return name in TOOLS
