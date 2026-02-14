# Console-Based To-Do Application

**Course:** Fundamental of Agentic AI - NED PGD
**Title:** Final Exam
**Date:** 2026-02-14
**Author:** Asim Khan

---

## Overview

A simple console-based To-Do application built using **Specs-Driven Development (SDD)** with **Claude Code** as an AI pair programmer.

## Features

- **Add Task** - Create tasks with title, description, and category
- **View Tasks** - Display all tasks or filter by category
- **Update Task** - Modify existing task details
- **Delete Task** - Remove tasks from the list
- **Categorize** - Organize tasks (Work, Personal, Shopping, Health, Other)
- **Complete/Incomplete** - Toggle task completion status
- **Persistence** - Data saved to JSON file

---

## Development Process: Specs-Driven Development (SDD)

### What is SDD?

Specs-Driven Development is a methodology where development follows a structured flow:

```
1. SPECIFICATION  -->  2. PLANNING  -->  3. IMPLEMENTATION  -->  4. VALIDATION
      (spec.md)          (plan.md)         (todo_app.py)          (testing)
```

### Step 1: Specification (`spec.md`)

First, we defined WHAT the application should do:
- Core features (CRUD operations)
- Data model (Task structure)
- User interface (Menu system)
- Acceptance criteria (Testable requirements)

### Step 2: Planning (`plan.md`)

Next, we designed HOW to implement it:
- Architecture decisions
- Module structure
- Data flow
- Error handling strategy

### Step 3: Implementation (`todo_app.py`)

Finally, we wrote code that fulfills the specification:
- `Task` dataclass for data structure
- `TodoApp` class for business logic
- Console interface for user interaction
- JSON persistence for data storage

---

## How Claude Code Helped

Claude Code acted as an AI pair programmer that:

1. **Understood Requirements** - Translated natural language specs to code
2. **Applied Best Practices** - Used dataclasses, type hints, clean architecture
3. **Generated Documentation** - Created inline comments and docstrings
4. **Ensured Consistency** - Maintained coding standards throughout
5. **Handled Edge Cases** - Added input validation and error handling

---

## Project Structure

```
todo-console-app/
    |-- README.md          # This file - Project documentation
    |-- spec.md            # Feature specification
    |-- plan.md            # Implementation plan
    |-- todo_app.py        # Main application code
    |-- tasks.json         # Data storage (auto-created)
```

---

## How to Run

### Prerequisites
- Python 3.8 or higher

### Steps

1. Clone the repository:
```bash
git clone https://github.com/asimkhan80/AgenticAI-final-exam-NED.git
cd AgenticAI-final-exam-NED
```

2. Run the application:
```bash
python todo_app.py
```

3. Follow the on-screen menu to manage your tasks.

---

## Code Explanation

### 1. Data Model (Task)

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    category: str
    created_at: str
    completed: bool = False
```

Uses Python's `dataclass` decorator for clean, self-documenting data structure.

### 2. Application Class (TodoApp)

```python
class TodoApp:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_from_file()

    def add_task(self, title, description, category) -> Task:
        # Creates and saves a new task

    def update_task(self, task_id, ...) -> bool:
        # Updates existing task

    def delete_task(self, task_id) -> bool:
        # Removes task from list
```

Encapsulates all business logic with clear method signatures.

### 3. Persistence

```python
def save_to_file(self):
    data = {"tasks": [asdict(task) for task in self.tasks]}
    with open("tasks.json", "w") as f:
        json.dump(data, f)
```

Uses JSON for human-readable, portable data storage.

### 4. User Interface

```python
def main():
    app = TodoApp()
    while True:
        print_menu()
        choice = input("Enter choice: ")
        # Handle user selection
```

Simple menu-driven interface with input validation.

---

## Sample Output

```
==================================================
       TO-DO CONSOLE APPLICATION
       NED PGD - Agentic AI Final Exam
       Date: 2026-02-14
==================================================

--- MAIN MENU ---
1. Add Task
2. View All Tasks
3. View Tasks by Category
4. Update Task
5. Delete Task
6. Mark Task Complete/Incomplete
7. Exit
--------------------
Enter your choice (1-7): 1

--- ADD NEW TASK ---
Enter task title: Complete Final Exam
Enter description (optional): Submit Agentic AI project
Available Categories:
  1. Work
  2. Personal
  3. Shopping
  4. Health
  5. Other
Select category (1-5): 1

Task #1 added successfully!
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| dataclasses | Data structure definition |
| JSON | Data persistence |
| typing | Type annotations |

---

## License

MIT License - Feel free to use and modify.

---

## Acknowledgments

- **NED University** - PGD in Agentic AI
- **Claude Code** - AI pair programming assistant
- **Anthropic** - AI technology provider
