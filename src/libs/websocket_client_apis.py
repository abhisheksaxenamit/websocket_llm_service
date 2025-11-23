import asyncio
from email.mime import message
import websockets
import playsound
from pathlib import Path
import json
import vlc


class WebSocketClientAPI:
    """Websocket client API to handle client connections."""

    def __init__(self, uri: str = "ws://127.0.0.1:8765", config_args=None):
        """Initialise the WebSocket client."""
        self.uri = uri
        self.config_args = config_args
    
    async def openai_chat_bot(self):
        try:
            async with websockets.connect(self.uri, ) as websocket:
                # Perform API handshake
                handshake_request = self.create_api_handshake()
                await websocket.send(handshake_request)
                handshake_response = await websocket.recv()
                print(f"Handshake response from server: {handshake_response}")
                
                while True:
                    message = input("Client! Ask the assistant (exit to quit): ")
                    if message.lower() in ['exit', 'quit']:
                        print("Exiting...")
                        await websocket.close()
                        break
                    await websocket.send(message)
                    print(f'Client sent: {message}')

                    server_response = await websocket.recv()
                    
                    print(f"Client received: {json.loads(server_response)['text']}")
                    playsound.playsound(json.loads(server_response)['audio'])
                    # player = vlc.MediaPlayer(json.loads(server_response)['audio'])
                    # player.play()
        except websockets.ConnectionClosed:
            print("Connection closed by the server.")
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("Client interrupted and exiting.")
            await websocket.close()
            # playsound.playsound(None)

    def create_api_handshake(self):
        """ Create JSON data for communication."""
        data = {
            "api_key": self.config_args.api_key
        }
        return json.dumps(data)