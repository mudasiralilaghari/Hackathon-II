import uvicorn
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json

# Initialize API Router
app = APIRouter()

# Import shared tools registry (this is the SAME dictionary that main.py populates)
from .tools_registry import TOOLS, get_all_tools, is_tool_registered

class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: Dict[str, Any]
    id: str

class JSONRPCResponse(BaseModel):
    jsonrpc: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: str

# Standard JSON-RPC error codes from official specification
JSONRPC_ERROR_CODES = {
    "PARSE_ERROR": -32700,
    "INVALID_REQUEST": -32600,
    "METHOD_NOT_FOUND": -32601,
    "INVALID_PARAMS": -32602,
    "INTERNAL_ERROR": -32603
}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp-server"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP endpoint following exact JSON-RPC 2.0 specification from official schema.ts."""
    try:
        # Parse JSON-RPC request
        body = await request.json()
        
        # Validate JSON-RPC version
        if body.get("jsonrpc") != "2.0":
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": JSONRPC_ERROR_CODES["INVALID_REQUEST"],
                    "message": "Invalid JSON-RPC version. Expected '2.0'"
                },
                "id": body.get("id")
            }
        
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        
        # Handle standard MCP methods as per official specification
        if method == "initialize":
            # Return initialize response as per official spec
            return {
                "jsonrpc": "2.0",
                "result": {
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"listChanged": False},
                        "prompts": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "Todo AI Chatbot MCP Server",
                        "version": "1.0.0"
                    }
                },
                "id": request_id
            }
        
        elif method == "tools/list":
            # Import tools directly to ensure we get the registered ones
            try:
                from .tools.add_task import AddTaskTool
                from .tools.list_tasks import ListTasksTool
                from .tools.complete_task import CompleteTaskTool
                from .tools.update_task import UpdateTaskTool
                from .tools.delete_task import DeleteTaskTool
                
                current_tools = {
                    "add_task": AddTaskTool,
                    "list_tasks": ListTasksTool,
                    "complete_task": CompleteTaskTool,
                    "update_task": UpdateTaskTool,
                    "delete_task": DeleteTaskTool
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": JSONRPC_ERROR_CODES["INTERNAL_ERROR"],
                        "message": f"Failed to load tools: {str(e)}"
                    },
                    "id": request_id
                }
            
            # Return list of available tools with their schemas as per official spec
            tools_list = []
            for tool_name, tool_class in current_tools.items():
                schema = tool_class.get_schema()
                tools_list.append({
                    "name": schema["name"],
                    "description": schema["description"],
                    "inputSchema": schema["inputSchema"],
                    "outputSchema": schema.get("outputSchema"),
                    "execution": schema.get("execution"),
                    "annotations": schema.get("annotations")
                })

            return {
                "jsonrpc": "2.0",
                "result": {"tools": tools_list},
                "id": request_id
            }
        
        elif method.startswith("tools/"):
            # Import tools directly to ensure we get the registered ones
            try:
                from .tools.add_task import AddTaskTool
                from .tools.list_tasks import ListTasksTool
                from .tools.complete_task import CompleteTaskTool
                from .tools.update_task import UpdateTaskTool
                from .tools.delete_task import DeleteTaskTool
                
                current_tools = {
                    "add_task": AddTaskTool,
                    "list_tasks": ListTasksTool,
                    "complete_task": CompleteTaskTool,
                    "update_task": UpdateTaskTool,
                    "delete_task": DeleteTaskTool
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": JSONRPC_ERROR_CODES["INTERNAL_ERROR"],
                        "message": f"Failed to load tools: {str(e)}"
                    },
                    "id": request_id
                }
            
            # Execute tool call as per official spec
            tool_name = method.split("/", 1)[1]

            if tool_name not in current_tools:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": JSONRPC_ERROR_CODES["METHOD_NOT_FOUND"],
                        "message": f"Method '{method}' not found"
                    },
                    "id": request_id
                }

            tool_class = current_tools[tool_name]
            try:
                # Extract user_id from params or headers
                user_id = params.pop("user_id", None) or request.headers.get("X-User-ID", "test-user")

                result = tool_class.execute(user_id=user_id, **params)
                
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": JSONRPC_ERROR_CODES["INTERNAL_ERROR"],
                        "message": f"Internal error: {str(e)}"
                    },
                    "id": request_id
                }
        
        elif method == "ping":
            # Ping method for liveness checks as per official spec
            return {
                "jsonrpc": "2.0",
                "result": {"pong": True},
                "id": request_id
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": JSONRPC_ERROR_CODES["METHOD_NOT_FOUND"],
                    "message": f"Method '{method}' not found"
                },
                "id": request_id
            }
            
    except json.JSONDecodeError as e:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": JSONRPC_ERROR_CODES["PARSE_ERROR"],
                "message": f"Parse error: {str(e)}"
            },
            "id": None
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": JSONRPC_ERROR_CODES["INTERNAL_ERROR"],
                "message": f"Internal error: {str(e)}"
            },
            "id": None
        }

# Register tools on startup (tools are registered in main.py lifespan)
# This function is kept for backward compatibility but not used
def setup_startup_event(app_instance):
    pass  # Tools are now registered in main.py lifespan event

# For standalone running
if __name__ == "__main__":
    from fastapi import FastAPI
    standalone_app = FastAPI(title="MCP Server", description="MCP server for Todo AI Chatbot following official specification exactly")
    
    # Add the router to the standalone app
    standalone_app.include_router(app)
    
    # Setup startup event for the standalone app
    setup_startup_event(standalone_app)
    
    uvicorn.run(standalone_app, host="0.0.0.0", port=8001)
else:
    # When imported as a module, setup the startup event for the router's parent app
    from fastapi import FastAPI
    # We'll set up the startup in main.py after including the router
    pass