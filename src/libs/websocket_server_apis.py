import asyncio

import websockets


class WebSocketServerAPI:
    """Websocket server API to handle client connections."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        """Initialise the WebSocket server."""
        self.host = host
        self.port = port
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        async with websockets.serve(self.handle_connection, self.host, self.port):
            print(f"WebSocket server started at ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket) -> None:
        """ Handling incoming WebSocket connections."""
        print(f"Client connected {websocket.remote_address}")
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                response = f"Echo: {message}"
                await websocket.send(response)
                print(f"Sent response: {response}")
        except websockets.ConnectionClosed:
            print("Client disconnected")
    