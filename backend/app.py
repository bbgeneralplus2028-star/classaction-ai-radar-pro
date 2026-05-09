from fastapi import FastAPI
from database import SessionLocal, Lawsuit
from scanner import run_daily_scan

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ClassAction AI Radar Pro running"}

@app.get("/scan")
def scan_now():
    run_daily_scan()
    return {"message": "Scan completed"}

@app.get("/lawsuits")
def get_lawsuits():
    db = SessionLocal()
    return db.query(Lawsuit).all()
