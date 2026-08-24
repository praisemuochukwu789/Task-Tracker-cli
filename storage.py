import json
import os

FILENAME = "tasks.json"

def load_tasks():
    """Reads tasks from the JSON file safely."""
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    """Writes the updated task list back to the JSON file."""
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)