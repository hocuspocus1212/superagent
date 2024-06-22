from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    print("apps>memory>message.py>MessageType","line 7")
    HUMAN = "human"
    AI = "ai"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class BaseMessage(BaseModel):
    type: MessageType
    content: str
