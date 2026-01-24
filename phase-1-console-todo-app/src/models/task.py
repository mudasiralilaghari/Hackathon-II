"""
Task data model for the TODO CLI application.

This module defines the Task class which represents a single TODO item
with attributes like id, title, description, and completion status.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single TODO item.
    
    Attributes:
        id: Unique identifier for the task (auto-incremented)
        title: Title of the task (required, max 200 chars)
        description: Optional description of the task (max 1000 chars)
        completed: Status of the task (default: False)
    """
    
    id: int
    title: str
    description: Optional[str] = ""
    completed: bool = False
    
    def __post_init__(self):
        """Validate task attributes after initialization."""
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        
        # Validate description if provided
        if self.description and len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        
        # Validate ID
        if self.id <= 0:
            raise ValueError("ID must be a positive integer")
    
    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True
    
    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False
    
    def update_details(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update task details with validation."""
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or only whitespace")
            
            if len(title) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            
            self.title = title
        
        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description cannot exceed 1000 characters")
            
            self.description = description