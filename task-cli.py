import sys
import storage
import models

def main():
    if len(sys.argv) < 2:
        print("Please provide a command. Example: python task-cli.py add \"Buy groceries\"")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) != 3:
            print("Error: Missing task description! Usage: python task-cli.py add \"Buy groceries\"")
            return
        
        task_name = sys.argv[2]
        tasks = storage.load_tasks()

        new_id = 1 if len(tasks) == 0 else max(task["id"] for task in tasks) + 1
        new_task = models.create_task_blueprint(new_id, task_name)

        tasks.append(new_task)
        storage.save_tasks(tasks)
        print(f"Task added successfully (ID: {new_id})")

    elif command == "list":
        tasks = storage.load_tasks()

        if len(tasks) == 0:
            print("No tasks found.")
            return

        status_filter = sys.argv[2].lower() if len(sys.argv) > 2 else None

        for task in tasks:
            if status_filter is None or task["status"] == status_filter:
                created_str = models.format_timestamp(task.get("createdAt", ""))
                updated_str = models.format_timestamp(task.get("updatedAt", ""))

                print(f"[{task['id']}] {task['description']} ({task['status']})")
                print(f"    Created: {created_str} | Updated: {updated_str}")

    elif command in ["mark-in-progress", "mark-done"]:
        if len(sys.argv) < 3:
            print(f"Error: Missing task ID! Usage: python task-cli.py {command} <id>")
            return

        try:
            target_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a valid number!")
            return

        tasks = storage.load_tasks()
        new_status = "in-progress" if command == "mark-in-progress" else "done"
        task_found = False

        for task in tasks:
            if task["id"] == target_id:
                task["status"] = new_status
                task["updatedAt"] = models.get_now_iso()
                task_found = True
                break

        if not task_found:
            print(f"Error: Task with ID {target_id} not found.")
            return

        storage.save_tasks(tasks)
        print(f"Task {target_id} marked as {new_status} successfully!")

    elif command == "update":
        if len(sys.argv) < 4:
            print('Error: Missing arguments! Usage: python task-cli.py update <id> "New description"')
            return

        try:
            target_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a valid number!")
            return

        new_description = sys.argv[3]
        tasks = storage.load_tasks()
        task_found = False

        for task in tasks:
            if task["id"] == target_id:
                task["description"] = new_description
                task["updatedAt"] = models.get_now_iso()
                task_found = True
                break

        if not task_found:
            print(f"Error: Task with ID {target_id} not found.")
            return

        storage.save_tasks(tasks)
        print(f"Task {target_id} updated successfully!")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Missing task ID! Usage: python task-cli.py delete <id>")
            return

        try:
            target_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a valid number!")
            return

        tasks = storage.load_tasks()
        initial_count = len(tasks)
        tasks = [task for task in tasks if task["id"] != target_id]

        if len(tasks) == initial_count:
            print(f"Error: Task with ID {target_id} not found.")
            return

        storage.save_tasks(tasks)
        print(f"Task {target_id} deleted successfully!")

if __name__ == "__main__":
    main()