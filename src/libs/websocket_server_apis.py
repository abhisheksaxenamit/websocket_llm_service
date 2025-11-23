import asyncio
import websockets
from libs.chatbot_apis import ChatbotAPI
from argparse import Namespace
from libs.common_functions import load_config_from_json
from pathlib import Path
from openai import OpenAI

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
        print(f"Client connected to {websocket.remote_address}")
        try:
            # get the server configuration
            config_path = Path(__file__).parent / 'configs' / 'server_config.json'
            self.config_args = load_config_from_json(config_path)
            
            # create OpenAI client and ChatbotAPI instance
            client = OpenAI(api_key=self.config_args.api_key)
            chatbot_api = ChatbotAPI(client, model=self.config_args.model)
            
            async for message in websocket:
                print(f"You: {message}")
                await chatbot_api.send_message(message)

        except websockets.ConnectionClosed:
            print("Client disconnected")
        except Exception as e:
            print(f"Error: {e}")
