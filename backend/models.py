from sqlalchemy import Column, Integer, String, Text
from database import Base

class Lawsuit(Base):
    __tablename__ = "lawsuits"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(Text)
    court = Column(String)
    filed_date = Column(String)
    url = Column(String)
