# In-Memory TODO CLI Application

A simple command-line interface application for managing TODO tasks. Tasks are stored entirely in memory and will be lost when the application exits.

## Features

- Add new tasks with title and description
- View all tasks with status indicators
- Update task titles and descriptions
- Delete tasks by ID
- Mark tasks as complete or incomplete
- Unique auto-incremented IDs for each task
- Clear user feedback for all operations
- Graceful handling of invalid inputs

## Requirements

- Python 3.13 or higher

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Make sure you have Python 3.13+ installed

## Usage

Run the application using Python:

```bash
python -m src.main
```

Follow the on-screen menu prompts to interact with the application:

1. **Add a new task**: Enter a title and optional description
2. **View all tasks**: See a list of all tasks with their status
3. **Update a task**: Modify the title or description of an existing task
4. **Delete a task**: Remove a task by its ID
5. **Mark task as complete/incomplete**: Change the completion status of a task
6. **Exit**: Quit the application

## Project Structure

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

## Architecture

The application follows clean architecture principles with separation of concerns:

- **Models**: Define data structures (Task model)
- **Services**: Handle business logic (TaskManager)
- **CLI**: Handle user interface and input/output

## Testing

To run the tests:

```bash
pip install pytest
pytest tests/
```

## License

This project is created for educational purposes as part of a hackathon project.