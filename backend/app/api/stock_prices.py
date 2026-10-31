
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_user, require_roles
from app.crawlers.stock_price_crawler import StockPriceCrawler
from app.crawlers.stock_price_provider import StockPriceProvider


router = APIRouter(
    prefix="/stock-prices",
    tags=["Stock Prices"]
)


def get_stock_price_provider() -> StockPriceProvider:
    """
    Replace this dependency with your configured,
    authorized NEPSE data provider.
    """
    raise HTTPException(
        status_code=503,
        detail="Stock price provider has not been configured."
    )


@router.post("/crawl")
def crawl_stock_prices(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
    provider: StockPriceProvider = Depends(get_stock_price_provider)
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date."
        )

    crawler = StockPriceCrawler(
        db=db,
        provider=provider
    )

    try:
        return crawler.crawl_all(
            start_date=start_date,
            end_date=end_date
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/")
def get_stock_prices(
    company_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.stock_price import StockPrice

    query = db.query(StockPrice)

    if company_id is not None:
        query = query.filter(
            StockPrice.company_id == company_id
        )

    if start_date:
        query = query.filter(
            StockPrice.date >= start_date
        )

    if end_date:
        query = query.filter(
            StockPrice.date <= end_date
        )

    records = query.order_by(
        StockPrice.date.desc()
    ).all()

    return [
        {
            "id": record.id,
            "company_id": record.company_id,
            "date": record.date,
            "open": record.open,
            "high": record.high,
            "low": record.low,
            "close": record.close,
            "volume": record.volume
        }
        for record in records
    ]
