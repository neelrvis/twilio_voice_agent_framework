from asyncio import Queue


class TokenBuffer(): 
    def __init__(self):
        self.queue = Queue()

    async def put_token(self,token: str): 
        self.queue.put_nowait(token)
        pass 

    async def get_token(self): 
        token = self.queue.get_nowait()
        return token 


