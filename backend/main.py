from fastapi import FastAPI
from backend.routes import router
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClassAction AI Radar Pro")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "AI Radar Pro running"}
