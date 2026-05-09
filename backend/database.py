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
# LAWSUIT MODEL (FINAL V2)
# =========================================
class Lawsuit(Base):
    __tablename__ = "lawsuits"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)
    court = Column(String, index=True)

    # unified field name used everywhere
    filed_date = Column(String, index=True)

    summary = Column(Text, nullable=True)

    url = Column(String, unique=True, index=True)

    # future AI expansion fields
    category = Column(String, nullable=True)
    source = Column(String, nullable=True)
