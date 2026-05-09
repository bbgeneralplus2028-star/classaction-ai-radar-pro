from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    message = Column(Text)
    type = Column(String)
    read_status = Column(Boolean, default=False)
    created_at = Column(String)
    lawsuit_id = Column(Integer)
DATABASE_URL = "sqlite:///./lawsuits.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Lawsuit(Base):
    __tablename__ = "lawsuits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    court = Column(String)
    filed_date = Column(String)
    summary = Column(Text)
    url = Column(String)

Base.metadata.create_all(bind=engine)
