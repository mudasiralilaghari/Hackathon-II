"""
TaskManager service for the TODO CLI application.

This module handles the business logic for managing tasks,
including adding, listing, updating, deleting, and marking tasks.
"""

from typing import Dict, List, Optional
from ..models.task import Task


class TaskManager:
    """
    Manages the collection of tasks in memory.
    
    The TaskManager handles all business logic related to tasks,
    including creation, retrieval, updates, and deletion.
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task collection."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
    
    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and optional description.
        
        Args:
            title: The title of the task (required)
            description: The description of the task (optional)
            
        Returns:
            The newly created Task object with a unique ID
            
        Raises:
            ValueError: If the title is invalid
        """
        # Create a new task with the next available ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        
        # Add the task to the collection
        self._tasks[task.id] = task
        
        # Increment the ID counter for the next task
        self._next_id += 1
        
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def list_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            A list of all Task objects, sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update the title and/or description of an existing task.
        
        Args:
            task_id: The ID of the task to update
            title: The new title (optional)
            description: The new description (optional)
            
        Returns:
            True if the task was updated, False if the task was not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        
        try:
            task.update_details(title=title, description=description)
            return True
        except ValueError as e:
            raise e
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False if the task was not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def toggle_task_status(self, task_id: int, completed: bool) -> bool:
        """
        Mark a task as complete or incomplete.
        
        Args:
            task_id: The ID of the task to update
            completed: True to mark as complete, False to mark as incomplete
            
        Returns:
            True if the task status was updated, False if the task was not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        
        if completed:
            task.mark_complete()
        else:
            task.mark_incomplete()
        
        return True