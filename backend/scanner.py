from fastapi import APIRouter
from backend.scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    try:
        count = run_daily_scan()
        return {"message": "scan complete", "inserted": count}
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }
