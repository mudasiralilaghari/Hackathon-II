---
description: "Task list template for feature implementation"
---

# Tasks: AI Todo Chatbot

**Input**: Design documents from `/specs/1-ai-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web application** (when "frontend" + "backend" detected)
  - backend/src/
    - models/
    - services/
    - agents/
    - mcp/
    - api/
    - main.py
  - frontend/src/
    - components/
    - pages/
    - services/
  - database/migrations/

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK dependencies
- [ ] T003 [P] Configure linting and formatting tools (pylint, black, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [ ] T004 Setup database schema and migrations framework using SQLModel and Alembic
- [ ] T005 [P] Create SQLModel base configuration with Neon PostgreSQL connection
- [ ] T006 [P] Implement database connection lifecycle management with async context

### MCP Server Foundation

- [ ] T007 Setup MCP server using Official MCP SDK
- [ ] T008 [P] Configure MCP server to run on port 8001
- [ ] T009 [P] Implement MCP server health check endpoint

### Authentication Foundation

- [ ] T010 Setup Better Auth integration with JWT validation middleware
- [ ] T011 [P] Implement user_id extraction and validation middleware for FastAPI

### Agent Foundation

- [ ] T012 Setup OpenAI Agents SDK configuration
- [ ] T013 [P] Implement agent runner service for executing agent logic
- [ ] T014 [P] Configure OpenAI API client with rate limiting

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1) 🎯 MVP

**Goal**: User can manage todos using natural language commands without learning specific syntax

**Independent Test**: A user can add, list, complete, update, and delete tasks through natural language commands with the system correctly interpreting intent and executing appropriate MCP tool calls

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [ ] T015 [P] [US1] Contract test for POST /api/{user_id}/chat in tests/contract/test_chat_endpoint.py
- [ ] T016 [P] [US1] Integration test for natural language task creation, listing, completion, update, deletion in tests/integration/test_natural_language_todos.py

### Implementation for User Story 1

#### Data Models
- [ ] T017 [P] [US1] Create Task model in backend/src/models/task.py
- [ ] T018 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [ ] T019 [P] [US1] Create Message model in backend/src/models/message.py

#### Services
- [ ] T020 [US1] Implement ConversationService in backend/src/services/conversation_service.py (handles conversation creation, history retrieval)
- [ ] T021 [US1] Implement TaskService in backend/src/services/task_service.py (handles task operations with user_id validation)

#### MCP Tools
- [ ] T022 [P] [US1] Implement add_task tool in backend/src/mcp/tools/add_task.py
- [ ] T023 [P] [US1] Implement list_tasks tool in backend/src/mcp/tools/list_tasks.py
- [ ] T024 [P] [US1] Implement complete_task tool in backend/src/mcp/tools/complete_task.py
- [ ] T025 [P] [US1] Implement update_task tool in backend/src/mcp/tools/update_task.py
- [ ] T026 [P] [US1] Implement delete_task tool in backend/src/mcp/tools/delete_task.py

#### Agent Logic
- [ ] T027 [US1] Implement todo_agent system prompt in backend/src/agents/todo_agent.py
- [ ] T028 [US1] Implement intent-to-tool mapping logic in backend/src/agents/todo_agent.py
- [ ] T029 [US1] Implement contextual disambiguation for ambiguous task references in backend/src/agents/todo_agent.py
- [ ] T030 [US1] Implement confirmation response templates in backend/src/agents/todo_agent.py

#### API Endpoint
- [ ] T031 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat.py
- [ ] T032 [US1] Implement conversation creation logic in backend/src/api/chat.py
- [ ] T033 [US1] Implement conversation history reconstruction in backend/src/api/chat.py
- [ ] T034 [US1] Implement agent execution lifecycle in backend/src/api/chat.py
- [ ] T035 [US1] Implement message persistence (user and assistant) in backend/src/api/chat.py
- [ ] T036 [US1] Implement tool call logging and exposure in response in backend/src/api/chat.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation Continuity (Priority: P2)

**Goal**: Users can resume conversations seamlessly across sessions and server restarts

**Independent Test**: User starts a conversation, adds tasks, closes chat, and later resumes the same conversation ID. System retrieves full conversation history and continues normally.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US2] Contract test for conversation_id parameter handling in tests/contract/test_conversation_continuity.py
- [ ] T038 [P] [US2] Integration test for server restart recovery in tests/integration/test_conversation_recovery.py

### Implementation for User Story 2

#### Services Enhancement
- [ ] T039 [US2] Enhance ConversationService to support efficient conversation history retrieval with pagination in backend/src/services/conversation_service.py
- [ ] T040 [US2] Implement conversation metadata tracking (last_activity) in backend/src/services/conversation_service.py

#### API Endpoint Enhancement
- [ ] T041 [US2] Enhance chat endpoint to handle conversation_id parameter validation and resolution in backend/src/api/chat.py
- [ ] T042 [US2] Implement conversation context reconstruction from database in backend/src/api/chat.py

#### Agent Enhancement
- [ ] T043 [US2] Enhance agent to use conversation context for better task disambiguation in backend/src/agents/todo_agent.py
- [ ] T044 [US2] Implement recent task context caching in agent for improved disambiguation in backend/src/agents/todo_agent.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Task Isolation (Priority: P3)

**Goal**: Users can only access and modify their own tasks and conversations

**Independent Test**: User A creates tasks and conversations, then attempts to access User B's data. System consistently denies access and returns appropriate error messages.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T045 [P] [US3] Contract test for user_id validation in all endpoints in tests/contract/test_security.py
- [ ] T046 [P] [US3] Integration test for cross-user data isolation in tests/integration/test_security_isolation.py

### Implementation for User Story 3

#### Database Enhancement
- [ ] T047 [US3] Enhance all database queries to include user_id filtering in backend/src/models/*.py
- [ ] T048 [US3] Implement comprehensive ownership validation in backend/src/services/*.py

#### MCP Tools Enhancement
- [ ] T049 [US3] Enhance all MCP tools to validate user_id against provided parameter in backend/src/mcp/tools/*.py
- [ ] T050 [US3] Implement consistent error responses for unauthorized access in backend/src/mcp/tools/*.py

#### API Endpoint Enhancement
- [ ] T051 [US3] Enhance chat endpoint to validate user_id against authenticated user in backend/src/api/chat.py
- [ ] T052 [US3] Implement comprehensive error handling for security violations in backend/src/api/chat.py

#### Agent Enhancement
- [ ] T053 [US3] Enhance agent to validate task ownership before operations in backend/src/agents/todo_agent.py
- [ ] T054 [US3] Implement security-aware confirmation messages in backend/src/agents/todo_agent.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Documentation updates in docs/
- [ ] T056 Code cleanup and refactoring
- [ ] T057 Performance optimization across all stories
- [ ] T058 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T059 Security hardening
- [ ] T060 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for POST /api/{user_id}/chat in tests/contract/test_chat_endpoint.py"
Task: "Integration test for natural language task operations in tests/integration/test_natural_language_todos.py"

# Launch all models for User Story 1:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"

# Launch all MCP tools:
Task: "Implement add_task tool in backend/src/mcp/tools/add_task.py"
Task: "Implement list_tasks tool in backend/src/mcp/tools/list_tasks.py"
Task: "Implement complete_task tool in backend/src/mcp/tools/complete_task.py"
Task: "Implement update_task tool in backend/src/mcp/tools/update_task.py"
Task: "Implement delete_task tool in backend/src/mcp/tools/delete_task.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational together
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence