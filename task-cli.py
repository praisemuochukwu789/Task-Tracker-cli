import sys
import json
import os
from datetime import datetime

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
    now = datetime.now().isoformat()
    new_task = {
        "id": new_id,
        "description": task_name,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
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

    # Check for optional status filter
    status_filter = sys.argv[2].lower() if len(sys.argv) > 2 else None

    # Print all matching tasks
    for task in tasks:
        if status_filter is None or task["status"] == status_filter:
            # Fallback values handle older tasks in tasks.json created before adding timestamps
            try:
                created_dt = datetime.fromisoformat(task.get("createdAt", ""))
                created_str = created_dt.strftime("%d %b %Y, %H:%M")
            except ValueError:
                created_str = "N/A"

            # Safely format updatedAt
            try:
                updated_dt = datetime.fromisoformat(task.get("updatedAt", ""))
                updated_str = updated_dt.strftime("%d %b %Y, %H:%M")
            except ValueError:
                updated_str = "N/A"

            print(f"[{task['id']}] {task['description']} ({task['status']})")
            print(f"    Created: {created_str} | Updated: {updated_str}")

# Handle 'mark-in-progress' and 'mark-done' commands
elif action.lower() in ["mark-in-progress", "mark-done"]:
    if len(sys.argv) < 3:
        print(f"Error: Missing task ID! Usage: python task-cli.py {action.lower()} <id>")
        sys.exit()

    try:
        target_id = int(sys.argv[2])
    except ValueError:
        print("Error: Task ID must be a valid number!")
        sys.exit()

    # Load existing tasks
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Map command directly to target status string
    new_status = "in-progress" if action.lower() == "mark-in-progress" else "done"
    task_found = False

    # Search and update status in place
    for task in tasks:
        if task["id"] == target_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if not task_found:
        print(f"Error: Task with ID {target_id} not found.")
        sys.exit()

    # Save changes back to tasks.json
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {target_id} marked as {new_status} successfully!")


elif action.lower() == "update":
    # Validate argument counts
    if len(sys.argv) < 4:
        print('Error: Missing arguments! Usage: python task-cli.py update <id> "New description"')
        sys.exit()

    # Parse and validate integer ID
    try:
        target_id = int(sys.argv[2])
    except ValueError:
        print("Error: Task ID must be a valid number!")
        sys.exit()

    new_description = sys.argv[3]

    # Load existing tasks safely
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Find task and modify description in memory
    task_found = False
    for task in tasks:
        if task["id"] == target_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if not task_found:
        print(f"Error: Task with ID {target_id} not found.")
        sys.exit()

    # Persist changes back to disk
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {target_id} updated successfully!")

elif action.lower() == "delete":
    # Validate argument count
    if len(sys.argv) < 3:
        print("Error: Missing task ID! Usage: python task-cli.py delete <id>")
        sys.exit()

    # Parse ID safely
    try:
        target_id = int(sys.argv[2])
    except ValueError:
        print("Error: Task ID must be a valid number!")
        sys.exit()

    # Load existing tasks
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Check if the task exists before deleting
    initial_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != target_id]

    if len(tasks) == initial_count:
        print(f"Error: Task with ID {target_id} not found.")
        sys.exit()

    # Save remaining tasks back to disk
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {target_id} deleted successfully!")