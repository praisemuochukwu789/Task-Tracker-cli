import sys
import json
import os

FILENAME = "tasks.json" 
# Top check: make sure they provided at least ONE action word
if len(sys.argv) < 2:
    print("Please provide a command. Example: python task-cli.py add \"Buy groceries\"")
    sys.exit()
action = sys.argv[1]
# Specific check: handle 'add' command inputs inside its own section
if action.lower() == "add":
    if len(sys.argv) != 3:
        print("Error: Missing task description! Usage: python task-cli.py add \"Buy groceries\" (wrap task in quotes!) ")
        sys.exit()
    task_name = sys.argv[2]
    # Load existing tasks from tasks.json if it exists
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Calculate the next unique ID
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = max(task["id"] for task in tasks) + 1

    # Create and append the new task
    new_task = {
        "id": new_id,
        "description": task_name,
        "status": "todo"
    }
    tasks.append(new_task)

    # Save the updated tasks list back to tasks.json
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added successfully (ID: {new_id})")

# Specific check: handle 'add' command inputs inside its own section
elif action.lower() == "list":
    # Check if tasks file exists
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    if len(tasks) == 0:
        print("No tasks found.")
        sys.exit()

    # 2. Check for optional status filter
    status_filter = sys.argv[2].lower() if len(sys.argv) > 2 else None

    # 3. Print all matching tasks
    for task in tasks:
        if status_filter is None or task["status"] == status_filter:
            print(f"[{task['id']}] {task['description']} ({task['status']})")

# elif action.lower() == "mark in progress":
