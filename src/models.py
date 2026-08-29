from datetime import datetime
def create_task_blueprint(new_id,  task_name):
    """Defines the strict schema for a single task."""
    now = datetime.now().isoformat()
    return {
        "id": new_id,
        "description": task_name,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
def get_now_iso():
    """Returns the current timestamp formatted in ISO 8601 string format."""
    return datetime.now().isoformat()

def format_timestamp(iso_str):
    """Converts ISO string to readable format or N/A."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y, %H:%M")
    except (ValueError, TypeError):
        return "N/A"