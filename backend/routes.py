from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

# =========================================
# HEALTH
# =========================================
@router.get("/health")
def health():
    return {"status": "ok"}

# =========================================
# SCAN (MAIN)
# =========================================
@router.get("/scan")
def scan():

    count = run_daily_scan()

    db = SessionLocal()

    try:
        stored = db.query(Lawsuit).order_by(Lawsuit.id.desc()).limit(10).all()

        results = [
            {
                "id": x.id,
                "title": x.title,
                "court": x.court,
                "filed_date": x.filed_date,
                "summary": x.summary,
                "url": x.url,
                "category": x.category,
                "source": x.source
            }
            for x in stored
        ]

        return {
            "message": "AI Radar scan complete",
            "inserted": count,
            "status": "live_data" if count > 0 else "fallback_loaded",
            "results": results
        }

    finally:
        db.close()

# =========================================
# VIEW ALL
# =========================================
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
                "filed_date": r.filed_date,
                "summary": r.summary,
                "url": r.url,
                "category": r.category,
                "source": r.source
            }
            for r in rows
        ]

    finally:
        db.close()

# =========================================
# DEBUG
# =========================================
@router.get("/debug-scan")
def debug_scan():

    db = SessionLocal()

    try:
        rows = db.query(Lawsuit).limit(5).all()

        return {
            "database_connected": True,
            "stored_records": len(rows),
            "sample_data": [
                {
                    "id": x.id,
                    "title": x.title,
                    "court": x.court,
                    "filed_date": x.filed_date,
                    "url": x.url
                }
                for x in rows
            ]
        }

    finally:
        db.close()
