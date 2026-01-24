from message import BaseMsg, Message
from san_server import SanServer
from tool import make_msg
from log import Logger

logger = Logger(__file__)


class ServerMessage:
    def __init__(self, message: BaseMsg, addr: str = "", server: SanServer = None):
        self.msg = Message(message, addr)
        self.server = server

    def __str__(self):
        return f"ServerMessage from {self.msg.addr}: {self.msg.name}"

    async def re_msg(self, name: str = "", desc: str = "", data: bytes = b"") -> None:
        await self.server.send_message(make_msg(name, desc, data, self.msg.addr))

    async def exec(self) -> None:
        match self.msg.name:
            case "ping":
                await self.re_msg("pong")
            case "message":
                ...
            case "photo":
                ...
            case _:
                ...
