from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Engine = create_engine("sqlite:///robobrain.db", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=Engine)
