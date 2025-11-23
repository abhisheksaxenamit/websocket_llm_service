import asyncio
from libs.websocket_server_apis import WebSocketServerAPI
from libs.common_functions import load_config_from_json
from pathlib import Path

async def main():
    # get the server configuration
    config_path = Path(__file__).parent / 'libs' / 'configs' / 'server_config.json'
    config_args = load_config_from_json(config_path)
    print(f"Loaded server configuration: {config_args.server_host}:{config_args.server_port }")
    try:
        server = WebSocketServerAPI(host=config_args.server_host, port=config_args.server_port, config_args=config_args)
        await server.start()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    asyncio.run(main())