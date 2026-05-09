from fastapi import FastAPI
from backend.routes import router
from backend.database import Base, engine

# create tables ONLY (no drop_all in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Radar Pro V3")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "AI Radar Pro running"}
