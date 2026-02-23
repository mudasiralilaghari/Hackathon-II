"""
Unit tests for the TaskManager service in the TODO CLI application.
"""

import pytest
from src.models.task import Task
from src.services.task_manager import TaskManager


def test_task_manager_initialization():
    """Test that TaskManager initializes with empty task collection."""
    tm = TaskManager()
    
    assert len(tm.list_tasks()) == 0
    assert tm._next_id == 1


def test_add_task():
    """Test adding a task to the TaskManager."""
    tm = TaskManager()
    
    task = tm.add_task("Test Title", "Test Description")
    
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is False
    assert len(tm.list_tasks()) == 1
    assert tm._next_id == 2


def test_add_task_default_description():
    """Test adding a task with default empty description."""
    tm = TaskManager()
    
    task = tm.add_task("Test Title")
    
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == ""
    assert task.completed is False


def test_add_task_invalid_title():
    """Test adding a task with invalid title raises ValueError."""
    tm = TaskManager()
    
    with pytest.raises(ValueError):
        tm.add_task("")
    
    with pytest.raises(ValueError):
        tm.add_task("   ")


def test_get_task_found():
    """Test retrieving an existing task."""
    tm = TaskManager()
    added_task = tm.add_task("Test Title")
    
    retrieved_task = tm.get_task(added_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == added_task.id
    assert retrieved_task.title == added_task.title


def test_get_task_not_found():
    """Test retrieving a non-existing task returns None."""
    tm = TaskManager()
    
    retrieved_task = tm.get_task(999)
    
    assert retrieved_task is None


def test_list_tasks_empty():
    """Test listing tasks when no tasks exist."""
    tm = TaskManager()
    
    tasks = tm.list_tasks()
    
    assert len(tasks) == 0


def test_list_tasks_multiple():
    """Test listing multiple tasks."""
    tm = TaskManager()
    task1 = tm.add_task("Task 1")
    task2 = tm.add_task("Task 2")
    task3 = tm.add_task("Task 3")
    
    tasks = tm.list_tasks()
    
    assert len(tasks) == 3
    assert tasks[0].id == task1.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task3.id
    # Verify tasks are sorted by ID
    assert tasks[0].id < tasks[1].id < tasks[2].id


def test_update_task_success():
    """Test successfully updating a task."""
    tm = TaskManager()
    original_task = tm.add_task("Original Title", "Original Description")
    
    success = tm.update_task(original_task.id, "New Title", "New Description")
    
    assert success is True
    updated_task = tm.get_task(original_task.id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_partial():
    """Test updating only title or description."""
    tm = TaskManager()
    original_task = tm.add_task("Original Title", "Original Description")
    
    # Update only title
    success = tm.update_task(original_task.id, title="New Title")
    
    assert success is True
    updated_task = tm.get_task(original_task.id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged


def test_update_task_not_found():
    """Test updating a non-existing task returns False."""
    tm = TaskManager()
    
    success = tm.update_task(999, "New Title")
    
    assert success is False


def test_update_task_invalid_title():
    """Test updating a task with invalid title raises ValueError."""
    tm = TaskManager()
    original_task = tm.add_task("Original Title")
    
    with pytest.raises(ValueError):
        tm.update_task(original_task.id, "")


def test_delete_task_success():
    """Test successfully deleting a task."""
    tm = TaskManager()
    task_to_delete = tm.add_task("Test Title")
    
    success = tm.delete_task(task_to_delete.id)
    
    assert success is True
    assert tm.get_task(task_to_delete.id) is None
    assert len(tm.list_tasks()) == 0


def test_delete_task_not_found():
    """Test deleting a non-existing task returns False."""
    tm = TaskManager()
    
    success = tm.delete_task(999)
    
    assert success is False


def test_toggle_task_status_complete():
    """Test marking a task as complete."""
    tm = TaskManager()
    task = tm.add_task("Test Title")
    assert task.completed is False  # Should start as incomplete
    
    success = tm.toggle_task_status(task.id, True)
    
    assert success is True
    updated_task = tm.get_task(task.id)
    assert updated_task.completed is True


def test_toggle_task_status_incomplete():
    """Test marking a task as incomplete."""
    tm = TaskManager()
    task = tm.add_task("Test Title")
    # Manually set to complete first
    task.mark_complete()
    assert task.completed is True
    
    success = tm.toggle_task_status(task.id, False)
    
    assert success is True
    updated_task = tm.get_task(task.id)
    assert updated_task.completed is False


def test_toggle_task_status_not_found():
    """Test toggling status of a non-existing task returns False."""
    tm = TaskManager()
    
    success = tm.toggle_task_status(999, True)
    
    assert success is False