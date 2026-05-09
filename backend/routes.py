from fastapi import APIRouter
from backend.scanner import run_daily_scan
from backend.database import SessionLocal, Lawsuit

router = APIRouter()

# =========================================
# HEALTH CHECK
# =========================================
@router.get("/health")
def health():
    return {
        "status": "ok"
    }

# =========================================
# MAIN AI RADAR SCAN
# =========================================
@router.get("/scan")
def scan():

    # Run live scan
    count = run_daily_scan()

    db = SessionLocal()

    try:
        # Pull latest stored lawsuits for fallback/testing
        stored_cases = (
            db.query(Lawsuit)
            .order_by(Lawsuit.id.desc())
            .limit(10)
            .all()
        )

        results = []

        for case in stored_cases:
            results.append({
                "id": case.id,
                "title": case.title,
                "court": case.court,
                "date": case.date,
                "url": case.url
            })

        return {
            "message": "AI Radar scan complete",
            "inserted": count,

            # If new data inserted show live_data
            # otherwise fallback_loaded
            "status": (
                "live_data"
                if count > 0
                else "fallback_loaded"
            ),

            # Always return something if DB has records
            "results": results,

            "note": (
                "New lawsuits inserted successfully"
                if count > 0
                else "No new lawsuits found - returning stored database results"
            )
        }

    except Exception as e:

        return {
            "message": "scan failed",
            "error": str(e)
        }

    finally:
        db.close()

# =========================================
# VIEW ALL STORED LAWSUITS
# =========================================
@router.get("/lawsuits")
def get_lawsuits():

    db = SessionLocal()

    try:
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

        return results

    except Exception as e:

        return {
            "message": "failed to load lawsuits",
            "error": str(e)
        }

    finally:
        db.close()

# =========================================
# DEBUG ROUTE
# =========================================
@router.get("/debug-scan")
def debug_scan():

    db = SessionLocal()

    try:
        lawsuits = db.query(Lawsuit).limit(5).all()

        return {
            "database_connected": True,
            "stored_records": len(lawsuits),
            "sample_data": [
                {
                    "id": x.id,
                    "title": x.title,
                    "court": x.court,
                    "date": x.date,
                    "url": x.url
                }
                for x in lawsuits
            ]
        }

    except Exception as e:

        return {
            "database_connected": False,
            "error": str(e)
        }

    finally:
        db.close()
