from fastapi import APIRouter
from backend.scanner import run_daily_scan

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
