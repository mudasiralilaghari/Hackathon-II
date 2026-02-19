from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ToolCall(BaseModel):
    """Represents a tool call in the agent response."""
    name: str
    arguments: Dict[str, Any]
    id: str

class ToolResult(BaseModel):
    """Represents the result of a tool call."""
    tool_call_id: str
    content: str
    is_error: bool = False

class AgentResponse(BaseModel):
    """Structure for agent responses containing text and tool calls."""
    content: str
    tool_calls: List[ToolCall] = []
    tool_results: List[ToolResult] = []

class AddTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None

class TaskListResponse(BaseModel):
    tasks: List[dict]

class TaskResponse(BaseModel):
    task: dict