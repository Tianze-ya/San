class Meessage:
    def __init__(self, message: dict, addr: str):
        self.message = message
        self.addr = addr
        self.name = message["name"]
        self.data = message["data"]

    def __str__(self):
        return f"Message from {self.addr}: {self.name}"

    def exec(self): ...
