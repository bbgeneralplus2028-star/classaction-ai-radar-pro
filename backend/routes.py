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
# AI Radar Scan (MAIN)
# -------------------------
@router.get("/scan")
def scan():
    count = run_daily_scan()

    return {
        "message": "AI Radar scan complete",
        "inserted": count,
        "status": "live_data" if count > 0 else "no_new_data_found",
        "note": "System now uses multiple legal data sources"
    }

# -------------------------
# View Stored Lawsuits
# -------------------------
@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()

    try:
        rows = db.query(Lawsuit).all()

        return [
            {
                "id": r.id,
                "title": r.title,
                "court": r.court,
                "date": r.date,
                "url": r.url
            }
            for r in rows
        ]

    finally:
        db.close()
