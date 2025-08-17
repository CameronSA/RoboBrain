from db.database import Base, Engine
from db.models import ChatHistoryMessage, ChatMessage

Base.metadata.create_all(Engine)
