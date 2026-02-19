# backend/src/agents/todo_agent.py
from agents import Agent, Runner
from .mcp.mcp_config import create_mcp_server_config
from .intent_mapping import IntentMapper
from typing import Dict, Any

def create_todo_agent():
    """
    Create Todo AI Agent following OpenAI Agents SDK specification.
    
    Based on official documentation pattern:
    https://dev.to/seratch/openai-agents-sdk-multiple-mcp-servers-8d2
    
    Key requirements from OpenAI Agents SDK:
    - Use mcp_servers parameter for MCP integration
    - Agent instructions should be clear and focused
    - Tools are discovered automatically via MCP server's tools/list endpoint
    """
    mcp_servers = list(create_mcp_server_config().values())
    
    # System prompt following OpenAI Agents SDK best practices
    system_prompt = """You are a helpful todo assistant that helps users manage their tasks using natural language.
    
    ## Your Capabilities
    You can help with:
    - ✅ Adding new tasks with natural language descriptions
    - ✅ Listing all current tasks
    - ✅ Marking tasks as completed
    - ✅ Updating existing tasks
    - ✅ Deleting tasks
    
    ## How to Use Tools
    When a user asks you to perform a task operation, use the appropriate tool:
    - "add" → add_task tool
    - "list", "show", "what do I have" → list_tasks tool  
    - "complete", "finish", "done" → complete_task tool
    - "update", "change", "edit" → update_task tool
    - "delete", "remove", "cancel" → delete_task tool
    
    ## Response Guidelines
    1. Always confirm actions before executing them
    2. Be friendly and helpful in your responses
    3. If you need clarification about which task to modify, ask the user
    4. Use natural language in your responses, not technical jargon
    
    ## Context Awareness
    - Remember the conversation history
    - Use contextual disambiguation for task references (e.g., "the first task", "my grocery list")
    - If multiple tasks match, ask for clarification
    
    You have access to the following tools through the MCP server:
    {tools_list}
    
    Start by greeting the user and asking how you can help with their todos.
    """
    
    agent = Agent(
        name="Todo Assistant",
        instructions=system_prompt,
        mcp_servers=mcp_servers,
        # Note: tools parameter is optional when using mcp_servers - tools are discovered automatically
    )
    
    return agent

async def run_todo_agent(input_text: str, conversation_history: list = None):
    """Run the todo agent with the given input."""
    agent = create_todo_agent()
    
    # In real implementation, this would use the intent mapping logic
    # For now, we'll use the basic agent runner
    result = await Runner.run(agent, input=input_text)
    return result

# Helper functions for intent-based processing
def get_intent_and_tool(message: str) -> tuple:
    """Get intent and corresponding tool for a message."""
    intent, confidence = IntentMapper.detect_intent(message)
    tool_name = IntentMapper.get_tool_for_intent(intent)
    return intent, tool_name, confidence

def generate_confirmation_message(intent: str, task_info: Dict[str, Any] = None) -> str:
    """Generate friendly confirmation messages."""
    return IntentMapper.generate_confirmation_message(intent, task_info)