"""
To-Do Web Application (Gradio Interface)
==========================================
Course: Fundamental of Agentic AI - NED PGD
Title: Final Exam
Date: 2026-02-14
Author: Asim Khan

Development Approach: Specs-Driven Development (SDD) with Claude Code
"""

import gradio as gr
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

    def add_task(self, title: str, description: str, category: str) -> str:
        """Add a new task to the list."""
        if not title.strip():
            return "Error: Title cannot be empty!"

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            category=category,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file()
        return f"Task #{task.id} '{task.title}' added successfully!"

    def get_tasks_display(self, filter_category: str = "All") -> str:
        """Get formatted display of tasks."""
        tasks = self.tasks
        if filter_category != "All":
            tasks = [t for t in tasks if t.category == filter_category]

        if not tasks:
            return "No tasks found."

        output = []
        for task in tasks:
            status = "[DONE]" if task.completed else "[    ]"
            output.append(
                f"{status} #{task.id} | {task.title}\n"
                f"        Category: {task.category} | Created: {task.created_at}\n"
                f"        Description: {task.description or 'No description'}"
            )
        return "\n\n".join(output)

    def update_task(self, task_id: int, title: str, description: str, category: str) -> str:
        """Update an existing task."""
        for task in self.tasks:
            if task.id == task_id:
                if title.strip():
                    task.title = title.strip()
                if description.strip():
                    task.description = description.strip()
                if category:
                    task.category = category
                self.save_to_file()
                return f"Task #{task_id} updated successfully!"
        return f"Error: Task #{task_id} not found!"

    def delete_task(self, task_id: int) -> str:
        """Delete a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_to_file()
                return f"Task #{task_id} deleted successfully!"
        return f"Error: Task #{task_id} not found!"

    def toggle_complete(self, task_id: int) -> str:
        """Toggle task completion status."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                status = "completed" if task.completed else "incomplete"
                self.save_to_file()
                return f"Task #{task_id} marked as {status}!"
        return f"Error: Task #{task_id} not found!"

    def get_task_ids(self) -> List[int]:
        """Get list of all task IDs."""
        return [task.id for task in self.tasks]


# =============================================================================
# GRADIO INTERFACE
# =============================================================================

# Initialize the app
app = TodoApp()


def add_task(title, description, category):
    result = app.add_task(title, description, category)
    tasks_display = app.get_tasks_display()
    return result, tasks_display, "", ""  # Clear inputs


def view_tasks(filter_category):
    return app.get_tasks_display(filter_category)


def update_task(task_id, title, description, category):
    if not task_id:
        return "Error: Please enter a Task ID!", app.get_tasks_display()
    try:
        tid = int(task_id)
        result = app.update_task(tid, title, description, category)
        return result, app.get_tasks_display()
    except ValueError:
        return "Error: Invalid Task ID!", app.get_tasks_display()


def delete_task(task_id):
    if not task_id:
        return "Error: Please enter a Task ID!", app.get_tasks_display()
    try:
        tid = int(task_id)
        result = app.delete_task(tid)
        return result, app.get_tasks_display()
    except ValueError:
        return "Error: Invalid Task ID!", app.get_tasks_display()


def toggle_task(task_id):
    if not task_id:
        return "Error: Please enter a Task ID!", app.get_tasks_display()
    try:
        tid = int(task_id)
        result = app.toggle_complete(tid)
        return result, app.get_tasks_display()
    except ValueError:
        return "Error: Invalid Task ID!", app.get_tasks_display()


def refresh_tasks():
    return app.get_tasks_display()


# =============================================================================
# BUILD INTERFACE
# =============================================================================

with gr.Blocks(title="To-Do App - NED PGD Final Exam", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # To-Do Application
    ### NED PGD - Fundamental of Agentic AI - Final Exam
    **Date:** 2026-02-14 | **Developed with:** Specs-Driven Development + Claude Code
    ---
    """)

    with gr.Row():
        # Left column - Task List
        with gr.Column(scale=2):
            gr.Markdown("### Task List")
            filter_dropdown = gr.Dropdown(
                choices=["All"] + CATEGORIES,
                value="All",
                label="Filter by Category"
            )
            tasks_display = gr.Textbox(
                value=app.get_tasks_display(),
                label="Tasks",
                lines=15,
                interactive=False
            )
            refresh_btn = gr.Button("Refresh Tasks", variant="secondary")

        # Right column - Actions
        with gr.Column(scale=1):
            with gr.Tab("Add Task"):
                add_title = gr.Textbox(label="Title", placeholder="Enter task title...")
                add_desc = gr.Textbox(label="Description", placeholder="Optional description...")
                add_category = gr.Dropdown(choices=CATEGORIES, value="Work", label="Category")
                add_btn = gr.Button("Add Task", variant="primary")
                add_result = gr.Textbox(label="Result", interactive=False)

            with gr.Tab("Update Task"):
                update_id = gr.Textbox(label="Task ID", placeholder="Enter task ID...")
                update_title = gr.Textbox(label="New Title", placeholder="Leave empty to keep current...")
                update_desc = gr.Textbox(label="New Description", placeholder="Leave empty to keep current...")
                update_category = gr.Dropdown(choices=CATEGORIES, value="Work", label="New Category")
                update_btn = gr.Button("Update Task", variant="primary")
                update_result = gr.Textbox(label="Result", interactive=False)

            with gr.Tab("Delete Task"):
                delete_id = gr.Textbox(label="Task ID", placeholder="Enter task ID to delete...")
                delete_btn = gr.Button("Delete Task", variant="stop")
                delete_result = gr.Textbox(label="Result", interactive=False)

            with gr.Tab("Toggle Complete"):
                toggle_id = gr.Textbox(label="Task ID", placeholder="Enter task ID...")
                toggle_btn = gr.Button("Toggle Complete/Incomplete", variant="primary")
                toggle_result = gr.Textbox(label="Result", interactive=False)

    gr.Markdown("""
    ---
    ### Development Process: Specs-Driven Development (SDD)
    1. **Specification** (`spec.md`) - Defined features and requirements
    2. **Planning** (`plan.md`) - Designed architecture and data flow
    3. **Implementation** (`app.py`) - Built with Claude Code assistance

    **Features:** Add, Update, Delete, Categorize, Complete/Incomplete, Filter by Category
    """)

    # Event handlers
    add_btn.click(
        add_task,
        inputs=[add_title, add_desc, add_category],
        outputs=[add_result, tasks_display, add_title, add_desc]
    )

    update_btn.click(
        update_task,
        inputs=[update_id, update_title, update_desc, update_category],
        outputs=[update_result, tasks_display]
    )

    delete_btn.click(
        delete_task,
        inputs=[delete_id],
        outputs=[delete_result, tasks_display]
    )

    toggle_btn.click(
        toggle_task,
        inputs=[toggle_id],
        outputs=[toggle_result, tasks_display]
    )

    filter_dropdown.change(
        view_tasks,
        inputs=[filter_dropdown],
        outputs=[tasks_display]
    )

    refresh_btn.click(
        refresh_tasks,
        outputs=[tasks_display]
    )


# =============================================================================
# LAUNCH
# =============================================================================

if __name__ == "__main__":
    demo.launch()
