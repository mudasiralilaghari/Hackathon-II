from typing import Dict, Any
import uuid
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from services.task_service import TaskService

class CompleteTaskTool:
    """MCP tool for marking a task as completed - following official MCP specification exactly."""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "inputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to mark as completed"
                    }
                },
                "required": ["task_id"]
            },
            "outputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "task": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "status": {"type": "string"},
                            "updated_at": {"type": "string"}
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
        """Execute the complete_task tool following MCP standards exactly."""
        try:
            # Validate user_id is provided
            if not user_id or not isinstance(user_id, str):
                return {
                    "success": False,
                    "error": "invalid_user_id",
                    "message": "Invalid or missing user_id parameter"
                }
            
            task_id = kwargs.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": "task_id_is_required",
                    "message": "task_id parameter is required"
                }
            
            # Enhanced security: validate user owns the task before operation
            if not TaskService.validate_user_owns_task(user_id, task_id):
                return {
                    "success": False,
                    "error": "access_denied",
                    "message": f"Access denied: User '{user_id}' does not own task '{task_id}'"
                }

            # Use toggle_task_completion from TaskService
            from database import engine
            from sqlmodel import Session
            with Session(engine) as session:
                task = TaskService.toggle_task_completion(session, uuid.UUID(task_id), user_id)
            
            if task:
                return {
                    "success": True,
                    "message": f"Task '{task.title}' marked as completed",
                    "task": {
                        "id": str(task.id),
                        "title": task.title,
                        "status": "completed" if task.is_completed else "pending",
                        "updated_at": task.updated_at.isoformat()
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "task_not_found_or_access_denied",
                    "message": f"Task with ID '{task_id}' not found or access denied"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to complete task: {str(e)}"
            }