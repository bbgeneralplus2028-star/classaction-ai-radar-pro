from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

# -------------------------
# Health Check
# -------------------------
@router.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Manual Scan Endpoint
# -------------------------
@router.get("/scan")
def scan():
    count = run_daily_scan()

    return {
        "message": "scan complete",
        "inserted": count,
        "status": "live_data" if count > 0 else "no_new_data_found"
    }

# -------------------------
# Get Stored Lawsuits
# -------------------------
@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()

    try:
        lawsuits = db.query(Lawsuit).all()

        return [
            {
                "id": l.id,
                "title": l.title,
                "court": l.court,
                "date": l.date,
                "url": l.url
            }
            for l in lawsuits
        ]

    finally:
        db.close()
