from flask import render_template
import json

class CallService:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all call information."""
        self.last_call_id = None
        self.operations = []
        self.tickets = []
        self.finished = False

    def process_operations(self, call_id, json_data):
        """Insert operations into the list."""
        if not isinstance(json_data, dict):
            return  # Invalid input, ignore

        self.last_call_id = call_id
        call_op = json_data.get("operation")
        if isinstance(call_op, str):  # Ensure it's a string before processing
            self.operations.append(call_op.capitalize())

        self.finished = False

    def process_tickets(self, call_id, json_data):
        """Insert tickets into the list."""
        if not isinstance(json_data, dict):
            return  # Invalid input, ignore

        self.last_call_id = call_id
        call_ticket = json_data.get("ticket")
        if isinstance(call_ticket, dict):  # Ensure it's a dictionary before processing
            call_ticket = {
                key: value.capitalize() if isinstance(value, str) else value
                for key, value in call_ticket.items()
            }
            self.tickets.append(call_ticket)

        self.finished = False

    def save_call(self, done=False):
        """Save the call data to a file."""
        call_data = {
            "id": self.last_call_id,
            "operations": self.operations,
            "tickets": self.tickets,  # Fixed bug here
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
            call_operations=self.operations,
            call_finished=self.finished,
            call_tickets=self.tickets,
        )

# Create a single instance of CallInfo
call_service = CallService()
