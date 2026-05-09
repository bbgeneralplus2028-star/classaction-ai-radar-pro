from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

# Health check
@router.get("/health")
def health():
    return {
        "status": "ok"
    }

# Manual lawsuit scan
@router.get("/scan")
def scan():
    count = run_daily_scan()

    return {
        "message": "scan complete",
        "inserted": count
    }

# View lawsuits dashboard data
@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()

    lawsuits = db.query(Lawsuit).all()

    results = []

    for lawsuit in lawsuits:
        results.append({
            "id": lawsuit.id,
            "title": lawsuit.title,
            "court": lawsuit.court,
            "date": lawsuit.date,
            "url": lawsuit.url
        })

    db.close()

    return results
