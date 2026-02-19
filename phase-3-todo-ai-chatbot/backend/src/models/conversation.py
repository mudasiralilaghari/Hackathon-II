from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .task import Task

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    __table_args__ = {'extend_existing': True}

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)
    type: str = Field(regex="^(user|assistant)$")  # user or assistant
    content: str
    tool_calls: Optional[str] = None  # JSON string of tool calls
    tool_results: Optional[str] = None  # JSON string of tool results
    sequence_number: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")