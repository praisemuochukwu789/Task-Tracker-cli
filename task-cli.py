import sys
# Grab the arguments from the list
action = sys.argv[1]
task_name = sys.argv[2]

# Check if the user typed "add"
if action.lower() == "add":
    tasks = [
        {"id": 1, "description": "Buy groceries", "status": "done"},
        {"id": 2, "description": "Cook dinner", "status": "todo"}
    ]

# Calculate the next unique ID
if len(tasks) == 0:
    new_id = 1
else:
    # Find the highest ID used so far and add 1
    new_id = max(task["id"] for task in tasks) + 1

print(f"New task ID will be: {new_id}")  # Outputs: New task ID will be: 3
print(f"Task added: {task_name}")