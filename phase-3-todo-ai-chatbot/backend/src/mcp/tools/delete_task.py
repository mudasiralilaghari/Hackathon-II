from typing import Dict, Any
import uuid
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from services.task_service import TaskService

class DeleteTaskTool:
    """MCP tool for deleting a task - following official MCP specification."""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            "name": "delete_task",
            "description": "Delete a task from the user's todo list",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    
    @staticmethod
    def execute(user_id: str, **kwargs) -> Dict[str, Any]:
        """Execute the delete_task tool following MCP standards."""
        try:
            task_id = kwargs.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "task_id parameter is required"
                }

            # Use database session to delete task
            from database import engine
            from sqlmodel import Session
            with Session(engine) as session:
                success = TaskService.delete_task(session=session, task_id=uuid.UUID(task_id), user_id=user_id)

            if success:
                return {
                    "success": True,
                    "message": f"Task with ID '{task_id}' deleted successfully"
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
                "message": f"Failed to delete task: {str(e)}"
            }