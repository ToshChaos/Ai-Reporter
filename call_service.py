from flask import render_template
import json

from models import Device, Operation, Ticket

class CallService:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all call information."""
        self.last_call_id = None
        self.device = None
        self.operations = []
        self.tickets = []
        self.finished = False

    def set_device(self, call_id, device_id):
        """Set device ID for the current call."""
        if call_id != self.last_call_id:
            self.save_call()
            self.reset()

        self.last_call_id = call_id
        self.device = Device(device_id)

    def process_operations(self, call_id, json_data):
        """Insert operations into the list or update existing ones."""
        if not isinstance(json_data, dict):
            return

        self.last_call_id = call_id
        call_op = json_data.get("operation")
        finished = json_data.get("finished", False)  # Default False

        if isinstance(call_op, str):
            # Check if operation exists and update it
            existing_op = next((op for op in self.operations if op.name == call_op.capitalize()), None)
            if existing_op:
                existing_op.finished = finished
            else:
                self.operations.append(Operation(call_op, finished))

        self.finished = False

    def process_tickets(self, call_id, json_data):
        """Insert tickets into the list."""
        if not isinstance(json_data, dict):
            return

        self.last_call_id = call_id
        call_ticket = json_data.get("ticket")
        if isinstance(call_ticket, dict):
            self.tickets.append(Ticket(call_ticket))

        self.finished = False

    def save_call(self, done=False):
        """Save the call data to a file."""
        call_data = {
            "id": self.last_call_id,
            "device": self.device.to_dict() if self.device else None,
            "operations": [op.to_dict() for op in self.operations],
            "tickets": [tkt.to_dict() for tkt in self.tickets],
            "done": done,
        }

        print("Saving Report:", json.dumps(call_data, indent=4))

        if self.last_call_id is None:
            print("Error: No call ID to save")
            return

        file_name = f"{self.last_call_id}.txt"
        try:
            with open(file_name, "w") as f:
                json.dump(call_data, f, indent=4)
        except IOError as e:
            print(f"Error saving file {file_name}: {e}")

        self.finished = done

    def show_call_info(self):
        """Return call statistics in HTML format."""
        return render_template(
            "call_info.html",
            last_call_id=self.last_call_id,
            call_operations=[op.to_dict() for op in self.operations],
            call_finished=self.finished,
            call_tickets=[tkt.to_dict() for tkt in self.tickets],
            device=self.device.to_dict() if self.device else None,
        )


# Create a single instance of CallService
call_service = CallService()
