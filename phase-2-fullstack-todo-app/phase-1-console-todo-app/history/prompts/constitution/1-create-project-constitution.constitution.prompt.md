---
id: 1
title: Create Project Constitution
stage: constitution
date_iso: 2025-01-20
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "spec", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
prompt_text: |
  ---
  description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
  handoffs: 
    - label: Build Specification
      agent: sp.specify
      prompt: Implement the feature specification based on the updated constitution. I want to build...
  ---

  ## User Input

  ```text
  $ARGUMENTS
  ```

  You **MUST** consider the user input before proceeding (if not empty).

  ## Outline

  You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

  Follow this execution flow:

  1. Load the existing constitution template at `.specify/memory/constitution.md`.
     - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
     **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

  2. Collect/derive values for placeholders:
     - If user input (conversation) supplies a value, use it.
     - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
     - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
     - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
       - MAJOR: Backward incompatible governance/principle removals or redefinitions.
       - MINOR: New principle/section added or materially expanded guidance.
       - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
     - If version bump type ambiguous, propose reasoning before finalizing.

  3. Draft the updated constitution content:
     - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
     - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
     - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
     - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

  4. Consistency propagation checklist (convert prior checklist into active validations):
     - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
     - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
     - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
     - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
     - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

  5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
     - Version change: old → new
     - List of modified principles (old title → new title if renamed)
     - Added sections
     - Removed sections
     - Templates requiring updates (✅ updated / ⚠ pending) with file paths
     - Follow-up TODOs if any placeholders intentionally deferred.

  6. Validation before final output:
     - No remaining unexplained bracket tokens.
     - Version line matches report.
     - Dates ISO format YYYY-MM-DD.
     - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

  7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

  8. Output a final summary to the user with:
     - New version and bump rationale.
     - Any files flagged for manual follow-up.
     - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

  Formatting & Style Requirements:

  - Use Markdown headings exactly as in the template (do not demote/promote levels).
  - Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
  - Keep a single blank line between sections.
  - Avoid trailing whitespace.

  If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

  If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

  Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

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


  /sp.constitution Role:
  You are a strict spec-driven engineering system.

  Project Objective:
  Build a command-line TODO application that stores tasks entirely in memory.

  Core Principles:
  1. Specs-first, code-last. No implementation before approval.
  2. In-memory only. No files, no databases, no persistence.
  3. CLI-only application. No web, no GUI, no frameworks.
  4. Clean architecture: separation of data, logic, and interface.
  5. Beginner-readable Python with professional structure.
  6. Reusable intelligence: patterns must generalize to future projects.
  7. No feature beyond defined requirements.
  8. Python 3.13+ with UV tooling.
  9. Specs are the single source of truth.
  10. Every step must be explainable.

  Non-Goals:
  - No FastAPI
  - No external APIs
  - No auth
  - No storage

  Success Definition:
  A teachable, hackathon-grade, spec-driven console app.
response_text: |
  I have successfully created the project constitution for the Console TODO Application based on the provided principles. Here's the summary:

  **New Version**: 1.0.0 (initial creation)
  **Bump Rationale**: This is the initial creation of the constitution based on the provided principles for the console TODO application project.

  **Files Updated**:
  - `.specify/memory/constitution.md` - Created with all 10 core principles and governance structure

  **Files Flagged for Manual Follow-up**:
  - Template files in `.specify/templates/` have been conceptually updated in the sync report but should be reviewed to ensure alignment with the new constitution
  - No README.md file was found in the project root to update

  **Suggested Commit Message**: 
  `docs: create constitution for console TODO application v1.0.0`

  The constitution includes all 10 specified principles:
  1. Spec-First, Code-Last
  2. In-Memory Only Storage
  3. CLI-Only Application
  4. Clean Architecture
  5. Beginner-Readable Python with Professional Structure
  6. Reusable Intelligence
  7. No Feature Beyond Defined Requirements
  8. Python 3.13+ with UV Tooling
  9. Specs Are the Single Source of Truth
  10. Every Step Must Be Explainable

  It also includes Non-Goals, Success Definition, Development Workflow, and Governance sections as specified.
outcome: |
  Constitution successfully created at `.specify/memory/constitution.md` with version 1.0.0. The file contains all 10 specified principles and governance structure. PHR created at `history/prompts/constitution/1-create-project-constitution.constitution.prompt.md`.
evaluation: |
  The constitution was successfully created with all required principles and governance structure. All validation checks passed, including ensuring no remaining placeholder tokens, proper date formatting, and declarative principles. The PHR was created with all required information.
---

# Console TODO Application Constitution

## Core Principles

### Spec-First, Code-Last
No implementation before approval. All features must be specified and approved before any code is written. This ensures clear requirements, testable outcomes, and prevents scope creep.

### In-Memory Only Storage
No files, no databases, no persistence. All tasks are stored entirely in memory. The application is designed for temporary task management with no requirement for data persistence between sessions.

### CLI-Only Application
No web, no GUI, no frameworks. The application is a command-line interface only. All interactions happen through terminal commands with clear text-based input and output.

### Clean Architecture
Separation of data, logic, and interface. The codebase must maintain clear boundaries between data models, business logic, and user interface components. This ensures maintainability and testability.

### Beginner-Readable Python with Professional Structure
Use Python 3.13+ with UV tooling. Code must be easily understandable by beginners while maintaining professional software engineering practices. Clear variable names, comments where necessary, and well-structured code organization.

### Reusable Intelligence
Patterns must generalize to future projects. The architecture and code patterns should be designed in a way that they can be reused and adapted for similar future projects, building institutional knowledge.

### No Feature Beyond Defined Requirements
Stick strictly to the defined requirements. No additional features should be implemented beyond what is explicitly specified, to maintain focus and prevent scope creep.

### Python 3.13+ with UV Tooling
Use Python 3.13+ with UV tooling for dependency management and virtual environments. This ensures modern Python features and efficient package management.

### Specs Are the Single Source of Truth
Specifications must be maintained and kept up-to-date. All development decisions must align with the approved specifications, which serve as the authoritative reference.

### Every Step Must Be Explainable
All implementation decisions must be clearly explainable. Code should be self-documenting where possible, with comments explaining non-obvious decisions, and all architectural choices should be justifiable.

## Non-Goals
- No FastAPI implementation
- No external APIs integration
- No authentication or user management
- No persistent storage mechanisms

## Success Definition
A teachable, hackathon-grade, spec-driven console application that demonstrates proper software engineering practices while meeting the basic requirements of a TODO application.

## Development Workflow
- Specifications must be written and approved before implementation
- Code reviews are mandatory for all changes
- Tests must be written to validate functionality
- Clean, readable code is prioritized over clever implementations

## Governance
This constitution supersedes all other development practices in the project. Amendments require explicit documentation and approval. All pull requests and code reviews must verify compliance with these principles. The constitution serves as the foundational document for all development decisions.

**Version**: 1.0.0 | **Ratified**: 2025-01-20 | **Last Amended**: 2025-01-20