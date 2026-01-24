# API Contract: In-Memory TODO CLI App

## CLI Commands

### 1. Add Task
**Command**: `add`
**Description**: Add a new task with title and optional description
**Input**:
- title (string, required): Task title (max 200 chars)
- description (string, optional): Task description (max 1000 chars)
**Output**:
- Success: Task added with unique ID
- Error: Appropriate error message for invalid input

### 2. View All Tasks
**Command**: `view`
**Description**: Display all tasks with their details and status
**Input**: None
**Output**:
- List of all tasks with ID, title, description, and completion status
- Message if no tasks exist

### 3. Update Task
**Command**: `update`
**Description**: Update the title and/or description of an existing task
**Input**:
- id (integer, required): Task ID
- title (string, optional): New task title
- description (string, optional): New task description
**Output**:
- Success: Task updated successfully
- Error: Appropriate error message for invalid ID or input

### 4. Delete Task
**Command**: `delete`
**Description**: Delete a task by its ID
**Input**:
- id (integer, required): Task ID
**Output**:
- Success: Task deleted successfully
- Error: Appropriate error message for invalid ID

### 5. Mark Task Complete/Incomplete
**Command**: `mark`
**Description**: Mark a task as complete or incomplete
**Input**:
- id (integer, required): Task ID
- status (boolean, required): True for complete, False for incomplete
**Output**:
- Success: Task status updated successfully
- Error: Appropriate error message for invalid ID

## Error Handling
- Invalid IDs: "Error: Task with ID [X] does not exist"
- Invalid inputs: "Error: [specific validation error]"
- General errors: "An error occurred: [error message]"

## Success Messages
- Add: "Task added successfully with ID [X]"
- Update: "Task [X] updated successfully"
- Delete: "Task [X] deleted successfully"
- Mark: "Task [X] marked as [complete/incomplete] successfully"