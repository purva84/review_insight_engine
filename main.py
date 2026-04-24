# main.py
from fastapi import FastAPI
from app.api.routes import business, reviews
from app.db.mongo import ping

app = FastAPI(
    title="Review Insight Engine",
    description="Context-aware customer review analysis API",
    version="1.0.0"
)

# Connect to MongoDB on startup
@app.on_event("startup")
def startup():
    ping()

# Register routes
app.include_router(business.router)
app.include_router(reviews.router)

@app.get("/")
def root():
    return {
        "app":     "Review Insight Engine",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}