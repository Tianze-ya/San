import asyncio


class SanClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.running = False

    async def listen_for_messages(self, reader):
        """持续监听服务器消息"""
        while self.running:
            try:
                data = await reader.read(1024)
                if not data:
                    print("Server closed the connection")
                    break
                
                message = data.decode().strip()
                print(f"Received: {message}")
                
            except (asyncio.CancelledError, ConnectionError):
                break

    async def run(self):
        """运行客户端"""
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            self.running = True
            print(f"Connected to server at {self.host}:{self.port}")
            print("Waiting for messages from server...")
            
            # 启动消息监听任务
            listen_task = asyncio.create_task(self.listen_for_messages(reader))
            
            try:
                # 保持连接，等待用户中断或服务器断开
                await listen_task
            except KeyboardInterrupt:
                print("\nClient shutting down...")
            finally:
                self.running = False
                listen_task.cancel()
                try:
                    await listen_task
                except asyncio.CancelledError:
                    pass
                
                writer.close()
                await writer.wait_closed()
                print("Disconnected from server")
                
        except ConnectionRefusedError:
            print(f"Could not connect to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"An error occurred: {e}")


async def main():
    client = SanClient()
    await client.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass