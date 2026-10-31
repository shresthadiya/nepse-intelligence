from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Company, StockPrice
from app.schemas.company import (
    CompanyResponse,
    CompanyPriceHistoryResponse
)

router = APIRouter(
    prefix="/api/companies",
    tags=["Companies"]
)


@router.get("", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):

    companies = (
        db.query(Company)
        .filter(Company.is_active == True)
        .order_by(Company.symbol)
        .all()
    )

    return companies


@router.get(
    "/{company_id}/prices",
    response_model=CompanyPriceHistoryResponse
)
def get_company_prices(
    company_id: int,
    range: str = Query(
        default="30d",
        pattern="^(7d|30d|90d|1y|all)$"
    ),
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.id == company_id,
        Company.is_active == True
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    query = db.query(StockPrice).filter(
        StockPrice.company_id == company_id
    )

    if range != "all":

        days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "1y": 365
        }

        start_date = date.today() - timedelta(
            days=days[range]
        )

        query = query.filter(
            StockPrice.date >= start_date
        )

    prices = query.order_by(StockPrice.date.asc()).all()

    return {
        "company_id": company.id,
        "symbol": company.symbol,
        "range": range,
        "prices": prices
    }