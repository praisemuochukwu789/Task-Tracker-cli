import json
from pathlib import Path

# Path.home() finds your central user directory on any OS (Windows, macOS, Linux)
# On Windows, this resolves to: C:\Users\DELL\tasks.json
FILE_PATH = Path.home() / "tasks.json"


def load_tasks():
    """Loads tasks from the central JSON file. Returns an empty list if missing or corrupted."""
    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Saves the tasks list to the central JSON file."""
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"Error saving tasks to file: {e}")