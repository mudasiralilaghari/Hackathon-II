"""
Basic integration test for the TODO CLI application.
"""

from src.models.task import Task
from src.services.task_manager import TaskManager
from src.cli.cli_interface import CLIInterface


def test_full_workflow():
    """Test the full workflow of the TODO application."""
    # Initialize components
    task_manager = TaskManager()
    cli_interface = CLIInterface(task_manager)
    
    # Test adding a task
    task1 = task_manager.add_task("First Task", "Description for first task")
    assert task1.id == 1
    assert task1.title == "First Task"
    assert task1.description == "Description for first task"
    assert task1.completed is False
    
    # Test adding another task
    task2 = task_manager.add_task("Second Task")
    assert task2.id == 2
    assert task2.title == "Second Task"
    assert task2.description == ""
    assert task2.completed is False
    
    # Test listing tasks
    tasks = task_manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2
    
    # Test updating a task
    success = task_manager.update_task(1, "Updated First Task", "Updated description")
    assert success is True
    updated_task = task_manager.get_task(1)
    assert updated_task.title == "Updated First Task"
    assert updated_task.description == "Updated description"
    
    # Test marking a task as complete
    success = task_manager.toggle_task_status(1, True)
    assert success is True
    completed_task = task_manager.get_task(1)
    assert completed_task.completed is True
    
    # Test marking a task as incomplete
    success = task_manager.toggle_task_status(1, False)
    assert success is True
    incomplete_task = task_manager.get_task(1)
    assert incomplete_task.completed is False
    
    # Test deleting a task
    success = task_manager.delete_task(2)
    assert success is True
    assert task_manager.get_task(2) is None
    assert len(task_manager.list_tasks()) == 1
    
    print("All integration tests passed!")


if __name__ == "__main__":
    test_full_workflow()