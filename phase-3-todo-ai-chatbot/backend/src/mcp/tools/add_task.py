from typing import Dict, Any
from pydantic import BaseModel
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from schemas import AddTaskRequest
from services.task_service import TaskService

class AddTaskTool:
    """MCP tool for adding a new task - following official MCP specification."""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        return {
            "name": "add_task",
            "description": "Add a new task to the user's todo list",
            "inputSchema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["title"]
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
                            "created_at": {"type": "string"}
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
        """Execute the add_task tool following MCP standards exactly."""
        try:
            # Validate user_id is provided
            if not user_id or not isinstance(user_id, str):
                return {
                    "success": False,
                    "error": "invalid_user_id",
                    "message": "Invalid or missing user_id parameter"
                }

            # Import here to avoid circular imports
            import sys
            import os
            src_path = os.path.join(os.path.dirname(__file__), '..')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from database import engine
            from models.task import TaskCreate
            from services.task_service import TaskService
            from sqlmodel import Session
            
            request = AddTaskRequest(**kwargs)
            
            # Create task using TaskService
            with Session(engine) as session:
                task_create = TaskCreate(
                    title=request.title,
                    description=request.description or ""
                )
                # Use a valid UUID for testing
                import uuid as uuid_lib
                try:
                    user_uuid = uuid_lib.UUID(user_id)
                except (ValueError, TypeError):
                    # Generate a consistent UUID for string user_ids
                    user_uuid = uuid_lib.uuid5(uuid_lib.NAMESPACE_DNS, user_id)
                
                task = TaskService.create_task(session, task_create, user_uuid)

                return {
                    "success": True,
                    "message": f"Task '{task.title}' added successfully",
                    "task": {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "status": "pending",
                        "created_at": task.created_at.isoformat()
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to add task: {str(e)}"
            }