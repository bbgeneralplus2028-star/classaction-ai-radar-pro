from fastapi import APIRouter
from backend.database import SessionLocal, Lawsuit
from backend.scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    return run_daily_scan()

@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()
    data = db.query(Lawsuit).all()
    db.close()

    return [
        {
            "id": l.id,
            "title": l.title,
            "court": l.court,
            "filed_date": l.filed_date,
            "summary": l.summary,
            "url": l.url
        }
        for l in data
    ]
