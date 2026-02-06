from message import BaseMsg
from server_message import ServerMessage
from client_message import ClientMessage
from tools import get_token


def get_msg(data: BaseMsg, addr: str, server) -> ServerMessage | ClientMessage:
    token = get_token()
    if data["token"] == token:
        return ServerMessage(data, addr, server)
    else:
        return ClientMessage(data, addr, server)
