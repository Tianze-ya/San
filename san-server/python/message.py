import hashlib
from typing import TypedDict
import json


class BaseMsg(TypedDict):
    """
    {
        "name": "",
        "msg": "",
        "data": "",
    }
    """

    name: str
    msg: str
    data: bytes


class Message:
    def __init__(self, message: BaseMsg, addr: str = ""):
        self.message = message
        self.addr = addr
        self.name = message["name"]
        self.data = message["data"]

    def __str__(self):
        return f"Message from {self.addr}: {self.name}"

    def to_bytes(self) -> bytes:
        ojson = json.dumps(self.message)
        return ojson.encode("utf-8")

    def exec(self) -> str:
        match self.name:
            case "message":
                ...
            case "photo":
                hash = hashlib.sha256(self.data).hexdigest()
                with open(f"photos/{hash}.jpg", "wb") as f:
                    f.write(self.data)
                return "ok"
            case _:
                ...


def make_msg(
    name: str = "", msg: str = "", data: bytes = b"", addr: str = ""
) -> Message:
    return Message({"name": name, "msg": msg, "data": data}, addr)
