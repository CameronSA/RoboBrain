from typing import List
from db.models import ChatHistoryMessage, ChatMessage
import db.database as database
from sqlalchemy.exc import SQLAlchemyError


class ChatHistoryRepository:

    def __init__(self):
        self.__session = database.Session()

    def AddChatHistory(self, messages: List[ChatMessage]):
        db_messages = [
            ChatHistoryMessage(role=message.role, content=message.content)
            for message in messages
        ]

        try:
            with self.__session.begin():
                self.__session.add_all(db_messages)
        except SQLAlchemyError as e:
            print(f"Failed to add chat history: {e}", e)

    def GetChatHistory(self) -> List[ChatMessage]:
        chat_history = self.__session.query(
            ChatHistoryMessage.role, ChatHistoryMessage.content
        ).all()

        return [ChatMessage(role=r.role, content=r.content) for r in chat_history]
