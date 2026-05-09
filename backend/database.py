from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./lawsuits.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# =========================================
# LAWSUIT MODEL (AI RADAR V2)
# =========================================
class Lawsuit(Base):
    __tablename__ = "lawsuits"

    id = Column(Integer, primary_key=True, index=True)

    # Core fields
    title = Column(String, index=True)
    court = Column(String, index=True)

    # FIXED FIELD (consistent naming across system)
    filed_date = Column(String, index=True)

    # AI-ready expansion fields
    summary = Column(Text, nullable=True)
    url = Column(String, unique=True, index=True)

    # Optional future AI classification fields
    category = Column(String, nullable=True)   # credit, banking, debt, etc.
    source = Column(String, nullable=True)     # courtlistener, cfpb, news
