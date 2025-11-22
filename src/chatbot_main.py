from openai import OpenAI
import json
from argparse import Namespace
import asyncio
from libs.chatbot_apis import ChatbotAPI
from pathlib import Path


def get_config(config_path: str) -> Namespace:
    ''' Load configuration from a JSON file and return as Namespace.'''
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
    return Namespace(**config_data)


async def main():
    ''' Main function to start the client and chatbot API.'''
    config = get_config(Path(__file__).parent / 'libs' / 'config.json')
    print(f"Loaded configuration: {config}")
    client = OpenAI(api_key=config.api_key)
    chatbot_api = ChatbotAPI(client, model=config.model)
    while True:
        message = input("You: ")
        if message.lower() in ['exit', 'quit']:
            print("Exiting chat...")
            break
        await chatbot_api.send_message(message)
    # await chatbot_api.start()


if __name__ == "__main__":
    asyncio.run(main())