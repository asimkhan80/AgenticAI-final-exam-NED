"""
Console-Based To-Do Application
================================
Course: Fundamental of Agentic AI - NED PGD
Title: Final Exam
Date: 2026-02-14
Author: Asim Khan

Development Approach: Specs-Driven Development (SDD) with Claude Code

This application demonstrates:
1. CRUD operations (Create, Read, Update, Delete)
2. Data persistence using JSON
3. Category-based organization
4. Interactive console interface
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional


# =============================================================================
# DATA MODEL
# =============================================================================

@dataclass
class Task:
    """Represents a single to-do task."""
    id: int
    title: str
    description: str
    category: str
    created_at: str
    completed: bool = False


# =============================================================================
# CONSTANTS
# =============================================================================

CATEGORIES = ["Work", "Personal", "Shopping", "Health", "Other"]
DATA_FILE = "tasks.json"


# =============================================================================
# TO-DO APPLICATION CLASS
# =============================================================================

class TodoApp:
    """Main application class for managing to-do tasks."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self.load_from_file()

    # -------------------------------------------------------------------------
    # PERSISTENCE METHODS
    # -------------------------------------------------------------------------

    def save_to_file(self) -> None:
        """Save all tasks to JSON file."""
        data = {
            "next_id": self.next_id,
            "tasks": [asdict(task) for task in self.tasks]
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self) -> None:
        """Load tasks from JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.next_id = data.get("next_id", 1)
                    self.tasks = [Task(**task) for task in data.get("tasks", [])]
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                self.next_id = 1

    # -------------------------------------------------------------------------
    # CRUD OPERATIONS
    # -------------------------------------------------------------------------

    def add_task(self, title: str, description: str, category: str) -> Task:
        """Add a new task to the list."""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            category=category,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file()
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.tasks

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks filtered by category."""
        return [task for task in self.tasks if task.category == category]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None,
                    description: str = None, category: str = None) -> bool:
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description is not None:
                task.description = description
            if category:
                task.category = category
            self.save_to_file()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_to_file()
            return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle task completion status."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            self.save_to_file()
            return True
        return False


# =============================================================================
# CONSOLE INTERFACE
# =============================================================================

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the application header."""
    print("\n" + "=" * 50)
    print("       TO-DO CONSOLE APPLICATION")
    print("       NED PGD - Agentic AI Final Exam")
    print("       Date: 2026-02-14")
    print("=" * 50)


def print_menu():
    """Print the main menu."""
    print("\n--- MAIN MENU ---")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Tasks by Category")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Mark Task Complete/Incomplete")
    print("7. Exit")
    print("-" * 20)


def print_task(task: Task):
    """Print a single task in a formatted way."""
    status = "[X]" if task.completed else "[ ]"
    print(f"\n  {status} Task #{task.id}")
    print(f"      Title: {task.title}")
    print(f"      Description: {task.description or 'No description'}")
    print(f"      Category: {task.category}")
    print(f"      Created: {task.created_at}")


def print_tasks(tasks: List[Task], title: str = "Tasks"):
    """Print a list of tasks."""
    print(f"\n--- {title} ({len(tasks)} items) ---")
    if not tasks:
        print("  No tasks found.")
    else:
        for task in tasks:
            print_task(task)


def select_category() -> str:
    """Prompt user to select a category."""
    print("\nAvailable Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")

    while True:
        try:
            choice = int(input("\nSelect category (1-5): "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")


def get_task_id() -> int:
    """Prompt user for task ID."""
    while True:
        try:
            return int(input("\nEnter Task ID: "))
        except ValueError:
            print("Please enter a valid number.")


# =============================================================================
# MENU HANDLERS
# =============================================================================

def handle_add_task(app: TodoApp):
    """Handle adding a new task."""
    print("\n--- ADD NEW TASK ---")
    title = input("Enter task title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return

    description = input("Enter description (optional): ").strip()
    category = select_category()

    task = app.add_task(title, description, category)
    print(f"\nTask #{task.id} added successfully!")


def handle_view_all(app: TodoApp):
    """Handle viewing all tasks."""
    tasks = app.get_all_tasks()
    print_tasks(tasks, "ALL TASKS")


def handle_view_by_category(app: TodoApp):
    """Handle viewing tasks by category."""
    category = select_category()
    tasks = app.get_tasks_by_category(category)
    print_tasks(tasks, f"{category.upper()} TASKS")


def handle_update_task(app: TodoApp):
    """Handle updating a task."""
    print("\n--- UPDATE TASK ---")
    handle_view_all(app)

    if not app.get_all_tasks():
        return

    task_id = get_task_id()
    task = app.get_task_by_id(task_id)

    if not task:
        print(f"Error: Task #{task_id} not found.")
        return

    print(f"\nUpdating Task #{task_id}")
    print("(Press Enter to keep current value)\n")

    new_title = input(f"New title [{task.title}]: ").strip()
    new_desc = input(f"New description [{task.description}]: ").strip()

    print("\nChange category?")
    change_cat = input("Enter 'y' to change, or press Enter to keep: ").lower()
    new_category = select_category() if change_cat == 'y' else None

    app.update_task(
        task_id,
        title=new_title or None,
        description=new_desc if new_desc else None,
        category=new_category
    )
    print(f"\nTask #{task_id} updated successfully!")


def handle_delete_task(app: TodoApp):
    """Handle deleting a task."""
    print("\n--- DELETE TASK ---")
    handle_view_all(app)

    if not app.get_all_tasks():
        return

    task_id = get_task_id()

    confirm = input(f"Are you sure you want to delete Task #{task_id}? (y/n): ")
    if confirm.lower() == 'y':
        if app.delete_task(task_id):
            print(f"\nTask #{task_id} deleted successfully!")
        else:
            print(f"Error: Task #{task_id} not found.")
    else:
        print("Deletion cancelled.")


def handle_toggle_complete(app: TodoApp):
    """Handle marking task as complete/incomplete."""
    print("\n--- TOGGLE TASK STATUS ---")
    handle_view_all(app)

    if not app.get_all_tasks():
        return

    task_id = get_task_id()

    if app.toggle_complete(task_id):
        task = app.get_task_by_id(task_id)
        status = "completed" if task.completed else "incomplete"
        print(f"\nTask #{task_id} marked as {status}!")
    else:
        print(f"Error: Task #{task_id} not found.")


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Main application entry point."""
    app = TodoApp()

    print_header()
    print("\nWelcome! This is a console-based To-Do application.")
    print("Developed using Specs-Driven Development with Claude Code.")

    while True:
        print_menu()

        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                handle_add_task(app)
            elif choice == "2":
                handle_view_all(app)
            elif choice == "3":
                handle_view_by_category(app)
            elif choice == "4":
                handle_update_task(app)
            elif choice == "5":
                handle_delete_task(app)
            elif choice == "6":
                handle_toggle_complete(app)
            elif choice == "7":
                print("\nThank you for using the To-Do App!")
                print("Goodbye!\n")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            print("\n\nExiting application...")
            break

        input("\nPress Enter to continue...")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
