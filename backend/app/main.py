from fastapi import FastAPI
from app.database import Base, engine

# Import models before creating tables
from app.models import Company, StockPrice, CrawlRun
from app.api.companies import router as companies_router
from app.api.auth import router as auth_router
from app.api.news import router as news_router
from app.api.analytics import router as analytics_router
from app.api.admin import router as admin_router
from app.api.websocket import router as websocket_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.stock_prices import router as stock_prices_router

app = FastAPI(
    title="NEPSE Intelligence API",
    description="Stock Market Analytics and News Intelligence Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(companies_router)
app.include_router(auth_router)
app.include_router(news_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(websocket_router)
app.include_router(stock_prices_router, prefix="/api")

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