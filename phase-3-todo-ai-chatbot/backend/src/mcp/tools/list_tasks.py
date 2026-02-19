from typing import Dict, Any
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from schemas import TaskListResponse
from services.task_service import TaskService

class ListTasksTool:
    """MCP tool for listing tasks - following official MCP specification exactly."""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            "name": "list_tasks",
            "description": "List all tasks for the user",
            "inputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status"
                    }
                },
                "required": []
            },
            "outputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "title": {"type": "string"},
                                "status": {"type": "string"},
                                "created_at": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "execution": {
                "taskSupport": "optional"
            },
            "annotations": {
                "destructive": False,
                "idempotent": True,
                "openWorld": True
            }
        }
    
    @staticmethod
    def execute(user_id: str, **kwargs) -> Dict[str, Any]:
        """Execute the list_tasks tool following MCP standards exactly."""
        try:
            # Import here to avoid circular imports
            import sys
            import os
            src_path = os.path.join(os.path.dirname(__file__), '..')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from database import engine
            from services.task_service import TaskService
            from sqlmodel import Session
            
            status = kwargs.get("status", "all")
            
            with Session(engine) as session:
                tasks = TaskService.get_tasks(session, user_id)

            task_list = [{
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": "completed" if task.is_completed else "pending",
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            } for task in tasks]

            return {
                "success": True,
                "message": f"Found {len(task_list)} tasks",
                "tasks": task_list
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to list tasks: {str(e)}"
            }