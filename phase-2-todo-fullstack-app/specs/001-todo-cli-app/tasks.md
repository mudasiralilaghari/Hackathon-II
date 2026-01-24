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

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with UV dependencies
- [X] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create Task data model in src/models/task.py
- [X] T005 [P] Create TaskManager service in src/services/task_manager.py
- [X] T006 Create CLI interface in src/cli/cli_interface.py
- [X] T007 Create main application entry point in src/main.py
- [X] T008 [P] Create test configuration in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a new task with a title and description

**Independent Test**: Can be fully tested by adding a new task via CLI command and verifying it appears in the task list with a unique ID and status indicator.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T009 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [X] T010 [P] [US1] Unit test for add_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Create Task model in src/models/task.py
- [X] T012 [US1] Implement add_task method in src/services/task_manager.py
- [X] T013 [US1] Implement add task CLI command in src/cli/cli_interface.py
- [X] T014 [US1] Connect add task command to main application in src/main.py
- [X] T015 [US1] Add validation for task title and description in src/models/task.py
- [X] T016 [US1] Add error handling for invalid inputs in src/cli/cli_interface.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Allow users to view all their tasks with a status indicator

**Independent Test**: Can be fully tested by adding multiple tasks and then viewing the complete list with status indicators.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T017 [P] [US2] Unit test for list_tasks functionality in tests/unit/test_task_manager.py
- [X] T018 [P] [US2] Integration test for view all tasks in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T019 [US2] Implement list_tasks method in src/services/task_manager.py
- [X] T020 [US2] Implement view all tasks CLI command in src/cli/cli_interface.py
- [X] T021 [US2] Connect view tasks command to main application in src/main.py
- [X] T022 [US2] Format output with ID, title, description, and completion status in src/cli/cli_interface.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Allow users to update the title and/or description of a task

**Independent Test**: Can be fully tested by updating a task's title and/or description and verifying the changes are reflected when viewing the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US3] Unit test for update_task functionality in tests/unit/test_task_manager.py
- [X] T024 [P] [US3] Integration test for update task in tests/integration/test_cli.py

### Implementation for User Story 3

- [X] T025 [US3] Implement update_task method in src/services/task_manager.py
- [X] T026 [US3] Implement update task CLI command in src/cli/cli_interface.py
- [X] T027 [US3] Connect update task command to main application in src/main.py
- [X] T028 [US3] Add validation for task updates in src/models/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow users to delete a task by its ID

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T029 [P] [US4] Unit test for delete_task functionality in tests/unit/test_task_manager.py
- [X] T030 [P] [US4] Integration test for delete task in tests/integration/test_cli.py

### Implementation for User Story 4

- [X] T031 [US4] Implement delete_task method in src/services/task_manager.py
- [X] T032 [US4] Implement delete task CLI command in src/cli/cli_interface.py
- [X] T033 [US4] Connect delete task command to main application in src/main.py
- [X] T034 [US4] Add error handling for invalid IDs in src/cli/cli_interface.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: Allow users to mark a task as complete or incomplete

**Independent Test**: Can be fully tested by marking a task as complete/incomplete and verifying the status change is reflected in the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T035 [P] [US5] Unit test for toggle_complete functionality in tests/unit/test_task_manager.py
- [X] T036 [P] [US5] Integration test for mark task in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T037 [US5] Implement toggle_complete method in src/services/task_manager.py
- [X] T038 [US5] Implement mark task CLI command in src/cli/cli_interface.py
- [X] T039 [US5] Connect mark task command to main application in src/main.py
- [X] T040 [US5] Add status transition validation in src/models/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T041 [P] Documentation updates in README.md
- [X] T042 Code cleanup and refactoring
- [X] T043 [P] Additional unit tests (if requested) in tests/unit/
- [X] T044 Error handling improvements across all modules
- [X] T045 [P] Performance optimization across all stories
- [X] T046 Run quickstart.md validation

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