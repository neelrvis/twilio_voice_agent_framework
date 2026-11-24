import json
from anthropic import AsyncAnthropic
from asyncio import create_task,Queue
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from fastmcp import Client
from .twilio.twilio_channel import TwilioChannel
from .utils.constants import WELCOME_GREETING
from .utils.streaming import LLMStreamBuffer
from .agent import Agent
import os


NGROK_URL = os.environ("NGROK_URL","")

@asynccontextmanager
async def lifespan(app: FastAPI): 
    #mcp_client = Client("http://localhost:8080/")
    anthropic_client = AsyncAnthropic()

    async with anthropic_client: 
        app.state.anthropic_client = anthropic_client
        print("Anthropic Client connected")
        yield
    '''
    async with mcp_client: 
        app.state.mcp = mcp_client
        app.state.anthropic_client = anthropic_client
        yield 
    '''

    #print("MCP disconnected")
    print("Anthropic Client disconnected")

app = FastAPI(lifespan=lifespan)

@app.api_route("/twiml", methods=["GET", "POST"])
async def twiml(request: Request): 
    ws_url = f"wss//{NGROK_URL}/ws"
    twiml_response = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response> 
        <Connect>
            <ConversationalRelay url="{ws_url}" welcomeGreeting="{WELCOME_GREETING}" />
        </Connect>
    </Response>

    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept()

    #mcp = websocket.app.state.mcp
    anthropic_client = websocket.app.state.anthropic_client
    llm_response_stream_queue = Queue()
    llm_stream_buffer = LLMStreamBuffer(llm_response_stream_queue,anthropic_client)
    twilio_channel = TwilioChannel(llm_response_stream_queue,websocket)
    create_task(twilio_channel.poll_queue())
    agent = Agent(llm_stream_buffer)

    while True: 
        raw_message = await websocket.receive_text()
        parsed_message = json.loads(raw_message)
        message_type = parsed_message.get("type")

        if message_type == "setup": 
            pass 

        elif message_type == "prompt": 
            agent.invoke()
            pass

        elif message_type == "interrupt": 
            pass

        else: 
            pass
    pass











