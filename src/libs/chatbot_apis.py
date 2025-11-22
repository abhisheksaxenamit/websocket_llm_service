from openai import AuthenticationError, OpenAIError
import asyncio
from datetime import datetime
from playsound import playsound
from pathlib import Path

class ChatbotAPI():
    '''Base class for chatbot APIs.'''

    def __init__(self, client, model: str):
        '''Initialise the Chatbot with the client to openai'''
        self.client = client
        # Context defines the behaviour of the chatbot
        # There are 3 parts to communicating: system, user and assistant
        self.context = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        # this is the model for the chatbot defined by the user
        self.model = model


    async def send_message(self, message: str):
        '''Send a message to the chatbot API.'''    
        # Here the message is coming from the user
        # Appending the context with the user message
        self.context.append({"role": "user", "content": message})
        try:
            # Sending the message to the openai client
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.context
            )
            # print(f"Response received: {response.choices[0].message.content}")
            # Getting the response from the assistant
            response_content = response.choices[0].message.content

            # Appending the context with the assistant response to maintain the conversation
            self.context.append({"role": "assistant", "content": response_content})
        except AuthenticationError as e:
            print("Authentication failed. Please check your API key.")
        except OpenAIError as e:
            print("An error occurred while communicating with the OpenAI API.")
    def print_chat(self, response_text: str):
        '''Print the latest chat response.'''
        print(f"Assistant: {response_text}")
    
    def print_chat_history(self):
        '''Print the chat history.'''
        for message in self.context:
            if message['role'] == "user":
                print(f"User: {message['content']}")
            elif message['role'] == "assistant":
                print(f"Assistant: {message['content']}")