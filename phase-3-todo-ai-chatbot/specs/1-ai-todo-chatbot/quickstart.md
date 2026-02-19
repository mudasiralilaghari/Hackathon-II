# Quickstart Guide: AI Todo Chatbot

**Feature**: 1-ai-todo-chatbot
**Date**: 2026-02-09

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon recommended)
- OpenAI API key
- Better Auth credentials

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/hackathon-II.git
cd hackathon-II/phase-3-todo-ai-chatbot
```

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
AUTH_JWT_SECRET=your_jwt_secret
MCP_SERVER_URL=http://localhost:8001
```

### 4. Database Setup
```bash
# Run database migrations
alembic upgrade head

# Or create tables manually if needed
python scripts/create_tables.py
```

### 5. Start MCP Server
```bash
uvicorn backend.src.mcp.server:app --host 0.0.0.0 --port 8001 --reload
```

### 6. Start Backend Server
```bash
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Start Frontend
```bash
cd frontend
npm install
npm start
```

## Testing the System

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/test-user/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "message": "Add a task: Call mom"
  }'
```

Expected response:
```json
{
  "conversation_id": "uuid-here",
  "response": "I've added 'Call mom' to your todo list.",
  "tool_calls": [
    {
      "name": "add_task",
      "parameters": {
        "user_id": "test-user",
        "title": "Call mom"
      }
    }
  ]
}
```

### Test Task Listing
```bash
curl -X POST http://localhost:8000/api/test-user/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "conversation_id": "uuid-from-previous-response",
    "message": "What tasks do I have?"
  }'
```

## Development Workflow

### Local Development
1. Make changes to backend code in `backend/src/`
2. Restart backend server with `--reload` flag
3. Test with curl or frontend
4. Run tests: `pytest tests/`

### Running Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Contract tests
pytest tests/contract/
```

### Debugging Tips
- Enable debug logging: `LOG_LEVEL=DEBUG uvicorn ...`
- Check MCP server logs for tool execution details
- Use database query tools to inspect conversation and task data
- Monitor request IDs for tracing across services

## Common Issues and Solutions

### 401 Unauthorized
- Check JWT token validity
- Verify AUTH_JWT_SECRET matches between services
- Ensure user_id in token matches request path parameter

### Tool Calls Not Executing
- Verify MCP server is running on port 8001
- Check network connectivity between backend and MCP server
- Validate tool schemas match expected parameters

### Slow Performance
- Check database indexing on user_id and conversation_id
- Monitor OpenAI API latency
- Consider connection pooling configuration

This quickstart guide provides everything needed to get the AI Todo Chatbot running locally for development and testing.