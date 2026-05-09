from fastapi import APIRouter
from database import SessionLocal, Lawsuit
from scanner import run_daily_scan

router = APIRouter()

@router.get("/scan")
def scan():
    run_daily_scan()
    return {"message": "scan complete"}

@router.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()
    return db.query(Lawsuit).all()
