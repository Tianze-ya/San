from message import BaseMsg, Message
from san_server import SanServer
import hashlib
from tool import make_msg
from log import Logger

logger = Logger(__file__)


class ClientMessage:
    def __init__(self, message: BaseMsg, addr: str = "", server: SanServer = None):
        self.msg = Message(message, addr)
        self.server = server

    def __str__(self):
        return f"ClientMessage from {self.msg.addr}: {self.msg.name}"

    async def re_msg(
        self, name: str = "", desc: str = "", data: bytes = b"", addr: str = ""
    ) -> None:
        await self.server.send_message(make_msg(name, desc, data, addr))

    async def exec(self) -> str:
        match self.msg.name:
            case "message":
                ...
            case "photo":
                hash = hashlib.sha256(self.data).hexdigest()
                with open(f"photos/{hash}.jpg", "wb") as f:
                    f.write(self.data)
                return "ok"
            case _:
                ...
