# backend/src/agents/intent_mapping.py
from typing import Dict, Any, Optional, List, Tuple
import re

class IntentMapper:
    """Handles natural language intent to tool mapping for Todo AI Chatbot."""
    
    # Keyword mappings for intent detection
    INTENT_KEYWORDS = {
        "add": ["add", "create", "make", "new", "start", "begin"],
        "list": ["list", "show", "what", "all", "current", "existing", "have"],
        "complete": ["complete", "finish", "done", "mark", "check", "tick"],
        "update": ["update", "change", "edit", "modify", "rename", "adjust"],
        "delete": ["delete", "remove", "cancel", "discard", "eliminate"]
    }
    
    @staticmethod
    def detect_intent(message: str) -> Tuple[str, float]:
        """
        Detect the primary intent from a user message.
        
        Returns: (intent_type, confidence_score)
        """
        message_lower = message.lower()
        best_intent = None
        best_score = 0.0
        
        for intent, keywords in IntentMapper.INTENT_KEYWORDS.items():
            score = 0.0
            for keyword in keywords:
                if keyword in message_lower:
                    # Weight based on keyword importance
                    weight = 1.0 + (len(keyword) / 10.0)
                    score += weight
            
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent or "unknown", best_score / 10.0
    
    @staticmethod
    def extract_task_reference(message: str, conversation_history: List[Dict[str, Any]]) -> Optional[str]:
        """
        Extract task reference from message using contextual disambiguation.
        
        Supports references like:
        - "the first task"
        - "my grocery list"
        - "the one about groceries"
        - "that task"
        """
        message_lower = message.lower()
        
        # Look for ordinal references
        if "first" in message_lower or "1st" in message_lower:
            return "first"
        elif "second" in message_lower or "2nd" in message_lower:
            return "second"
        elif "last" in message_lower or "recent" in message_lower:
            return "last"
        
        # Look for title-based references
        for task in reversed(conversation_history):
            if task.get("type") == "assistant" and "task" in task.get("content", "").lower():
                # Simple matching - in real implementation would use NLP
                if any(word in message_lower for word in ["grocery", "shopping", "buy"]):
                    return "grocery"
        
        # Default to asking for clarification
        return None
    
    @staticmethod
    def get_tool_for_intent(intent: str) -> str:
        """Map intent to MCP tool name."""
        intent_to_tool = {
            "add": "add_task",
            "list": "list_tasks",
            "complete": "complete_task",
            "update": "update_task",
            "delete": "delete_task"
        }
        return intent_to_tool.get(intent, "unknown")
    
    @staticmethod
    def generate_confirmation_message(intent: str, task_info: Dict[str, Any] = None) -> str:
        """Generate friendly confirmation messages for tool execution."""
        confirmations = {
            "add": "I'll add '{title}' to your todo list. Let me do that for you...",
            "list": "Here are your current tasks:",
            "complete": "I'll mark '{title}' as completed. Is that correct?",
            "update": "I'll update '{title}' to '{new_title}'. Does that sound right?",
            "delete": "I'll delete '{title}'. Are you sure you want to remove this task?"
        }
        
        if intent in confirmations:
            if task_info and "title" in task_info:
                return confirmations[intent].format(title=task_info.get("title", "this task"))
            return confirmations[intent].format(title="this task")
        
        return "I can help you with that. What would you like me to do?"

# Example usage:
# intent, confidence = IntentMapper.detect_intent("Add a new task: Buy groceries")
# tool_name = IntentMapper.get_tool_for_intent(intent)
# confirmation = IntentMapper.generate_confirmation_message(intent, {"title": "Buy groceries"})