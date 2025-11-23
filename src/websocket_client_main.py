import asyncio
from libs.websocket_client_apis import WebSocketClientAPI
from libs.common_functions import load_config_from_json
from pathlib import Path

async def main():
    # get the server configuration
    config_path = Path(__file__).parent / 'libs' / 'configs' / 'client_config.json'
    config_args = load_config_from_json(config_path)
    client = WebSocketClientAPI(uri=config_args.uri, config_args=config_args)
    await client.openai_chat_bot()

if __name__ == "__main__":
    asyncio.run(main())