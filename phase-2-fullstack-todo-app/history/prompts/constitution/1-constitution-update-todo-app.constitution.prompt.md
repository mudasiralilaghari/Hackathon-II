---
id: 1
title: constitution-update-todo-app
stage: constitution
date: 2026-01-07
surface: agent
model: Qwen
feature: multi-user-todo-app
branch: 001-multi-user-todo-app
user: user
command: /sp.constitution
labels: [constitution, todo, fullstack]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```
/sp.constitution # Phase 2 Constitution – Todo Full-Stack Web App

## Core Principles
1. Spec-Driven Development is mandatory
2. Backend and frontend must strictly follow specs
3. No business logic without spec reference
4. Authentication is mandatory for all APIs
5. Each user can only access their own data
6. Clean architecture and separation of concerns
7. No hardcoded secrets – environment variables only
8. Phase-1 logic may inspire but not be reused blindly

## Non-Goals
- No AI chatbot in Phase-2
- No role-based access control
- No file uploads

## Quality Bar
- API must be RESTful
- Frontend must be responsive
- Database must be persistent (Neon)
- JWT auth must be enforced on every request
```

## Response snapshot

Updated the project constitution and aligned templates with the new principles. Created a comprehensive constitution document for the Todo Full-Stack Web App with 8 core principles, non-goals, and quality bar requirements. Updated plan-template.md, spec-template.md, and tasks-template.md to ensure compliance with the new constitution.

## Outcome

- ✅ Impact: Updated constitution and aligned templates with new principles
- 🧪 Tests: No tests required for documentation update
- 📁 Files: 4 files updated to align with constitution
- 🔁 Next prompts: Ready for feature specification based on updated constitution
- 🧠 Reflection: Successfully implemented constitution-driven development approach

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification using new constitution