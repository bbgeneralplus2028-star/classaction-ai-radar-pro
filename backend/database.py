from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# DATABASE CONFIG
# =========================
DATABASE_URL = "sqlite:///./lawsuits.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# =========================
# LAWSUIT TABLE
# =========================
class Lawsuit(Base):
    __tablename__ = "lawsuits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    court = Column(String)
    filed_date = Column(String)
    summary = Column(Text)
    url = Column(String)

# =========================
# NOTIFICATION TABLE
# =========================
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    type = Column(String)
    read_status = Column(Boolean, default=False)
    created_at = Column(String)
    lawsuit_id = Column(Integer)

# =========================
# CREATE TABLES
# =========================
Base.metadata.create_all(bind=engine)
