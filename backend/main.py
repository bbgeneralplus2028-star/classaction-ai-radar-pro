from fastapi import FastAPI
from routes import router

app = FastAPI(title="ClassAction AI Radar Pro")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "AI Radar Pro running"}
