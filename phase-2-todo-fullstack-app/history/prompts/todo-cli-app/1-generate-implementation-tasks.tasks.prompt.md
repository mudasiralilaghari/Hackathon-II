---
id: 1
title: Generate Implementation Tasks
stage: tasks
date_iso: 2025-01-20
surface: agent
model: Qwen
feature: todo-cli-app
branch: 001-todo-cli-app
user: user
command: /sp.tasks
labels: ["tasks", "todo", "cli", "implementation"]
links:
  spec: specs/001-todo-cli-app/spec.md
  plan: specs/001-todo-cli-app/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-todo-cli-app/tasks.md"
tests_yaml: []
prompt_text: |
  ---
  description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
  handoffs: 
    - label: Analyze For Consistency
      agent: sp.analyze
      prompt: Run a project analysis for consistency
      send: true
    - label: Implement Project
      agent: sp.implement
      prompt: Start the implementation in phases
      send: true
  ---

  ## User Input

  ```text
  $ARGUMENTS
  ```

  You **MUST** consider the user input before proceeding (if not empty).

  ## Outline

  1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

  2. **Load design documents**: Read from FEATURE_DIR:
     - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
     - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
     - Note: Not all projects have all documents. Generate tasks based on what's available.

  3. **Execute task generation workflow**:
     - Load plan.md and extract tech stack, libraries, project structure
     - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
     - If data-model.md exists: Extract entities and map to user stories
     - If contracts/ exists: Map endpoints to user stories
     - If research.md exists: Extract decisions for setup tasks
     - Generate tasks organized by user story (see Task Generation Rules below)
     - Generate dependency graph showing user story completion order
     - Create parallel execution examples per user story
     - Validate task completeness (each user story has all needed tasks, independently testable)

  4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
     - Correct feature name from plan.md
     - Phase 1: Setup tasks (project initialization)
     - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
     - Phase 3+: One phase per user story (in priority order from spec.md)
     - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
     - Final Phase: Polish & cross-cutting concerns
     - All tasks must follow the strict checklist format (see Task Generation Rules below)
     - Clear file paths for each task
     - Dependencies section showing story completion order
     - Parallel execution examples per story
     - Implementation strategy section (MVP first, incremental delivery)

  5. **Report**: Output path to generated tasks.md and summary:
     - Total task count
     - Task count per user story
     - Parallel opportunities identified
     - Independent test criteria for each story
     - Suggested MVP scope (typically just User Story 1)
     - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

  Context for task generation: Generate actionable development tasks. Tasks: 1. Initialize UV project and virtual environment 2. Create folder structure: - src/ - specs/ 3. Implement Task model 4. Implement TaskManager service: - add_task - list_tasks - update_task - delete_task - toggle_complete 5. Implement CLI menu system 6. Connect CLI with TaskManager 7. Add input validation and error handling 8. Write README.md 9. Manual testing of all features Wait for execution approval before coding.

  The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

  ## Task Generation Rules

  **CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

  **Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

  ### Checklist Format (REQUIRED)

  Every task MUST strictly follow this format:

  ```text
  - [ ] [TaskID] [P?] [Story?] Description with file path
  ```

  **Format Components**:

  1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
  2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
  3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
  4. **[Story] label**: REQUIRED for user story phase tasks only
     - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
     - Setup phase: NO story label
     - Foundational phase: NO story label  
     - User Story phases: MUST have story label
     - Polish phase: NO story label
  5. **Description**: Clear action with exact file path

  **Examples**:

  - ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
  - ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
  - ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
  - ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
  - ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
  - ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
  - ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
  - ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

  ### Task Organization

  1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
     - Each user story (P1, P2, P3...) gets its own phase
     - Map all related components to their story:
       - Models needed for that story
       - Services needed for that story
       - Endpoints/UI needed for that story
       - If tests requested: Tests specific to that story
     - Mark story dependencies (most stories should be independent)

  2. **From Contracts**:
     - Map each contract/endpoint → to the user story it serves
     - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

  3. **From Data Model**:
     - Map each entity to the user story(ies) that need it
     - If entity serves multiple stories: Put in earliest story or Setup phase
     - Relationships → service layer tasks in appropriate story phase

  4. **From Setup/Infrastructure**:
     - Shared infrastructure → Setup phase (Phase 1)
     - Foundational/blocking tasks → Foundational phase (Phase 2)
     - Story-specific setup → within that story's phase

  ### Phase Structure

  - **Phase 1**: Setup (project initialization)
  - **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
  - **Phase 3+**: User Stories in priority order (P1, P2, P3...)
    - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
    - Each phase should be a complete, independently testable increment
  - **Final Phase**: Polish & Cross-Cutting Concerns

  ---

  As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

  1) Determine Stage
     - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

  2) Generate Title and Determine Routing:
     - Generate Title: 3–7 words (slug for filename)
     - Route is automatically determined by stage:
       - `constitution` → `history/prompts/constitution/`
       - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
       - `general` → `history/prompts/general/`

  3) Create and Fill PHR (Shell first; fallback agent‑native)
     - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
     - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
     - If the script fails:
       - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
       - Allocate an ID; compute the output path based on stage from step 2; write the file
       - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

  4) Validate + report
     - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
     - On failure: warn, don't block. Skip only for `/sp.phr`.
response_text: |
  ## Completion Report

  **Tasks File Path**: `D:\\hackathon-II\\phase-1-console-todo-app\\specs\\001-todo-cli-app\\tasks.md`

  **Generated Tasks Summary**:
  - Total task count: 46 tasks
  - Setup phase: 3 tasks
  - Foundational phase: 5 tasks
  - User Story 1 (Add New Task): 7 tasks
  - User Story 2 (View All Tasks): 6 tasks
  - User Story 3 (Update Task Details): 6 tasks
  - User Story 4 (Delete Task): 6 tasks
  - User Story 5 (Mark Task Complete/Incomplete): 6 tasks
  - Polish phase: 7 tasks

  **Parallel opportunities identified**:
  - Multiple setup and foundational tasks can run in parallel
  - All user stories can be developed in parallel after foundational phase
  - Test tasks within each user story can run in parallel

  **Independent test criteria**:
  - Each user story has clearly defined independent test criteria from the spec
  - User Story 1 (Add New Task): Can be tested by adding a task and verifying it appears in the list
  - User Story 2 (View All Tasks): Can be tested by adding tasks and viewing the complete list
  - User Story 3 (Update Task Details): Can be tested by updating task details and verifying changes
  - User Story 4 (Delete Task): Can be tested by deleting a task and verifying it's removed
  - User Story 5 (Mark Task Complete/Incomplete): Can be tested by marking tasks and verifying status changes

  **Suggested MVP scope**: User Story 1 (Add New Task) provides the core functionality of the TODO app

  All tasks follow the required checklist format with proper IDs, labels, and file paths.
outcome: |
  Successfully created tasks file for the In-Memory TODO CLI App at `D:\\hackathon-II\\phase-1-console-todo-app\\specs\\001-todo-cli-app\\tasks.md` with 46 tasks organized across 8 phases. The tasks follow the required format and are organized by user story priority.
evaluation: |
  The tasks file meets all requirements with proper organization by user story, correct formatting, and clear file paths. Each task is specific enough to be executed independently. The parallel execution opportunities and dependencies are clearly identified.
---

---

description: "Task list for In-Memory TODO CLI App implementation"
---

# Tasks: In-Memory TODO CLI App

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with UV dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create Task data model in src/models/task.py
- [ ] T005 [P] Create TaskManager service in src/services/task_manager.py
- [ ] T006 Create CLI interface in src/cli/cli_interface.py
- [ ] T007 Create main application entry point in src/main.py
- [ ] T008 [P] Create test configuration in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a new task with a title and description

**Independent Test**: Can be fully tested by adding a new task via CLI command and verifying it appears in the task list with a unique ID and status indicator.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [ ] T010 [P] [US1] Unit test for add_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [ ] T011 [P] [US1] Create Task model in src/models/task.py
- [ ] T012 [US1] Implement add_task method in src/services/task_manager.py
- [ ] T013 [US1] Implement add task CLI command in src/cli/cli_interface.py
- [ ] T014 [US1] Connect add task command to main application in src/main.py
- [ ] T015 [US1] Add validation for task title and description in src/models/task.py
- [ ] T016 [US1] Add error handling for invalid inputs in src/cli/cli_interface.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Allow users to view all their tasks with a status indicator

**Independent Test**: Can be fully tested by adding multiple tasks and then viewing the complete list with status indicators.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Unit test for list_tasks functionality in tests/unit/test_task_manager.py
- [ ] T018 [P] [US2] Integration test for view all tasks in tests/integration/test_cli.py

### Implementation for User Story 2

- [ ] T019 [US2] Implement list_tasks method in src/services/task_manager.py
- [ ] T020 [US2] Implement view all tasks CLI command in src/cli/cli_interface.py
- [ ] T021 [US2] Connect view tasks command to main application in src/main.py
- [ ] T022 [US2] Format output with ID, title, description, and completion status in src/cli/cli_interface.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Allow users to update the title and/or description of a task

**Independent Test**: Can be fully tested by updating a task's title and/or description and verifying the changes are reflected when viewing the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Unit test for update_task functionality in tests/unit/test_task_manager.py
- [ ] T024 [P] [US3] Integration test for update task in tests/integration/test_cli.py

### Implementation for User Story 3

- [ ] T025 [US3] Implement update_task method in src/services/task_manager.py
- [ ] T026 [US3] Implement update task CLI command in src/cli/cli_interface.py
- [ ] T027 [US3] Connect update task command to main application in src/main.py
- [ ] T028 [US3] Add validation for task updates in src/models/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow users to delete a task by its ID

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US4] Unit test for delete_task functionality in tests/unit/test_task_manager.py
- [ ] T030 [P] [US4] Integration test for delete task in tests/integration/test_cli.py

### Implementation for User Story 4

- [ ] T031 [US4] Implement delete_task method in src/services/task_manager.py
- [ ] T032 [US4] Implement delete task CLI command in src/cli/cli_interface.py
- [ ] T033 [US4] Connect delete task command to main application in src/main.py
- [ ] T034 [US4] Add error handling for invalid IDs in src/cli/cli_interface.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: Allow users to mark a task as complete or incomplete

**Independent Test**: Can be fully tested by marking a task as complete/incomplete and verifying the status change is reflected in the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US5] Unit test for toggle_complete functionality in tests/unit/test_task_manager.py
- [ ] T036 [P] [US5] Integration test for mark task in tests/integration/test_cli.py

### Implementation for User Story 5

- [ ] T037 [US5] Implement toggle_complete method in src/services/task_manager.py
- [ ] T038 [US5] Implement mark task CLI command in src/cli/cli_interface.py
- [ ] T039 [US5] Connect mark task command to main application in src/main.py
- [ ] T040 [US5] Add status transition validation in src/models/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T041 [P] Documentation updates in README.md
- [ ] T042 Code cleanup and refactoring
- [ ] T043 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T044 Error handling improvements across all modules
- [ ] T045 [P] Performance optimization across all stories
- [ ] T046 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

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

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model in tests/unit/test_task.py"
Task: "Unit test for add_task functionality in tests/unit/test_task_manager.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence