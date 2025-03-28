class Operation:
    def __init__(self, name, finished=False):
        self.name = name.capitalize()
        self.finished = finished

    def to_dict(self):
        return {"name": self.name, "finished": self.finished}


class Ticket:
    def __init__(self, details):
        self.details = {
            key: value.capitalize() if isinstance(value, str) else value
            for key, value in details.items()
        }

    def to_dict(self):
        return self.details


class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    def to_dict(self):
        return {"device_id": self.device_id}