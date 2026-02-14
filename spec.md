# Specification: Console-Based To-Do Application

**Course:** Fundamental of Agentic AI - NED PGD
**Title:** Final Exam
**Date:** 2026-02-14
**Author:** Asim Khan

---

## 1. Overview

A simple console-based To-Do application that allows users to manage tasks through a command-line interface. The application supports adding, updating, categorizing, and deleting tasks.

## 2. Functional Requirements

### 2.1 Core Features

| Feature | Description |
|---------|-------------|
| **Add Task** | Create a new task with title, description, and category |
| **View Tasks** | Display all tasks or filter by category |
| **Update Task** | Modify task title, description, or category |
| **Delete Task** | Remove a task from the list |
| **Categorize** | Assign categories (Work, Personal, Shopping, Health, Other) |

### 2.2 User Interface

- Interactive menu-driven console interface
- Clear prompts and feedback messages
- Input validation for all operations

## 3. Data Model

```
Task:
  - id: Integer (auto-generated)
  - title: String (required)
  - description: String (optional)
  - category: String (Work | Personal | Shopping | Health | Other)
  - created_at: DateTime
  - completed: Boolean
```

## 4. Menu Structure

```
========== TO-DO APP ==========
1. Add Task
2. View All Tasks
3. View Tasks by Category
4. Update Task
5. Delete Task
6. Mark Task Complete/Incomplete
7. Exit
===============================
```

## 5. Acceptance Criteria

- [ ] User can add a task with title and category
- [ ] User can view all tasks with their details
- [ ] User can filter tasks by category
- [ ] User can update any task field
- [ ] User can delete a task by ID
- [ ] User can mark tasks as complete/incomplete
- [ ] Data persists in a JSON file
- [ ] Input validation prevents crashes

## 6. Technical Constraints

- Python 3.8+
- No external dependencies (standard library only)
- JSON file for data persistence
- Single-file implementation for simplicity
