from dataclasses import dataclass
from typing import Literal

from sqlalchemy import Column, Integer, String
from db.database import Base


@dataclass
class ChatMessage:
    role: Literal["user", "assistant"]
    content: str


class ChatHistoryMessage(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
