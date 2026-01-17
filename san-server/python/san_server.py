import asyncio
import json
from asyncio import StreamReader, StreamWriter
from message import Message
from typing import Set
from log import Logger

logger = Logger(__file__)


class SanServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 9412) -> None:
        self.host = host
        self.port = port
        self.clients: Set[StreamWriter] = set()
        self.client_dict: dict = {}

    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        """处理客户端连接"""
        client_addr = writer.get_extra_info("peername")
        logger.info(f"New connection from {client_addr}")
        self.clients.add(writer)
        self.client_dict[client_addr] = writer

        try:
            while True:
                # 读取数据
                data = await reader.read(1024)
                if not data:
                    break

                # 处理数据
                json_data: dict = json.loads(data.decode().strip())
                message = Message(json_data, client_addr)
                logger.info(message)
                message.exec()

        except (asyncio.CancelledError, ConnectionError):
            pass
        finally:
            logger.info(f"Connection closed: {client_addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_message(self, message: str) -> None:
        """向所有客户端广播消息"""
        if not self.clients:
            logger.info("No clients connected")
            return

        message_with_newline = message + "\n"

        for client in self.clients:
            try:
                client.write(message_with_newline.encode())
                await client.drain()
            except ConnectionError:
                pass

    async def send_message(self, message: Message) -> None:
        try:
            client_addr = message.addr
            client = self.client_dict[client_addr]
            client.write(message.to_bytes())
        except KeyError:
            # 发送回错误消息
            pass

    async def get_all_addresses(self) -> list:
        """获取所有客户端地址"""
        logger.info("Getting all addresses")
        addresses = []
        for client in self.clients:
            addresses.append(client.get_extra_info("peername"))
        return addresses

    async def get_user_input(self) -> None:
        """获取用户输入"""
        loop = asyncio.get_event_loop()
        while True:
            # 在事件循环中运行同步的input函数
            message = await loop.run_in_executor(
                None, input, "Enter message to broadcast (or 'quit' to exit): "
            )

            if message.lower() == "quit":
                logger.info("Shutting down server...")
                # 关闭所有客户端连接
                for client in self.clients.copy():
                    try:
                        client.close()
                        await client.wait_closed()
                    except Exception:
                        pass
                self.clients.clear()
                return

            await self.broadcast_message(message)

    async def run(self) -> None:
        """启动服务器"""
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")

        # 启动用户输入任务
        # input_task = asyncio.create_task(self.get_user_input())

        try:
            async with server:
                await server.serve_forever()
        except asyncio.CancelledError:
            pass
        """
        finally:
            input_task.cancel()
            try:
                await input_task
            except asyncio.CancelledError:
                pass
        """


# 运行服务器
async def main() -> None:
    server = SanServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("SanServer stopped")
