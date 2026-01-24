"""
Main entry point for the TODO CLI application.

This module initializes the application components and starts the CLI interface.
"""

from src.services.task_manager import TaskManager
from src.cli.cli_interface import CLIInterface


def main():
    """
    Main function to run the TODO CLI application.
    
    Initializes the TaskManager and CLIInterface, then starts the application loop.
    """
    # Initialize the task manager
    task_manager = TaskManager()
    
    # Initialize the CLI interface with the task manager
    cli_interface = CLIInterface(task_manager)
    
    # Start the application
    cli_interface.run()


if __name__ == "__main__":
    main()