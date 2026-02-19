from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import sys
import os

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.conversation import Conversation, Message
from database import engine

class ConversationService:
    """Service for managing conversations and message history."""

    @staticmethod
    def create_conversation(user_id: str) -> Conversation:
        """Create a new conversation for the user."""
        with Session(engine) as session:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        with Session(engine) as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = session.exec(statement).first()
        return result

    @staticmethod
    def get_conversation_history(conversation_id: str, limit: int = 100, offset: int = 0) -> List[Message]:
        """Get conversation history ordered by sequence number with pagination."""
        with Session(engine) as session:
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.sequence_number).offset(offset)
            if limit:
                statement = statement.limit(limit)
            results = session.exec(statement).all()
        return results

    @staticmethod
    def update_last_activity(conversation_id: str) -> None:
        """Update last activity timestamp for conversation."""
        with Session(engine) as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            conversation = session.exec(statement).first()
            if conversation:
                conversation.last_activity = datetime.utcnow()
                session.add(conversation)
                session.commit()

    @staticmethod
    def get_user_conversations(user_id: str, limit: int = 10, offset: int = 0) -> List[Conversation]:
        """Get all conversations for a user with pagination."""
        with Session(engine) as session:
            statement = select(Conversation).where(
                Conversation.user_id == user_id
            ).order_by(Conversation.last_activity.desc()).offset(offset)
            if limit:
                statement = statement.limit(limit)
            results = session.exec(statement).all()
        return results

    @staticmethod
    def get_recent_conversation(user_id: str) -> Optional[Conversation]:
        """Get the most recent conversation for a user."""
        with Session(engine) as session:
            statement = select(Conversation).where(
                Conversation.user_id == user_id
            ).order_by(Conversation.last_activity.desc()).limit(1)
            result = session.exec(statement).first()
        return result