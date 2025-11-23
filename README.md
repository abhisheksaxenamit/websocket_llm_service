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
1. Work on the APIs provided and learn its implementation. Creating a simple HTTP client directly to the OpenAI server. **(Done)**
2. Create a Websocket service and check connection with different end points. **(Done)**
3. Building a Client to the Websocket service and check the connection to the OpenAI end point **(Done)**
4. Integrate the complete logic in Step1 to the Websocket service **(Done)**
5. Completing the Unit test cases and test the service. **(Done locally thru scripts out of time to write using pytest)** 
6. Update the readme with the complete logic **(Done)**

### How to run the code
There are 2 main function in this code, for **Server**(websocket_server_apis.py) and **Client**(websocket_client_main.py)
The configs for the server and client can be foud in the `libs -> config` where the user can add the api key on the client side.

└── websocket_llm_service
    ├── README.md
    ├── requirement.txt
    └── src
        ├── audio
        ├── libs
        │   ├── audio
        │   ├── chatbot_apis.py
        │   ├── common_functions.py
        │   ├── configs
        │   │   ├── client_config.json
        │   │   └── server_config.json
        │   ├── __init__.py
        │   ├── websocket_client_apis.py
        │   └── websocket_server_apis.py
        ├── websocket_client_main.py
        └── websocket_server_main.py

### Starting the code
- Add the api key to the file `src->libs->config->client_config.json` at `"api_key": "your-client-api-key-here"`
- **Terminal 1** - Start the Server side: `/websocket_llm_service$ python src/websocket_server_main.py`
- **Terminal 2** - Start the client side: `/websocket_llm_service$ python src/websocket_client_main.py`
- User input on the Terminal 2 to interact with the webserver -> OpenAI models
Please note there is a ping_timeout of 60 secs.

### Installation
To install the environment use the `requirement.txt` file using command `pipenv install -r requirements.txt`

### Flow of code
The architecture of the code is as follows:

- `websocket_server_main.py ` instantiates object of class `WebSocketServerAPI` with config params in `server_config.json` 
- We start the server using `start()`
- `websocket_client_main.py`  instantiates object of class `WebSocketClientAPI` with config params in `client_config.json`
- Than the client API connects to the server and initiates a handshake in function `do_api_handshake`. This is to share the api_key needed for communicating to the OpenAI Server.
- After handshake is successful we create the Open AI client.
- Now User can input the query in the Client terminal window as a text message.
- This is sent as a message to the `WebSocketServerAPI->handle_connection` that is waiting to receive message form the client.
- This message is forwarded to the `ChatbotAPI` class function `send_message` where it is forwarded to the OpenAI text model defined in the `server_config.json`
- After the response is gathered from the OpenAI we forward the message to the audio generation model.
- We then return the reply of the text and the audio path to the Client
- Client than shows the reply and plays the text message.




