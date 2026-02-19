<!-- Sync Impact Report
Version change: N/A → 1.0.0
Added sections: Development Standards, Architecture Standards, AI & Agent Standards, MCP Tooling Standards, Conversation & Persistence Rules, Frontend Standards, Database Standards, Error Handling Standards, Quality & Review Standards, Constraints, Success Criteria
Templates requiring updates:
- .specify/templates/plan-template.md: Update Constitution Check section to reference new principles
- .specify/templates/spec-template.md: Ensure requirements align with new principles
- .specify/templates/tasks-template.md: Ensure task categorization reflects new principle-driven task types
-->

# Todo AI Chatbot Constitution

## Core Principles

### I. Agent-First Design
All business logic must flow through AI agents. No direct API endpoints or service functions should implement core business logic without agent orchestration. Agents serve as the single source of truth for intent interpretation and action selection.

### II. Tool-Driven Intelligence
Agents must act only via MCP tools. Direct database access, external API calls, or state manipulation outside of defined MCP tool interfaces is strictly prohibited. Tools provide the contract boundary for all system interactions.

### III. Stateless Backend
No in-memory session or conversation state. Each request must be self-contained with all necessary context provided in the request payload or retrieved from persistent storage. Server restarts must not affect ongoing conversations.

### IV. Deterministic Persistence
All state must be stored in the database. Temporary in-memory caches are permitted only for performance optimization with proper fallback to persistent storage. Data consistency and durability are non-negotiable requirements.

### V. Reusable Intelligence
Patterns, tools, and agent logic must be reusable across features and projects. Code duplication for similar functionality is prohibited. Common utilities, tool implementations, and agent behaviors must be extracted into shared components.

### VI. Zero Manual Coding
Implementation only via Claude Code iterations. All code must be generated through the Spec-Driven Development workflow: Write spec → Generate plan → Break into tasks → Implement via AI. No ad-hoc implementation outside this workflow is permitted.

## Development Standards

- Follow Agentic Dev Stack strictly:
  Write spec → Generate plan → Break into tasks → Implement via AI.
- No ad-hoc implementation outside the defined workflow.
- Each phase must be reviewable and reproducible.
- Specs must live under /specs.
- Architecture must be explainable in README.
- No unused endpoints or dead code.
- Logs must be minimal and meaningful.

## Architecture Standards

- Single stateless chat endpoint:
  POST /api/{user_id}/chat
- Conversation history must be fetched from DB on every request.
- Server must be horizontally scalable.
- MCP server must expose task operations as tools only.
- FastAPI server must never directly mutate task state outside MCP tools.
- Use SQLModel with Neon PostgreSQL for database access.
- Models must match defined schema: Task, Conversation, Message
- Migrations must be included and reproducible.

## AI & Agent Standards

- Use OpenAI Agents SDK for all AI logic.
- Agent must:
  - Interpret natural language intent
  - Select correct MCP tool(s)
  - Chain tools when required
  - Produce user-friendly confirmations
- Agent must NOT:
  - Guess task IDs without verification
  - Modify data without tool calls
  - Store hidden state
- Agent responses must be deterministic and reproducible given the same input context.

## MCP Tooling Standards

- MCP tools must be stateless.
- Each tool call must:
  - Validate user ownership
  - Persist changes in the database
  - Return structured, predictable outputs
- Tools must match the defined specifications exactly:
  add_task, list_tasks, complete_task, update_task, delete_task
- Tool errors must be explicit and machine-readable.
- Tool implementations must be unit-tested and contract-verified.

## Conversation & Persistence Rules

- Every user message must be stored.
- Every assistant response must be stored.
- Conversation context must be reconstructed per request.
- Server restarts must not affect ongoing conversations.
- Conversation history must be paginated and efficiently retrievable.
- Message ordering must be preserved and verifiable.

## Frontend Standards

- Use OpenAI ChatKit only.
- No custom chat logic outside ChatKit.
- Domain allowlist must be correctly configured.
- Frontend must be a thin UI layer — no business logic.
- User interface must be responsive and accessible.

## Database Standards

- Use SQLModel with Neon PostgreSQL.
- Models must match defined schema:
  Task, Conversation, Message
- Migrations must be included and reproducible.
- Database queries must be optimized for common access patterns.
- Schema changes require migration scripts and backward compatibility considerations.

## Error Handling Standards

- Graceful handling of:
  - Task not found
  - Unauthorized access
  - Invalid tool parameters
- Agent must explain errors in user-friendly language.
- Error codes must be consistent and documented.
- System must log errors with sufficient context for debugging without exposing sensitive information.

## Quality & Review Standards

- Code must be readable and modular.
- Specs must live under /specs.
- Architecture must be explainable in README.
- No unused endpoints or dead code.
- Logs must be minimal and meaningful.
- All changes must include appropriate tests.
- Pull requests must demonstrate compliance with constitution principles.

## Constraints

- No manual coding.
- No hidden state.
- No deviation from defined tool contracts.
- No frontend logic duplication.
- No direct database access from agent logic.
- No session-based authentication; use token-based authentication only.

## Success Criteria

- User can fully manage todos using natural language.
- All task operations occur via MCP tools.
- Conversation context survives server restarts.
- Project demonstrates reusable agent + MCP patterns.
- Architecture is production-grade and hackathon-ready.
- System handles 100+ concurrent users with <500ms p95 latency.
- 95% of user intents are correctly interpreted and acted upon.

## Governance

The Todo AI Chatbot Constitution supersedes all other practices and guidelines for this project. Amendments require:
1. Documentation of the change rationale and impact
2. Review and approval by the project lead
3. Migration plan for existing implementations
4. Update of all dependent templates and documentation

All PRs and reviews must verify compliance with constitution principles. Complexity must be justified against the principles. The constitution is reviewed quarterly or when significant architectural changes are proposed.

**Version**: 1.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09