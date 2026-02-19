# Data Model: AI Todo Chatbot

**Feature**: 1-ai-todo-chatbot
**Date**: 2026-02-09
**Based on**: specs/1-ai-todo-chatbot/spec.md and constitution principles

## Entities

### Conversation
Represents a chat session between a user and the AI assistant.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Primary key | Required, unique |
| user_id | string | Owner of the conversation | Required, indexed |
| created_at | datetime | When conversation was created | Required |
| last_activity | datetime | Last message timestamp | Required, updated on each message |
| metadata | JSON | Additional conversation data | Optional |

**Relationships**:
- One-to-many with Message (conversation has many messages)
- Many-to-one with User (user has many conversations)

### Message
Represents a single exchange in a conversation.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Primary key | Required, unique |
| conversation_id | UUID | Reference to parent conversation | Required, indexed, foreign key |
| user_id | string | Owner of the message | Required, indexed |
| type | enum | "user" or "assistant" | Required |
| content | text | Message content | Required |
| timestamp | datetime | When message was sent | Required |
| tool_calls | JSON | Array of tool call objects | Optional |
| sequence_number | integer | Order within conversation | Required, unique per conversation |

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)
- Many-to-one with User (user owns the message)

### Task
Represents a todo item.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Primary key | Required, unique |
| user_id | string | Owner of the task | Required, indexed |
| title | string | Task description | Required, indexed |
| description | text | Additional details | Optional |
| status | enum | "pending" or "completed" | Required, default: "pending" |
| created_at | datetime | When task was created | Required |
| updated_at | datetime | Last modification time | Required |
| metadata | JSON | Additional task data | Optional |

**Relationships**:
- Many-to-one with User (user owns the task)
- No direct relationship with Conversation (tasks are referenced by content/context)

## Validation Rules

### Cross-Entity Validation
- All operations must validate user_id matches authenticated user
- Messages must belong to existing conversations
- Tasks must belong to existing users
- conversation_id in requests must match existing conversation or be null for new conversations

### Business Logic Validation
- Task titles can be duplicated per user (resolved via contextual disambiguation)
- Status transitions: pending → completed only (no reverse transitions)
- Updated_at must be >= created_at
- Sequence numbers must be sequential within each conversation

## State Transitions

### Conversation
- Created → Active → Archived (not implemented per out-of-scope)
- No deletion (per constitution constraints)

### Message
- Created → Stored → Retrieved
- No state changes after creation

### Task
- Created (pending) → Completed
- No deletion (hard delete per constitution constraints)

## Indexing Strategy

| Table | Indexes | Purpose |
|-------|---------|---------|
| conversations | user_id, created_at | Fast user-specific conversation lookup |
| messages | conversation_id, sequence_number, user_id, timestamp | Fast conversation history retrieval |
| tasks | user_id, status, title, created_at | Fast task listing and filtering |

## Migration Approach

1. **Initial schema**: Create tables with basic fields
2. **Phase 1**: Add indexes and foreign key constraints
3. **Phase 2**: Add metadata fields and validation rules
4. **Versioning**: Use Alembic with semantic versioning

## Data Lifecycle

- **Creation**: All entities created through API endpoints or MCP tools
- **Reading**: Read-only operations through GET endpoints or MCP tools
- **Updating**: Limited updates (task status, description, message content not updated)
- **Deletion**: Hard delete for tasks (per constitution), no soft deletes

This data model satisfies all functional requirements from the specification and adheres to the constitution principles of deterministic persistence and stateless backend design.