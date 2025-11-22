from openai import AuthenticationError, OpenAIError
import asyncio
from datetime import datetime
from playsound import playsound
from pathlib import Path


class ChatbotAPI:
    """Base class for chatbot APIs."""

    def __init__(self, client, model: str):
        """Initialise the Chatbot with the client to openai"""
        self.client = client
        # Context defines the behaviour of the chatbot
        # There are 3 parts to communicating: system, user and assistant
        self.context = [{"role": "system", "content": "You are a helpful assistant."}]
        # this is the model for the chatbot defined by the user
        self.model = model

    async def send_message(self, message: str):
        """Send a message to the chatbot API."""
        # Here the message is coming from the user
        # Appending the context with the user message
        self.context.append({"role": "user", "content": message})
        try:
            # Sending the message to the openai client
            response = self.client.chat.completions.create(
                model=self.model, messages=self.context
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
        task1 = asyncio.create_task(
            asyncio.to_thread(self.speak_response, response_content)
        )
        task2 = asyncio.create_task(
            asyncio.to_thread(self.print_chat, response_content)
        )
        await task1
        await task2

    def print_chat(self, response_text: str):
        """Print the latest chat response."""
        print(f"Assistant: {response_text}")

    def print_chat_history(self):
        """Print the chat history."""
        for message in self.context:
            if message["role"] == "user":
                print(f"User: {message['content']}")
            elif message["role"] == "assistant":
                print(f"Assistant: {message['content']}")

    def speak_response(self, response_text: str):
        """Convert text response to speech and play it."""
        # This is a placeholder for TTS implementationq
        # You can integrate any TTS library here
        speech_file = (
            Path(__file__).parent
            / "audio"
            / f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        )
        # ensure the audio directory exists
        speech_file.parent.mkdir(parents=True, exist_ok=True)
        response = self.client.audio.speech.create(
            model="tts-1-hd", voice="echo", input=response_text
        )
        response.stream_to_file(speech_file)
        playsound(speech_file)
