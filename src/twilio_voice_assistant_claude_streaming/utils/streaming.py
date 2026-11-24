from anthropic import AsyncAnthropic
from asyncio import Queue
from .constants import MAX_TOKENS,CLAUDE_HAIKU_MODEL
from .message import Message, MessageType

class LLMStreamBuffer(): 

    def __init__(self,queue: Queue, client: AsyncAnthropic):
        self.queue = queue
        self.client = client

    async def claude_api_stream(self,system_prompt: str, user_prompt: str, messages: list, tools: list): 
        response_accumulator = ""

        messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )
        async with self.client.messages.stream(
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages,
            tools=tools,
            model=CLAUDE_HAIKU_MODEL
        ) as stream: 
            async for event in stream: 
                if event.type == "content_block_start": 
                    if event.content_block_start == "text": 
                        response_accumulator+=event.content_block.text
                        self.queue.put_nowait()
                    elif event.content_block_start == "tool_use": 
                        pass
                elif event.type == "content_block_delta": 
                    pass 
                elif event.type ==  "content_block_stop": 
                    pass
                elif event.type == "message_delta": 
                    pass 
                elif event.type == "message_stop": 
                    pass 

                pass

        return response_accumulator
    '''
    async def claude_api_stream(self,system_prompt: str, user_prompt: str, messages: list, tools: list): 

        
        response_accumulator = ""

        async with self.client.messages.stream(
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages,
            tools = tools,
            model=CLAUDE_HAIKU_MODEL,
         ) as stream: 
            async for event in stream:  
                if event["type"] == "content_block_start": 
                    if event.content_block.type == "text": 

                        response_accumulator+=event.content_block.text
                        self.token_buffer.put_token(event.content_block.text)

                    elif event.content_block.type == "tool_use": 
                        pass
                if event["type"] == "content_block_delta": 
                    if event.delta.type == "text_delta":

                        self.token_buffer.put_token(event.delta.text)
                elif event["type"] == "content_block_delta": 
                    pass
                #response_accumulator.append(token)
                #self.token_buffer.put_token(token)

        return response_accumulator
    '''