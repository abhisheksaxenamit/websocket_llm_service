import asyncio
import json
import websockets
from libs.chatbot_apis import ChatbotAPI
from pathlib import Path
from openai import OpenAI
from libs.common_functions import log_message

class WebSocketServerAPI:
    """Websocket server API to handle client connections."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765, config_args=None):
        """Initialise the WebSocket server."""
        log_message("Server", f"Initializing WebSocket server at {host}:{port}")
        self.host = host
        self.port = port
        self.config_args = config_args
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        try:
            async with websockets.serve(self.handle_connection, self.host, self.port, open_timeout=None, ping_timeout=60):
                log_message("Server", f"WebSocket server started at ws://{self.host}:{self.port}")
                print(f"WebSocket server started at ws://{self.host}:{self.port}")
                await asyncio.Future()  # Run forever
        except Exception as e:
            log_message("Server", f"Failed to start WebSocket server: {self.host}:{self.port} - {e}", level='error')
            print(f"Failed to start WebSocket server: {self.host}:{self.port}")
        
    async def do_api_handshake(self, websocket) -> str:
        """ Perform API handshake to get api_key from client."""
        raw_handshake = await websocket.recv()
        try:
            log_message("Server", f"Received handshake: {raw_handshake}")
            handshake = json.loads(raw_handshake)
            self.client_api_key = handshake.get("api_key")
            if not self.client_api_key:
                await websocket.send(json.dumps({"error": "missing api_key in handshake"}))
                await websocket.close(code=4000, reason="Missing api_key")
                return

            # Acknowledge successful handshake
            await websocket.send(json.dumps({"status": "handshake_ok"}))
        except json.JSONDecodeError:
            log_message("Server", "Invalid handshake JSON received", level='error')
            await websocket.send(json.dumps({"error": "invalid handshake JSON"}))
            await websocket.close(code=4001, reason="Invalid JSON")
            return
    
    async def handle_connection(self, websocket) -> None:
        """ Handling incoming WebSocket connections."""
        print(f"Client connected to {websocket.remote_address}")
        log_message("Server", f"Client connected to {websocket.remote_address}")
        await self.do_api_handshake(websocket)

        try:                
            # Create OpenAI client and ChatbotAPI for this connection
            client = OpenAI(api_key=self.client_api_key)
            chatbot_api = ChatbotAPI(client, model_text=self.config_args.model_text, model_audio=self.config_args.model_audio)

            async for message in websocket:
                print(f"You: {message}")
                server_response = await chatbot_api.send_message(message)
                await websocket.send(json.dumps(server_response))

        except websockets.ConnectionClosed:
            print(f"Client disconnected: {websocket.remote_address}")
        except Exception as e:
            print(f"Error: {e}")
