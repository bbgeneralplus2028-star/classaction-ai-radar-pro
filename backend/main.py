from fastapi import FastAPI
from backend.routes import router
from backend.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClassAction AI Radar Pro")

# Load routes
app.include_router(router)

# Home route
@app.get("/")
def home():
    return {
        "status": "AI Radar Pro running"
    }
