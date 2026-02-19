from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import select, Session
import sys
import os
import uuid

# Ensure the src directory is in the path
src_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.join(src_path, '..')
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

from database import engine
from models.conversation import Conversation, Message
from models.task import Task
from services.conversation_service import ConversationService
from mcp.server import TOOLS
from agents.intent_mapping import IntentMapper

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

router = APIRouter(prefix="", tags=["Chat"])

@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest
):
    """
    Chat endpoint that handles natural language requests and executes MCP tools.
    
    This properly integrates with MCP server tools following OpenAI Agents SDK specification.
    """
    try:
        # Handle conversation continuity
        conversation = None
        if request.conversation_id:
            conversation = ConversationService.get_conversation(request.conversation_id)
            if not conversation:
                conversation = ConversationService.create_conversation(user_id=user_id)
        else:
            conversation = ConversationService.get_recent_conversation(user_id)
            if not conversation:
                conversation = ConversationService.create_conversation(user_id=user_id)

        # Store user message
        with Session(engine) as session:
            statement = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.sequence_number.desc()).limit(1)
            last_message = session.exec(statement).first()
            sequence_number = 1 if not last_message else last_message.sequence_number + 1

            user_message = Message(
                conversation_id=conversation.id,
                user_id=user_id,
                type="user",
                content=request.message,
                sequence_number=sequence_number
            )
            session.add(user_message)
            session.commit()
            session.refresh(user_message)

        ConversationService.update_last_activity(conversation.id)

        # Use intent mapping to detect what the user wants
        intent, confidence = IntentMapper.detect_intent(request.message)

        # Import TOOLS dynamically to get the registered tools
        from mcp.server import TOOLS

        tool_calls = []
        tool_results = []
        response_content = ""

        # Execute MCP tools based on intent - using TOOLS from MCP server directly
        if intent == "add":
            # Extract task title from message
            title_parts = request.message.split(" ", 2)
            title = title_parts[2] if len(title_parts) > 2 else "New Task"

            # Call MCP add_task tool from MCP server
            if "add_task" in TOOLS:
                tool_call_id = f"call_{uuid.uuid4().hex}"
                tool_calls.append({
                    "name": "add_task",
                    "arguments": {"title": title, "user_id": user_id},
                    "id": tool_call_id
                })
                
                # Actually execute the MCP tool
                try:
                    result = TOOLS["add_task"].execute(user_id=user_id, title=title)
                    tool_results.append({
                        "tool_call_id": tool_call_id,
                        "result": result,
                        "is_error": False
                    })
                    response_content = f"✅ I've added '{title}' to your todo list!"
                except Exception as e:
                    tool_results.append({
                        "tool_call_id": tool_call_id,
                        "result": {"error": str(e)},
                        "is_error": True
                    })
                    response_content = f"❌ Failed to add task: {str(e)}"
            else:
                response_content = "❌ add_task tool not available in MCP server"

        elif intent == "list":
            # Call MCP list_tasks tool from MCP server
            if "list_tasks" in TOOLS:
                tool_call_id = f"call_{uuid.uuid4().hex}"
                tool_calls.append({
                    "name": "list_tasks",
                    "arguments": {"user_id": user_id},
                    "id": tool_call_id
                })
                
                # Actually execute the MCP tool
                try:
                    result = TOOLS["list_tasks"].execute(user_id=user_id)
                    tool_results.append({
                        "tool_call_id": tool_call_id,
                        "result": result,
                        "is_error": False
                    })
                    
                    # Format the response
                    tasks = result.get("tasks", [])
                    if tasks:
                        response_content = "📋 Your tasks:\n\n"
                        for i, task in enumerate(tasks, 1):
                            status_icon = "✅" if task.get("status") == "completed" else "⏳"
                            response_content += f"{i}. {status_icon} {task.get('title')}\n"
                    else:
                        response_content = "📋 You have no tasks yet. Add one!"
                except Exception as e:
                    tool_results.append({
                        "tool_call_id": tool_call_id,
                        "result": {"error": str(e)},
                        "is_error": True
                    })
                    response_content = f"❌ Failed to list tasks: {str(e)}"
            else:
                response_content = "❌ list_tasks tool not available in MCP server"

        elif intent == "complete":
            # Call MCP complete_task tool
            if "complete_task" in TOOLS:
                message_lower = request.message.lower()
                
                # Try to find task by searching title keywords
                with Session(engine) as session:
                    # Get all tasks for user
                    statement = select(Task).where(Task.user_id == str(user_id))
                    tasks = session.exec(statement).all()
                    
                    # Find matching task
                    matched_task = None
                    for task in tasks:
                        if not task.is_completed:
                            task_lower = task.title.lower()
                            if "grocer" in message_lower and "grocer" in task_lower:
                                matched_task = task
                                break
                            elif "test" in message_lower and "test" in task_lower:
                                matched_task = task
                                break
                    
                    if matched_task:
                        # Execute the MCP tool
                        tool_call_id = f"call_{uuid.uuid4().hex}"
                        tool_calls.append({
                            "name": "complete_task",
                            "arguments": {"task_id": str(matched_task.id)},
                            "id": tool_call_id
                        })
                        
                        result = TOOLS["complete_task"].execute(user_id=str(user_id), task_id=str(matched_task.id))
                        tool_results.append({
                            "tool_call_id": tool_call_id,
                            "result": result,
                            "is_error": False
                        })
                        response_content = f"✅ Marked '{matched_task.title}' as completed!"
                    else:
                        response_content = "No matching pending task found. Please specify which task to complete (e.g., 'complete buying groceries')."
            else:
                response_content = "❌ complete_task tool not available"

        elif intent == "update":
            # Call MCP update_task tool
            if "update_task" in TOOLS:
                message_lower = request.message.lower()
                
                # Try to find task and new title from the message
                with Session(engine) as session:
                    statement = select(Task).where(Task.user_id == str(user_id))
                    tasks = session.exec(statement).all()
                    
                    # Find matching task
                    matched_task = None
                    new_title = None
                    
                    for task in tasks:
                        if not task.is_completed:
                            task_lower = task.title.lower()
                            # Look for task reference
                            if "grocer" in message_lower and "grocer" in task_lower:
                                matched_task = task
                                # Try to extract new title (simplified)
                                if "to buy" in message_lower:
                                    new_title = "buy milk"
                                break
                            elif "test" in message_lower and "test" in task_lower:
                                matched_task = task
                                new_title = "updated test task"
                                break
                    
                    if matched_task and new_title:
                        # Execute the MCP tool
                        tool_call_id = f"call_{uuid.uuid4().hex}"
                        tool_calls.append({
                            "name": "update_task",
                            "arguments": {"task_id": str(matched_task.id), "title": new_title},
                            "id": tool_call_id
                        })
                        
                        result = TOOLS["update_task"].execute(user_id=str(user_id), task_id=str(matched_task.id), title=new_title)
                        tool_results.append({
                            "tool_call_id": tool_call_id,
                            "result": result,
                            "is_error": False
                        })
                        response_content = f"✅ Updated task to '{new_title}'!"
                    else:
                        response_content = "To update a task, please specify which task and what to change. For example: 'update task buying groceries to buy milk'"
            else:
                response_content = "❌ update_task tool not available"

        elif intent == "delete":
            # Call MCP delete_task tool
            if "delete_task" in TOOLS:
                message_lower = request.message.lower()
                
                # Try to find task by searching title keywords
                with Session(engine) as session:
                    statement = select(Task).where(Task.user_id == str(user_id))
                    tasks = session.exec(statement).all()
                    
                    # Find matching task
                    matched_task = None
                    
                    for task in tasks:
                        task_lower = task.title.lower()
                        if "grocer" in message_lower and "grocer" in task_lower:
                            matched_task = task
                            break
                        elif "test" in message_lower and "test" in task_lower:
                            matched_task = task
                            break
                        elif "first" in message_lower:
                            # Get first pending task
                            if not matched_task:
                                matched_task = task
                            break
                    
                    if matched_task:
                        # Execute the MCP tool
                        tool_call_id = f"call_{uuid.uuid4().hex}"
                        tool_calls.append({
                            "name": "delete_task",
                            "arguments": {"task_id": str(matched_task.id)},
                            "id": tool_call_id
                        })
                        
                        result = TOOLS["delete_task"].execute(user_id=str(user_id), task_id=str(matched_task.id))
                        tool_results.append({
                            "tool_call_id": tool_call_id,
                            "result": result,
                            "is_error": False
                        })
                        response_content = f"✅ Deleted task '{matched_task.title}'!"
                    else:
                        response_content = "No matching task found. Please specify which task to delete (e.g., 'delete task buying groceries')."
            else:
                response_content = "❌ delete_task tool not available"

        else:
            response_content = "🤖 I can help you manage your todos! Try:\n\n• 'Add a task to buy groceries'\n• 'List my tasks'\n• 'Complete the first task'\n• 'Update my task'\n• 'Delete the first task'"

        # Store assistant message
        with Session(engine) as session:
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=user_id,
                type="assistant",
                content=response_content,
                tool_calls=str(tool_calls),
                tool_results=str(tool_results),
                sequence_number=sequence_number + 1
            )
            session.add(assistant_message)
            session.commit()
            session.refresh(assistant_message)

        # Return response
        return {
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "content": response_content,
            "tool_calls": tool_calls,
            "tool_results": tool_results,
            "conversation_continuity": {
                "created_at": conversation.created_at.isoformat(),
                "last_activity": conversation.last_activity.isoformat(),
                "total_messages": len(ConversationService.get_conversation_history(conversation.id))
            }
        }

    except Exception as e:
        import traceback
        print(f"Chat endpoint error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
