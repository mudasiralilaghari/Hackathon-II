# Quickstart Guide: In-Memory TODO CLI App

## Prerequisites
- Python 3.13 or higher
- UV package manager

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (or `pip install -r requirements.txt` if using pip)
4. Run the application: `python -m src.main`

## Usage
1. Run the application with `python -m src.main`
2. Select an option from the main menu:
   - Add a new task
   - View all tasks
   - Update a task
   - Delete a task
   - Mark task as complete/incomplete
3. Follow the prompts for each operation

## Example Workflow
1. Add a task: Select "Add Task" and enter title and description
2. View tasks: Select "View All Tasks" to see your task list
3. Update a task: Select "Update Task" and provide the task ID and new details
4. Mark complete: Select "Mark Task Complete" and provide the task ID
5. Exit: Select "Exit" to quit the application

## Features
- Add tasks with title and optional description
- View all tasks with status indicators
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete
- Auto-incremented unique IDs
- Clear user feedback for all operations
- Graceful handling of invalid inputs