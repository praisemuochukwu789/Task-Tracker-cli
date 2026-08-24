# Task Tracker CLI

A lightweight, high-performance Command Line Interface (CLI) application built in Python for managing daily tasks and tracking progress straight from your terminal. 

This project was built following the backend project specification on [roadmap.sh](https://roadmap.sh/projects/task-tracker).

---

## Key Features

- **Global Execution**: Installed as a native system command using Python packaging standards (`setuptools` / `pyproject.toml`).
- **Centralized Data Persistence**: Saves and manages tasks in a single JSON store located in the user home directory (`~/tasks.json`), making your task database accessible across any working directory.
- **Dynamic Task Lifecycle Management**: Add, update descriptions, mark status transitions (`todo`, `in-progress`, `done`), and delete tasks cleanly.
- **Flexible List Filtering**: Filter task views dynamically by status or display the full backlog at once.
- **Robust Error Handling & ISO Timestamps**: Formats creation/update timestamps into human-readable strings while ensuring data corruption is caught gracefully.

---

## Project Structure

```text
Task-Tracker/
│
├── src/
│   ├── __init__.py      # Package indicator
│   ├── task.py          # Main CLI entry point & argument handler
│   ├── models.py        # Data schema definitions & timestamp formatters
│   └── storage.py       # JSON storage driver & file I/O layer
│
├── pyproject.toml       # Modern Python packaging configuration
├── .gitignore           # Git ignore settings
└── README.md            # Project documentation
```

---

## Installation & Setup

### Prerequisites

- **Python 3.8+** installed on your system.
- **Git Bash**, **PowerShell**, or standard Linux/macOS Terminal.

### Local Installation (Editable Mode)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/task-tracker-cli.git
   cd task-tracker-cli
   ```

2. **Install the CLI globally in editable mode**:
   ```bash
   pip install -e .
   ```

   *Note: Using `-e` allows any live changes made in the `src/` directory to instantly reflect in your global `task` command without needing reinstallation.*

---

## Usage Guide & Command Examples

### 1. Adding a Task
Add new tasks to your task list. The system automatically assigns an incrementing unique ID and records the ISO creation timestamp.

```bash
task add "Buy groceries and prep dinner"
```
**Output:**
```text
Task added successfully (ID: 1)
```

---

### 2. Listing Tasks
You can view all tasks or filter them specifically by status (`todo`, `in-progress`, `done`).

- **List all tasks:**
  ```bash
  task list
  ```
  **Output:**
  ```text
  [1] Buy groceries and prep dinner (todo)
      Created: 25 Aug 2026, 00:02 | Updated: 25 Aug 2026, 00:02
  ```

- **Filter by status:**
  ```bash
  task list todo
  task list in-progress
  task list done
  ```

---

### 3. Updating Task Descriptions
Modify existing task descriptions by providing the target task ID.

```bash
task update 1 "Buy organic groceries and cook dinner"
```
**Output:**
```text
Task 1 updated successfully!
```

---

### 4. Updating Task Status
Transition task states smoothly between `in-progress` and `done`.

- **Mark as in-progress:**
  ```bash
  task mark-in-progress 1
  ```

- **Mark as done:**
  ```bash
  task mark-done 1
  ```

---

### 5. Deleting a Task
Remove completed or unneeded tasks by ID.

```bash
task delete 1
```
**Output:**
```text
Task 1 deleted successfully!
```

---

## Data Schema & Storage

Tasks are persisted in standard JSON inside `~/tasks.json`. Each task object adheres to the following structural schema:

```json
[
    {
        "id": 1,
        "description": "Buy organic groceries and cook dinner",
        "status": "done",
        "createdAt": "2026-08-25T00:02:14.819201",
        "updatedAt": "2026-08-25T00:15:30.104822"
    }
]
```

---

## Architecture Overview

- **`src/task.py`**: Reads command-line arguments, orchestrates business logic, and outputs formatted terminal responses.
- **`src/models.py`**: Encapsulates schema blueprints, timestamp generation (`get_now_iso`), and timestamp parsing (`format_timestamp`).
- **`src/storage.py`**: Manages isolated read/write file IO operations with atomic JSON updates and exception safety (`json.JSONDecodeError`, `OSError`).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.