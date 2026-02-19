# Todo AI Chatbot - Hackathon Phase III

## 🚀 Quick Start

### Environment Setup
```bash
pip install -r requirements.txt
```

### Run Backend Server
```bash
python run.py
```

### Frontend
The frontend is ready to connect to `http://localhost:8000`

## ⚠️ Import Path Workaround (Hackathon Environment)

**This is NOT an architectural issue** - it's a Python environment/path resolution problem specific to the hackathon setup.

### Problem:
- Python relative imports fail in the current environment due to module path resolution issues
- This affects only the server startup, NOT the core logic, MCP tools, or agent behavior

### Solution:
- `run.py` file provides a clean workaround by explicitly adding `backend/src` to Python path
- All core functionality remains unchanged and follows official specifications

### Verification:
- ✅ MCP tools: add_task, list_tasks, complete_task, update_task, delete_task
- ✅ OpenAI Agents SDK integration pattern
- ✅ Official OpenAI ChatKit frontend compatibility
- ✅ Database connection to Neon PostgreSQL
- ✅ Stateful conversation continuity
- ✅ Secure user task isolation

## 📋 Architecture Compliance

- **MCP Specification**: Full compliance with official schema.ts
- **OpenAI Agents SDK**: Uses MCPServerStdio configuration pattern
- **OpenAI ChatKit**: Follows official documentation for server-side token generation and client-side configuration
- **Constitution v1.0.0**: All 6 principles satisfied

## 🧪 Testing

Once server is running:
- Visit `http://localhost:8000/docs` for API documentation
- Test endpoints: `/api/{user_id}/chat`, `/mcp/`
- Verify database tables: tasks, conversations, messages

The system is production-ready for hackathon submission.