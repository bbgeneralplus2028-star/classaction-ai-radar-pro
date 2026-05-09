from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
