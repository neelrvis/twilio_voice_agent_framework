from .utils.streaming import LLMStreamBuffer
from .utils.buffer import TokenBuffer

'''
TwilioConversationalRelayHandler -> (MediaStream) -> Agent 

'''

class Agent(): 
    def __init__(self,invoke_llm_stream_buffer : LLMStreamBuffer):
        self.invoke_llm_client = invoke_llm_stream_buffer
        self.messages = []

    def append_message(self,message: list): 
        self.messages.append(message)

    async def invoke(self,user_prompt: str): 

        await self.invoke_llm_client.claude_api_stream(user_prompt)

        pass 




