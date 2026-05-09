from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

# =========================================
# HEALTH CHECK
# =========================================
@router.get("/health")
def health():
    return {"status": "ok"}

# =========================================
# NORMAL SCAN (AUTO)
# =========================================
@router.get("/scan")
def scan():

    count = run_daily_scan()

    db = SessionLocal()

    try:
        rows = db.query(Lawsuit).order_by(Lawsuit.id.desc()).limit(10).all()

        return {
            "message": "AI Radar scan complete",
            "inserted": count,
            "status": "live_data" if count > 0 else "fallback_loaded",
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "court": r.court,
                    "filed_date": r.filed_date,
                    "url": r.url
                }
                for r in rows
            ]
        }

    finally:
        db.close()

# =========================================
# 🔥 MANUAL BUTTON (FORCE SCAN)
# =========================================
@router.get("/manual-scan")
def manual_scan():

    count = run_daily_scan()

    db = SessionLocal()

    try:
        rows = db.query(Lawsuit).order_by(Lawsuit.id.desc()).limit(10).all()

        return {
            "message": "MANUAL scan executed",
            "inserted": count,
            "status": "manual_triggered",
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "court": r.court,
                    "filed_date": r.filed_date,
                    "url": r.url
                }
                for r in rows
            ]
        }

    finally:
        db.close()

# =========================================
# VIEW DATABASE
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
                "url": r.url
            }
            for r in rows
        ]

    finally:
        db.close()

# =========================================
# DEBUG (FIXED)
# =========================================
@router.get("/debug-scan")
def debug_scan():

    db = SessionLocal()

    try:
        rows = db.query(Lawsuit).all()

        return {
            "database_connected": True,
            "stored_records": len(rows),
            "sample_data": [
                {
                    "id": r.id,
                    "title": r.title,
                    "court": r.court,
                    "filed_date": r.filed_date,
                    "url": r.url
                }
                for r in rows[:5]
            ]
        }

    except Exception as e:

        return {
            "database_connected": False,
            "error": str(e)
        }

    finally:
        db.close()
