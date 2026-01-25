# Hackathon II - Full Project Repository

This repository contains both phases of the Hackathon II project:

## Phase 1: Console TODO Application
A simple command-line interface application for managing TODO tasks. Tasks are stored entirely in memory and will be lost when the application exits.

### Features
- Add new tasks with title and description
- View all tasks with status indicators
- Update task titles and descriptions
- Delete tasks by ID
- Mark tasks as complete or incomplete
- Unique auto-incremented IDs for each task
- Clear user feedback for all operations
- Graceful handling of invalid inputs

### Requirements
- Python 3.13 or higher

### Project Structure
```
src/
├── models/
│   └── task.py          # Task data model
├── services/
│   └── task_manager.py  # Task business logic
├── cli/
│   └── cli_interface.py # Command-line interface
└── main.py              # Application entry point

tests/
├── unit/
│   ├── test_task.py     # Task model tests
│   └── test_task_manager.py # Task manager tests
├── integration/
│   └── test_cli.py      # CLI integration tests
└── conftest.py          # Test configuration
```

## Phase 2: Full-Stack TODO Application
A comprehensive web-based TODO application with frontend and backend components.

### Features
- Complete CRUD operations for tasks
- User authentication and authorization
- Responsive web interface
- Data persistence
- Modern UI/UX design

## Repository Structure
```
Hackathon-II/
├── phase-1-console-todo-app/     # Console application
├── phase-2-todo-fullstack-app/   # Full-stack application
└── README.md                     # This file
```

## Setup Instructions

### For Phase 1 (Console App):
1. Navigate to `phase-1-console-todo-app/`
2. Ensure Python 3.13+ is installed
3. Run: `python -m src.main`

### For Phase 2 (Full-Stack App):
1. Navigate to `phase-2-todo-fullstack-app/`
2. Follow the specific setup instructions in that directory

## License
This project is created for educational purposes as part of a hackathon project.