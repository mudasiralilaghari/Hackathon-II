# Data Model: In-Memory TODO CLI App

## Task Entity

### Attributes
- **id**: integer
  - Unique identifier for each task
  - Auto-incremented value
  - Required field
- **title**: string
  - Title of the task
  - Required field
  - Maximum length: 200 characters
- **description**: string
  - Optional description of the task
  - Default: empty string
  - Maximum length: 1000 characters
- **completed**: boolean
  - Status of the task
  - Default: false (incomplete)

### Validation Rules
- ID must be unique across all tasks
- ID must be a positive integer
- Title must not be empty or only whitespace
- Title must not exceed 200 characters
- Description, if provided, must not exceed 1000 characters

### State Transitions
- A task can transition from `completed=false` to `completed=true` (mark as complete)
- A task can transition from `completed=true` to `completed=false` (mark as incomplete)

## Task Collection

### In-Memory Storage
- Tasks are stored in a dictionary with ID as key and Task object as value
- IDs are auto-incremented starting from 1
- When all tasks are deleted, the ID counter continues from the last value (does not reset)

### Operations
- Add: Insert a new task with auto-generated ID
- Read: Retrieve a task by ID or list all tasks
- Update: Modify title and/or description of a task by ID
- Delete: Remove a task by ID
- Mark Complete/Incomplete: Update completion status by ID