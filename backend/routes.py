from fastapi import APIRouter
from backend.scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    inserted = run_daily_scan()
    return {"message": "scan complete", "inserted": inserted}
