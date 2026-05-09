from fastapi import APIRouter
from backend.database import SessionLocal, Lawsuit
from backend.scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    count = run_daily_scan()
    return {
        "message": "scan complete",
        "inserted": count
    }

@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()
    return db.query(Lawsuit).all()

@router.get("/health")
def health():
    return {"status": "ok"}
