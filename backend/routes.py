from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

@router.get("/scan")
def scan():
    count = run_daily_scan()

    return {
        "message": "scan complete",
        "inserted": count,
        "status": "success" if count > 0 else "no_new_data"
    }

@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()
    try:
        results = db.query(Lawsuit).all()

        return [
            {
                "id": l.id,
                "title": l.title,
                "court": l.court,
                "date": l.date,
                "url": l.url
            }
            for l in results
        ]
    finally:
        db.close()

@router.get("/health")
def health():
    return {"status": "ok"}
