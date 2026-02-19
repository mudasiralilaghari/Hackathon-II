# Research Summary: AI Todo Chatbot

**Feature**: 1-ai-todo-chatbot
**Date**: 2026-02-09

## Technical Research Findings

### MCP SDK Integration Patterns

**Decision**: Use official MCP SDK with FastAPI middleware pattern
**Rationale**: The official MCP SDK provides the most reliable integration with minimal custom code. The middleware pattern allows clean separation between HTTP request handling and MCP tool execution.
**Alternatives considered**: 
- Custom MCP implementation: Rejected due to increased complexity and maintenance burden
- Direct HTTP calls to MCP server: Rejected for violating tool-driven intelligence principle

### OpenAI Agents SDK Best Practices

**Decision**: Use system prompt with explicit tool selection instructions and context window management
**Rationale**: Clear instructions in the system prompt significantly improve tool selection accuracy for task operations. Context window management ensures conversation history is properly truncated for performance.
**Alternatives considered**:
- Fine-tuned model: Rejected due to high cost and complexity for this scope
- Prompt chaining: Rejected for potential inconsistency in tool selection

### SQLModel with Neon PostgreSQL Performance

**Decision**: Use async SQLAlchemy with connection pooling and appropriate indexing
**Rationale**: Async operations are essential for high-concurrency chat workloads. Connection pooling reduces database connection overhead. Indexing on user_id and conversation_id ensures fast lookups.
**Alternatives considered**:
- Raw SQL queries: Rejected for maintainability and security concerns
- ORM alternatives (SQLAlchemy Core, Peewee): Rejected for less Pythonic interface and reduced type safety

### ChatKit Integration Patterns

**Decision**: Use standard ChatKit with custom message formatting for tool call visualization
**Rationale**: Minimal customization required per constitution frontend standards. ChatKit provides robust messaging infrastructure out-of-the-box.
**Alternatives considered**:
- Custom UI framework: Rejected for violating frontend standards requiring ChatKit only
- Alternative chat libraries: Rejected for increased complexity and maintenance

## Architecture Decisions

### Conversation ID Scope

**Decision**: conversation_id is globally unique UUID (not per-user)
**Rationale**: Global uniqueness simplifies database design and prevents collision issues. User isolation is enforced through user_id validation, not conversation_id scoping.
**Impact**: More secure architecture with clear separation of concerns.

### Task Identification Strategy

**Decision**: Contextual disambiguation first (recent tasks, conversation history), then ask for clarification if ambiguity remains
**Rationale**: Balances efficiency with accuracy. Users expect intelligent disambiguation but appreciate when the system asks for clarification when truly uncertain.
**Implementation**: Agent maintains recent task context in conversation history and uses it for disambiguation.

### Database Timestamp Generation

**Decision**: Application-generated timestamps (not database-generated)
**Rationale**: Ensures consistency across distributed systems and allows precise control over timestamp precision. Database timestamps can vary slightly between replicas.
**Impact**: Better reproducibility and debugging capabilities.

### Error Handling Strategy

**Decision**: Standardized error responses with user-friendly messages and structured machine-readable details
**Rationale**: Provides both good user experience and programmatic error handling capabilities. Follows constitution error handling standards.
**Format**: { "error": { "code": "TASK_NOT_FOUND", "message": "The task you requested was not found.", "details": { "task_id": "abc123" } } }

## Technology Stack Validation

| Component | Choice | Justification |
|-----------|--------|---------------|
| Backend Framework | FastAPI | Async support, automatic OpenAPI docs, excellent typing |
| Database ORM | SQLModel | Pydantic integration, simple migration support |
| Database | Neon PostgreSQL | Cloud-native, excellent scalability, ACID compliance |
| AI Agent | OpenAI Agents SDK | Official SDK, best tool integration support |
| MCP Server | Official MCP SDK | Required by constitution, standardized tool contracts |
| Frontend | OpenAI ChatKit | Required by constitution, minimal customization |

## Risk Assessment

### High Risk
- **MCP SDK compatibility issues**: Mitigation - thorough contract testing and fallback strategy
- **OpenAI API rate limits**: Mitigation - implement client-side queuing and retry logic

### Medium Risk  
- **Context window limitations**: Mitigation - implement smart conversation history truncation
- **Ambiguous task resolution errors**: Mitigation - comprehensive testing of disambiguation logic

### Low Risk
- **Database performance**: Mitigation - proper indexing and query optimization
- **Authentication integration**: Mitigation - use standard JWT patterns

This research resolves all previously identified ambiguities and provides a solid technical foundation for implementation.