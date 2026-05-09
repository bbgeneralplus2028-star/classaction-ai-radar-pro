from fastapi import FastAPI
from backend.routes import router
from apscheduler.schedulers.background import BackgroundScheduler
from backend.scanner import run_daily_scan

app = FastAPI(title="ClassAction AI Radar Pro")

app.include_router(router)

# ----------------------------
# AUTO DAILY SCAN (every 6 hours)
# ----------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(run_daily_scan, "interval", hours=6)
scheduler.start()

@app.get("/")
def home():
    return {"status": "AI Radar Pro running"}
