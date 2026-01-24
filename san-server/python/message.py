from typing import TypedDict
import json


class BaseMsg(TypedDict):
    """
    {
        "name": str,
        "desc": str,
        "token": str,
        "data": bytes,
    }
    """

    name: str
    desc: str
    token: str
    data: bytes


class Message:
    """
    {
        "name": str,
        "desc": str,
        "data": bytes,
        "addr": str,
        "message": BaseMsg
    }
    """

    def __init__(self, message: BaseMsg, addr: str = ""):
        self.message = message
        self.addr = addr
        self.name = message["name"]
        self.desc = message["desc"]
        self.data = message["data"]

    def __str__(self):
        return f"Message from {self.addr}: {self.name}"

    def to_bytes(self) -> bytes:
        ojson = json.dumps(self.message)
        return ojson.encode("utf-8")
