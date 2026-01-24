"""
Command-line interface for the TODO CLI application.

This module handles all user interactions through the command line,
including displaying menus, getting user input, and showing results.
"""

from typing import Optional
from ..services.task_manager import TaskManager


class CLIInterface:
    """
    Handles the command-line interface for the TODO application.
    
    The CLIInterface manages user interactions, processes commands,
    and displays information to the user.
    """
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the CLI interface with a TaskManager.
        
        Args:
            task_manager: The TaskManager instance to use for task operations
        """
        self.task_manager = task_manager
    
    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("TODO CLI Application")
        print("="*40)
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Mark task as complete/incomplete")
        print("6. Exit")
        print("="*40)
    
    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.
        
        Returns:
            The user's choice as a string
        """
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return "6"  # Return exit choice
    
    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        
        if not title:
            print("Error: Task title cannot be empty")
            return
        
        description = input("Enter task description (optional): ").strip()
        
        try:
            task = self.task_manager.add_task(title, description)
            print(f"Task added successfully with ID {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.task_manager.list_tasks()
        
        if not tasks:
            print("No tasks found.")
            return
        
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] ID: {task.id} | Title: {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
            print()
    
    def update_task(self):
        """Handle updating a task."""
        print("\n--- Update Task ---")
        
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        # Check if task exists
        if not self.task_manager.get_task(task_id):
            print(f"Error: Task with ID {task_id} does not exist")
            return
        
        print("Leave blank to keep current value")
        new_title = input(f"Enter new title (current: '{self.task_manager.get_task(task_id).title}'): ").strip()
        new_description = input(f"Enter new description (current: '{self.task_manager.get_task(task_id).description}'): ").strip()
        
        # Use None to indicate no change, or the new value if provided
        title_update = new_title if new_title else None
        description_update = new_description if new_description else None
        
        try:
            if self.task_manager.update_task(task_id, title_update, description_update):
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Error: Could not update task {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        if self.task_manager.delete_task(task_id):
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Error: Task with ID {task_id} does not exist")
    
    def mark_task_status(self):
        """Handle marking a task as complete or incomplete."""
        print("\n--- Mark Task Status ---")
        
        try:
            task_id = int(input("Enter task ID: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        # Check if task exists
        if not self.task_manager.get_task(task_id):
            print(f"Error: Task with ID {task_id} does not exist")
            return
        
        status_choice = input("Mark as (c)omplete or (i)ncomplete? ").strip().lower()
        
        if status_choice in ['c', 'complete']:
            completed = True
            status_text = "complete"
        elif status_choice in ['i', 'incomplete']:
            completed = False
            status_text = "incomplete"
        else:
            print("Error: Invalid choice. Please enter 'c' for complete or 'i' for incomplete.")
            return
        
        if self.task_manager.toggle_task_status(task_id, completed):
            print(f"Task {task_id} marked as {status_text} successfully")
        else:
            print(f"Error: Could not update task {task_id}")
    
    def run(self):
        """Run the main application loop."""
        print("Welcome to the TODO CLI Application!")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_task_status()
            elif choice == "6":
                print("Thank you for using the TODO CLI Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")