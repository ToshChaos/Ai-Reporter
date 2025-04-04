from flask import render_template
import json

from models import Operation, Ticket

class CallService:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all call information."""
        self.call_id = None
        self.device_id = None
        self.operations = []
        self.tickets = []

    def check_new_call(self, call_id):
        if self.call_id and call_id != self.call_id:
            self.save_call()
            self.reset()

    def set_device(self, call_id, device_id):
        """Set device ID for the current call."""
        self.call_id = call_id
        self.device_id = device_id

    def process_operations(self, call_id, json_data):
        """Insert operations into the list or update existing ones."""
        if not isinstance(json_data, dict):
            return

        self.call_id = call_id
        call_op = json_data.get("operation")

        if isinstance(call_op, str):
            self.operations.append(Operation(call_op.capitalize()))

    def process_tickets(self, call_id, json_data):
        """Insert tickets into the list."""
        if not isinstance(json_data, dict):
            return

        self.call_id = call_id
        call_ticket = json_data.get("ticket")
        if isinstance(call_ticket, dict):
            self.tickets.append(Ticket(call_ticket))

    def save_call(self):
        """Save the call data to a file."""
        call_data = {
            "id": self.call_id,
            "device": self.device_id,
            "operations": [op.to_dict() for op in self.operations],
            "tickets": [tkt.to_dict() for tkt in self.tickets],
        }

        print("Saving Report:", json.dumps(call_data, indent=4))

        if self.device_id is None:
            print("Error: No device ID to save")
            return 400
        elif self.call_id is None:
            print("Error: No call ID to save")
            return 400

        file_name = f"{self.call_id}.txt"
        try:
            with open(file_name, "w") as f:
                json.dump(call_data, f, indent=4)
        except IOError as e:
            print(f"Error saving file {file_name}: {e}")

    def show_call_info(self):
        """Return call statistics in HTML format."""
        return render_template(
            "call_info.html",
            call_id=self.call_id,
            device_id=self.device_id,
            call_operations=[op.to_dict() for op in self.operations],
            call_tickets=[tkt.to_dict() for tkt in self.tickets]
        )

# Create a single instance of CallService
call_service = CallService()
