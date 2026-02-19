# Implementation Plan: AI Todo Chatbot

**Branch**: `1-ai-todo-chatbot` | **Date**: 2026-02-09 | **Spec**: [specs/1-ai-todo-chatbot/spec.md]
**Input**: Feature specification from `/specs/1-ai-todo-chatbot/spec.md`

## Summary

This plan outlines the architecture and design for an AI-powered todo chatbot that uses natural language processing through an OpenAI Agent that orchestrates MCP tools for task management. The system follows the constitution principles of agent-first design, tool-driven intelligence, stateless backend, deterministic persistence, reusable intelligence, and zero manual coding.

The core architecture consists of: Frontend (OpenAI ChatKit), FastAPI Backend, OpenAI Agents SDK (Agent + Runner), MCP Server (Official MCP SDK), and Neon PostgreSQL Database. Data flows from user input → backend → agent → MCP tools → database → response, maintaining strict statelessness throughout.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, Neon PostgreSQL
**Storage**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest, contract testing, integration testing
**Target Platform**: Linux server (cloud-deployable)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <500ms p95 latency for chat requests, 100+ concurrent users
**Constraints**: Strict statelessness, MCP tool-only data manipulation, no frontend business logic
**Scale/Scope**: 1000+ users, 10k+ tasks, production-ready for hackathon

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **I. Agent-First Design**: All business logic flows through AI agents - satisfied by agent handling intent interpretation and tool selection
✅ **II. Tool-Driven Intelligence**: Agents act only via MCP tools - satisfied by requiring all task operations through defined MCP tools
✅ **III. Stateless Backend**: No in-memory session state - satisfied by fetching conversation history from DB on every request
✅ **IV. Deterministic Persistence**: All state stored in database - satisfied by persisting conversations, messages, and tasks in PostgreSQL
✅ **V. Reusable Intelligence**: Patterns and tools designed for reuse - satisfied by modular MCP tool implementations and agent patterns
✅ **VI. Zero Manual Coding**: Implementation via Claude Code iterations - satisfied by following Agentic Dev Stack workflow

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── task.py
│   ├── services/
│   │   ├── chat_service.py
│   │   └── conversation_service.py
│   ├── agents/
│   │   ├── todo_agent.py
│   │   └── agent_runner.py
│   ├── mcp/
│   │   ├── server.py
│   │   ├── tools/
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── update_task.py
│   │   │   └── delete_task.py
│   │   └── schemas.py
│   ├── api/
│   │   └── chat.py
│   └── main.py
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface.tsx
│   ├── pages/
│   │   └── ChatPage.tsx
│   └── services/
│       └── api.ts
└── tests/

database/
├── migrations/
│   └── alembic/
└── schema.sql
```

**Structure Decision**: Web application structure with separate backend and frontend directories, following the constitution's architecture standards for single stateless chat endpoint and horizontal scalability requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | All constitution principles satisfied with current design |

## Phase 0: Research & Clarification

**Purpose**: Resolve any remaining ambiguities and establish technical foundations

### Research Tasks

1. **Research MCP SDK integration patterns** for FastAPI backend
   - Decision: Use official MCP SDK with FastAPI middleware pattern
   - Rationale: Official SDK provides best compatibility and security
   - Alternatives considered: Custom MCP implementation (rejected for complexity and maintenance)

2. **Research OpenAI Agents SDK best practices**
   - Decision: Use system prompt with clear tool selection instructions
   - Rationale: Maximizes reliability of tool selection for task operations
   - Alternatives considered: Fine-tuned model (rejected for complexity and cost)

3. **Research SQLModel with Neon PostgreSQL performance**
   - Decision: Use async SQLAlchemy with connection pooling
   - Rationale: Optimized for high-concurrency chat workloads
   - Alternatives considered: Raw SQL queries (rejected for maintainability)

4. **Research ChatKit integration patterns**
   - Decision: Use standard ChatKit with custom message formatting
   - Rationale: Minimal customization required per constitution frontend standards
   - Alternatives considered: Custom UI framework (rejected for violating frontend standards)

## Phase 1: Design & Contracts

**Purpose**: Define data models, API contracts, and implementation details

### Data Model Design

**Conversation Entity**:
- id: UUID (primary key)
- user_id: string (indexed, foreign key reference)
- created_at: datetime
- last_activity: datetime
- metadata: JSON (optional)

**Message Entity**:
- id: UUID (primary key)
- conversation_id: UUID (indexed, foreign key to Conversation)
- user_id: string (indexed, foreign key reference)
- type: enum (user/assistant)
- content: text
- timestamp: datetime
- tool_calls: JSON (array of tool call objects)
- sequence_number: integer (for ordering)

**Task Entity**:
- id: UUID (primary key)
- user_id: string (indexed, foreign key reference)
- title: string (indexed)
- description: text (nullable)
- status: enum (pending/completed)
- created_at: datetime
- updated_at: datetime
- metadata: JSON (optional)

**Validation Rules**:
- user_id must match authenticated user for all operations
- task titles can be duplicated per user (resolved via contextual disambiguation)
- conversation_id must be provided for resume operations
- timestamps generated by application (not database) for consistency

### API Contracts

**POST /api/{user_id}/chat**
- Request: { "conversation_id": "uuid", "message": "string" }
- Response: { "conversation_id": "uuid", "response": "string", "tool_calls": [{"name": "string", "parameters": {}}] }
- Authentication: Bearer token with user_id validation
- Rate limiting: 10 requests/second per user_id

**MCP Tool Schemas**:

1. **add_task**
   - Parameters: { "user_id": "string", "title": "string", "description": "string?" }
   - Returns: { "task_id": "string", "title": "string", "status": "string" }

2. **list_tasks**
   - Parameters: { "user_id": "string", "filter": "all|pending|completed" }
   - Returns: { "tasks": [{"id": "string", "title": "string", "status": "string", "created_at": "string"}] }

3. **complete_task**
   - Parameters: { "user_id": "string", "task_id": "string" }
   - Returns: { "task_id": "string", "status": "completed" }

4. **update_task**
   - Parameters: { "user_id": "string", "task_id": "string", "title": "string?", "description": "string?" }
   - Returns: { "task_id": "string", "title": "string", "description": "string", "status": "string" }

5. **delete_task**
   - Parameters: { "user_id": "string", "task_id": "string" }
   - Returns: { "task_id": "string", "deleted": true }

### Quickstart Guide

1. **Setup**: `pip install -r requirements.txt`
2. **Database**: Run migrations with `alembic upgrade head`
3. **MCP Server**: Start with `uvicorn backend.src.mcp.server:app --host 0.0.0.0 --port 8001`
4. **Backend**: Start with `uvicorn backend.src.main:app --host 0.0.0.0 --port 8000`
5. **Frontend**: `npm start` in frontend directory
6. **Test**: Send POST request to `/api/test-user/chat` with JSON body

## Phase 2: Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 0: Research and clarify technical foundations
2. Complete Phase 1: Design data models, contracts, and quickstart
3. Implement core chat endpoint with basic agent functionality
4. Implement minimal MCP tools (add_task, list_tasks)
5. **STOP and VALIDATE**: Test User Story 1 independently (natural language todo management)
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Foundation: Data models, MCP server, basic chat endpoint
2. Add User Story 1: Natural language todo management (add, list, complete, update, delete)
3. Add User Story 2: Conversation continuity (resume conversations, context preservation)
4. Add User Story 3: Secure task isolation (user ownership enforcement)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Foundation together
2. Once Foundation is done:
   - Developer A: User Story 1 (core functionality)
   - Developer B: User Story 2 (conversation continuity)
   - Developer C: User Story 3 (security/isolation)
3. Stories complete and integrate independently

## Architecture Details

### High-Level Architecture

```
[Frontend: ChatKit] 
       ↓ (HTTP POST /api/{user_id}/chat)
[Backend: FastAPI] 
       ↓ (Agent orchestration)
[OpenAI Agent] → [MCP Tools] → [Database: Neon PostgreSQL]
       ↑
[Response formatting]
       ↓
[Backend: FastAPI] → [Frontend: ChatKit]
```

### Backend Design

- Single chat endpoint handles all user interactions
- Request lifecycle: validate user_id → fetch conversation history → run agent → execute MCP tools → store messages → return response
- Conversation reconstruction: query all messages for conversation_id, ordered by timestamp
- Error handling: standardized error responses with user-friendly messages
- Rate limiting: per user_id to prevent abuse

### Agent Design

- System prompt: "You are a helpful todo assistant. You must use the provided tools to manage tasks. Never modify data directly."
- Tool selection strategy: 
  1. Parse user intent from natural language
  2. Match to closest tool based on keywords and context
  3. For ambiguous cases, use contextual disambiguation first, then ask clarification
- Tool chaining: Allow up to 3 sequential tool calls per turn (e.g., list then delete)
- Fallback behavior: When intent unclear, ask clarifying question with examples
- Confirmation patterns: "I've added 'Call mom' to your todo list" instead of technical jargon

### MCP Server Design

- MCP server runs as separate service on port 8001
- Each tool validates user_id against provided parameter
- Tools use SQLModel for database operations with transaction safety
- Error contracts: consistent format with error_code and user_message
- Statelessness: each tool call is independent with no shared state
- Authorization: tools verify user ownership before operations

### Database Design

- Tables: conversations, messages, tasks
- Indexes: user_id (all tables), conversation_id (messages), title (tasks), status (tasks)
- Foreign keys: messages.conversation_id → conversations.id, tasks.user_id → conversations.user_id
- Ownership enforcement: WHERE user_id = :provided_user_id in all queries
- Migration approach: Alembic with versioned migrations
- Data lifecycle: hard deletes for tasks (per constitution constraints), soft deletes not used

### Frontend Integration

- ChatKit initialized with API endpoint configuration
- Message format: { role: "user"/"assistant", content: string, tool_calls?: array }
- Assistant responses include tool_call information for debugging
- Error states: display user-friendly error messages from backend
- Loading states: show spinner during agent processing

### Authentication & Security

- Better Auth integration: JWT tokens with user_id claim
- user_id derived from JWT token and validated in middleware
- Access control: enforced at API layer (FastAPI) and MCP tool layer
- Cross-user protection: WHERE user_id = :authenticated_user_id in all database queries
- Suspicious activity: log failed authorization attempts

### Non-Functional Requirements

- Scalability: Stateless design enables horizontal scaling; load balancer distributes requests
- Failure recovery: Database replication ensures high availability; server restarts don't affect data
- Logging: Structured logs with request_id, user_id, operation_type, duration
- Observability: Trace IDs for request correlation, metrics for latency and error rates

## Development Workflow

### Agentic Dev Stack Implementation

1. **Write spec**: Completed (specs/1-ai-todo-chatbot/spec.md)
2. **Generate plan**: Current document (plan.md)
3. **Break into tasks**: Next step with /sp.tasks
4. **Implement via AI**: Claude Code iterations for each task

### Separation of Concerns

- **Backend team**: API endpoints, service logic, database models
- **Agent team**: Agent prompts, tool selection logic, response generation
- **MCP team**: Tool implementations, validation, database operations
- **Frontend team**: ChatKit integration, UI presentation

### Checkpoints for Validation

- **Foundation Ready**: Database schema, MCP server, basic chat endpoint
- **MVP Ready**: User Story 1 fully functional and tested
- **Complete Ready**: All user stories implemented and integrated
- **Production Ready**: Performance testing, security review, observability setup

## Assumptions & Trade-offs

### Explicit Assumptions

- User authentication handled by external service (Better Auth)
- OpenAI API available and responsive
- Neon PostgreSQL database available and configured
- Network connectivity between backend, MCP server, and database

### Known Limitations

- No offline capability (requires network for AI and database)
- Limited natural language understanding for complex multi-step requests
- Task titles can be duplicated (resolved via contextual disambiguation)
- Maximum 3 tool calls per turn (prevents infinite loops)

### Features Excluded (Per Out-of-Scope)

- Reminders, notifications, or scheduling
- File uploads or attachments
- Voice or multimodal input
- Advanced permissions or role-based access
- UI customization beyond ChatKit defaults

## Success Definition

The project is considered successful when:
- User can add, list, complete, update, and delete tasks using natural language commands
- Agent always uses MCP tools for task operations (100% compliance)
- Conversation context persists across server restarts (100% reliability)
- Users can only access their own tasks and conversations (0% cross-user leakage)
- System handles 100+ concurrent users with <500ms p95 latency
- 95% of user intents are correctly interpreted and acted upon

This plan provides a complete architectural blueprint that a different AI agent could implement without asking clarifying questions, following the constitution principles and specification requirements.