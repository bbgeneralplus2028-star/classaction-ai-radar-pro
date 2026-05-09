from fastapi import FastAPI
from backend.routes import router
from backend.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClassAction AI Radar Pro")

# Attach routes
app.include_router(router)

@app.get("/")
def home():
    return {"status": "AI Radar Pro running"}

@app.get("/health")
def health():
    return {"status": "ok"}
