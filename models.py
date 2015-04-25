from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///pastes.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Paste(Base):
    __tablename__ = 'pastes'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    paste_id = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=True, unique=True)

    content = relationship("Content", backref="content_output")


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    paste_body = Column(String)

    paste_fk = Column(Integer, ForeignKey('pastes.id'), nullable=False)

Base.metadata.create_all(engine)
