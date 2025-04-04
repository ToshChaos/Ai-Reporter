class Operation:
    def __init__(self, name):
        self.name = name.capitalize()

    def to_dict(self):
        return {"name": self.name}


class Ticket:
    def __init__(self, details):
        self.details = {
            key: value.capitalize() if isinstance(value, str) else value
            for key, value in details.items()
        }

        # Add default fields if not provided
        self.details.setdefault("reporter", "Unknown")
        self.details.setdefault("status", "Open")

    def to_dict(self):
        return self.details

