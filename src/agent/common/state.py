from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class BaseState(BaseModel):
    session_id: str
    messages: Annotated[list[AnyMessage], add_messages]
