import os
import json

def get_history_by_device(device_id):
    """Retrieve past tickets and operations for a given device ID."""
    if not device_id:
        return {"error": "Missing device_id parameter"}

    history = {"tickets": [], "operations": []}

    for file_name in os.listdir():
        if file_name.endswith(".txt"):
            try:
                with open(file_name, "r") as f:
                    call_data = json.load(f)
                    if call_data.get("device", {}).get("device_id") == device_id:
                        history["tickets"].extend(call_data.get("tickets", []))
                        history["operations"].extend(call_data.get("operations", []))
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading file {file_name}: {e}")

    return history
