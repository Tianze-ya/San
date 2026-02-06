import secrets
import os
from message import Message


def generate_token(length=32):
    token = secrets.token_hex(length)
    path = os.path.join(os.path.dirname(__file__), "token")
    with open(path, "w", encoding="utf-8") as f:
        f.write(token)
    return token


def get_token():
    path = os.path.join(os.path.dirname(__file__), "token")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def make_msg(
    name: str = "", desc: str = "", data: bytes = b"", addr: str = ""
) -> Message:
    return Message({"name": name, "desc": desc, "token": "", "data": data}, addr)
