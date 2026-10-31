from fastapi import FastAPI
from app.database import Base, engine

# Import models before creating tables
from app.models import Company, StockPrice
from app.api.companies import router as companies_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="NEPSE Intelligence API",
    description="Stock Market Analytics and News Intelligence Platform",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(companies_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to NEPSE Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }