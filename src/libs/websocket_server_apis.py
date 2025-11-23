import asyncio
import json
import websockets
from libs.chatbot_apis import ChatbotAPI
from pathlib import Path
from openai import OpenAI

class WebSocketServerAPI:
    """Websocket server API to handle client connections."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765, config_args=None):
        """Initialise the WebSocket server."""
        self.host = host
        self.port = port
        self.config_args = config_args
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        
        async with websockets.serve(self.handle_connection, self.host, self.port, open_timeout=None):
            print(f"WebSocket server started at ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket) -> None:
        """ Handling incoming WebSocket connections."""
        print(f"Client connected to {websocket.remote_address}")

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
