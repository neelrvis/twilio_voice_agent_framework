from enum import Enum

class MessageType(Enum): 
    TEXT = "text"
    TOOL_USE = "tool_use"
    END = "end"

class Message(): 
    def __init__(self, content: str, type: MessageType):
        self.content = content
