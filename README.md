# websocket_llm_service
This is the assignment for the Electronic Arts. Create service for accepting text and replying in audio using OpenAI LLMs

## Problem statement:
Build a WebSocket service that accepts text from a client, sends it to an LLM, then returns synthesized audio of the LLM’s response.

### High-Level Flow
Client → WebSocket message with text input → your service →
    1. send text to OpenAI LLM API
    2. receive text response
    3. send LLM text to OpenAI TTS API
    4. Sends audio back over WebSocket
→ Client

<img width="798" height="375" alt="image" src="https://github.com/user-attachments/assets/5f33f59e-61c8-4156-8920-2cae689e4233" />

Approach to this problem:
1. Work on the APIs provided and learn its implementation. Creating a simple HTTP client directly to the OpenAI server.
2. Create a Websocket service and check connection with different end points.
3. Building a Client to the Websocket service and check the connection to the OpenAI end point
4. Integrate the complete logic in Step1 to the Websocket service
5. Completing the Unit test cases and test the service.
6. Update the readme with the complete logic

