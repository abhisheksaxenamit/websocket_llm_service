import asyncio
from libs.websocket_server_apis import WebSocketServerAPI


async def main():
    server = WebSocketServerAPI()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())