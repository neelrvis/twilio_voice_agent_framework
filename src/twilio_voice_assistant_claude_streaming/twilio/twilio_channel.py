from fastapi import WebSocket
from asyncio import Queue

class TwilioChannel():
    def __init__(self, queue: Queue, websocket: WebSocket):
        self.websocket = websocket
        self.queue = queue

    '''
    Poll the queue containing events continiously being streamed from llm invocation
    
    Three types of events: 
        * Text
        * Tool Use 
        * End of Turn
        * Stop 
    
    On text continue to send Twilio speak websocket messages containing content of event 

    On Tool Use stop and invoke tool, append it to Agent messages

    On End of Turn do nothing, wait for stop message to come (technically this can be skipped... but it is better to track) 

    On Stop wait for user to speak again 
    '''
    async def poll_queue(self):
        pass
        '''
        token = self.queue.get_nowait()
        await self.websocket.send_text(token)
        '''

    async def speak(self,token: str): 
        twilio_send_token = {
            "type": "text",
            "token": token,
            "last": True
        }

        await self.websocket.send_text(token)

