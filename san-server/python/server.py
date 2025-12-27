import asyncio
from log import Logger

logger = Logger()

class SanServer:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.clients = set()

    async def handle_client(self, reader, writer):
        """处理客户端连接"""
        client_addr = writer.get_extra_info("peername")
        logger.info(f"New connection from {client_addr}")
        self.clients.add(writer)

        try:
            while True:
                # 读取数据
                data = await reader.read(1024)
                if not data:
                    break

                # 处理数据
                message = data.decode().strip()
                logger.info(f"Received from {client_addr}: {message}")

        except (asyncio.CancelledError, ConnectionError):
            pass
        finally:
            logger.info(f"Connection closed: {client_addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_message(self, message):
        """向所有客户端广播消息"""
        if not self.clients:
            logger.info("No clients connected")
            return
        
        message_with_newline = message + "\n"
        disconnected_clients = set()
        
        for client in self.clients:
            try:
                client.write(message_with_newline.encode())
                await client.drain()
            except ConnectionError:
                disconnected_clients.add(client)
        
        # 移除断开连接的客户端
        for client in disconnected_clients:
            self.clients.remove(client)
            try:
                client.close()
                await client.wait_closed()
            except:
                pass

    async def get_user_input(self):
        """获取用户输入"""
        loop = asyncio.get_event_loop()
        while True:
            # 在事件循环中运行同步的input函数
            message = await loop.run_in_executor(None, input, "Enter message to broadcast (or 'quit' to exit): ")
            
            if message.lower() == 'quit':
                logger.info("Shutting down server...")
                # 关闭所有客户端连接
                for client in self.clients.copy():
                    try:
                        client.close()
                        await client.wait_closed()
                    except:
                        pass
                self.clients.clear()
                return
            
            await self.broadcast_message(message)

    async def run(self):
        """启动服务器"""
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")
        logger.info("Type messages to broadcast to all clients. Type 'quit' to exit.")

        # 启动用户输入任务
        input_task = asyncio.create_task(self.get_user_input())
        
        try:
            async with server:
                await server.serve_forever()
        except asyncio.CancelledError:
            pass
        finally:
            input_task.cancel()
            try:
                await input_task
            except asyncio.CancelledError:
                pass


# 运行服务器
async def main():
    server = SanServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Server stopped")
