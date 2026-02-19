from typing import Dict, Any
import uuid
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from services.task_service import TaskService
from models.task import TaskUpdate

class UpdateTaskTool:
    """MCP tool for updating a task - following official MCP specification."""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            "name": "update_task",
            "description": "Update an existing task",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    }
                },
                "required": ["task_id"]
            }
        }
    
    @staticmethod
    def execute(user_id: str, **kwargs) -> Dict[str, Any]:
        """Execute the update_task tool following MCP standards."""
        try:
            task_id = kwargs.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "task_id parameter is required"
                }
            
            title = kwargs.get("title")
            description = kwargs.get("description")

            # Use database session to update task
            from database import engine
            from sqlmodel import Session
            with Session(engine) as session:
                task = TaskService.update_task(
                    session=session,
                    task_id=uuid.UUID(task_id),
                    task_update=TaskUpdate(title=title, description=description),
                    user_id=user_id
                )
            
            if task:
                return {
                    "success": True,
                    "message": f"Task '{task.title}' updated successfully",
                    "task": {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "status": "completed" if task.is_completed else "pending",
                        "updated_at": task.updated_at.isoformat()
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "task_not_found",
                    "message": f"Task with ID '{task_id}' not found or access denied"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to update task: {str(e)}"
            }