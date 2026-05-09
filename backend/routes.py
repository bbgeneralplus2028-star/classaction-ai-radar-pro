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
# MAIN SCAN (PRODUCTION)
# -------------------------
@router.get("/scan")
def scan():
    count = run_daily_scan()

    return {
        "message": "AI Radar scan complete",
        "inserted": count,
        "status": "live_data" if count > 0 else "no_new_data_found",
        "note": "System uses multi-source legal ingestion"
    }

# -------------------------
# VIEW DATABASE
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

# -------------------------
# DEBUG TEST ENDPOINT (SAFE)
# -------------------------
@router.get("/debug-scan")
def debug_scan():
    from backend.scanner import run_daily_scan
    return {
        "debug_inserted": run_daily_scan(),
        "note": "debug only - remove in production if desired"
    }
