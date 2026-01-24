"""
Unit tests for the Task model in the TODO CLI application.
"""

import pytest
from src.models.task import Task


def test_task_creation_valid():
    """Test creating a valid task."""
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_task_creation_defaults():
    """Test creating a task with default values."""
    task = Task(id=1, title="Test Task")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_invalid_title_empty():
    """Test creating a task with an empty title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty or only whitespace"):
        Task(id=1, title="", description="Test Description")


def test_task_creation_invalid_title_whitespace():
    """Test creating a task with a whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty or only whitespace"):
        Task(id=1, title="   ", description="Test Description")


def test_task_creation_invalid_title_too_long():
    """Test creating a task with a title that exceeds 200 characters raises ValueError."""
    long_title = "x" * 201
    with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
        Task(id=1, title=long_title, description="Test Description")


def test_task_creation_invalid_description_too_long():
    """Test creating a task with a description that exceeds 1000 characters raises ValueError."""
    long_description = "x" * 1001
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        Task(id=1, title="Test Task", description=long_description)


def test_task_creation_invalid_id_non_positive():
    """Test creating a task with a non-positive ID raises ValueError."""
    with pytest.raises(ValueError, match="ID must be a positive integer"):
        Task(id=0, title="Test Task", description="Test Description")
    
    with pytest.raises(ValueError, match="ID must be a positive integer"):
        Task(id=-1, title="Test Task", description="Test Description")


def test_task_mark_complete():
    """Test marking a task as complete."""
    task = Task(id=1, title="Test Task", completed=False)
    
    task.mark_complete()
    
    assert task.completed is True


def test_task_mark_incomplete():
    """Test marking a task as incomplete."""
    task = Task(id=1, title="Test Task", completed=True)
    
    task.mark_incomplete()
    
    assert task.completed is False


def test_task_update_details_title():
    """Test updating task title."""
    task = Task(id=1, title="Old Title", description="Description")
    
    task.update_details(title="New Title")
    
    assert task.title == "New Title"


def test_task_update_details_description():
    """Test updating task description."""
    task = Task(id=1, title="Title", description="Old Description")
    
    task.update_details(description="New Description")
    
    assert task.description == "New Description"


def test_task_update_details_both():
    """Test updating both title and description."""
    task = Task(id=1, title="Old Title", description="Old Description")
    
    task.update_details(title="New Title", description="New Description")
    
    assert task.title == "New Title"
    assert task.description == "New Description"


def test_task_update_details_invalid_title():
    """Test updating task with invalid title raises ValueError."""
    task = Task(id=1, title="Title", description="Description")
    
    with pytest.raises(ValueError, match="Title cannot be empty or only whitespace"):
        task.update_details(title="")


def test_task_update_details_invalid_title_too_long():
    """Test updating task with title that exceeds 200 characters raises ValueError."""
    task = Task(id=1, title="Title", description="Description")
    long_title = "x" * 201
    
    with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
        task.update_details(title=long_title)


def test_task_update_details_invalid_description_too_long():
    """Test updating task with description that exceeds 1000 characters raises ValueError."""
    task = Task(id=1, title="Title", description="Description")
    long_description = "x" * 1001
    
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        task.update_details(description=long_description)