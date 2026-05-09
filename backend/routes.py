from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit
from fastapi import APIRouter
from backend.scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    inserted = run_daily_scan()
    return {"message": "scan complete", "inserted": inserted}
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/scan")
def scan():
    count = run_daily_scan()
    return {
        "message": "scan complete",
        "inserted": count
    }

@router.get("/lawsuits")
def lawsuits():
    db = SessionLocal()

    results = db.query(Lawsuit).all()

    data = []

    for item in results:
        data.append({
            "id": item.id,
            "title": item.title,
            "court": item.court,
            "date": item.date,
            "url": item.url
        })

    db.close()

    return data
