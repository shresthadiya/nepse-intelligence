from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
import statistics

from app.database import get_db
from app.models import Company, StockPrice
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Analytics"])


@router.get("/{company_id}/behavior-summary")
def get_behavior_summary(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    prices = db.query(StockPrice).filter(
        StockPrice.company_id == company_id
    ).order_by(desc(StockPrice.date)).limit(30).all()

    if not prices:
        raise HTTPException(
            status_code=404,
            detail="No stock price data available"
        )

    prices = list(reversed(prices))

    total_volume = sum(
        float(price.volume or 0) for price in prices
    )

    total_turnover = sum(
        float(price.close or 0) *
        float(price.volume or 0)
        for price in prices
    )

    vwap = (
        total_turnover / total_volume
        if total_volume > 0 else 0
    )

    # Estimate buying/selling pressure from daily
    # closing-price movement. This is a proxy, not
    # actual broker-level transaction data.
    buy_volume = 0
    sell_volume = 0

    for price in prices:
        volume = float(price.volume or 0)
        opening = float(price.open or 0)
        closing = float(price.close or 0)

        if closing > opening:
            buy_volume += volume
        elif closing < opening:
            sell_volume += volume

    total_pressure_volume = buy_volume + sell_volume

    if total_pressure_volume:
        pressure = (
            (buy_volume - sell_volume) /
            total_pressure_volume
        ) * 100
    else:
        pressure = 0

    volumes = [
        float(price.volume or 0)
        for price in prices
    ]

    average_volume = statistics.mean(volumes)

    std_volume = (
        statistics.stdev(volumes)
        if len(volumes) > 1 else 0
    )

    anomalies = [
        {
            "date": price.date,
            "volume": float(price.volume or 0)
        }
        for price in prices
        if float(price.volume or 0) >
        average_volume + (2 * std_volume)
    ]

    latest_close = float(prices[-1].close or 0)

    return {
        "company": company.name,
        "symbol": company.symbol,
        "period_days": len(prices),
        "vwap": round(vwap, 2),
        "latest_closing_price": latest_close,
        "buy_volume": buy_volume,
        "sell_volume": sell_volume,
        "buy_sell_pressure": round(pressure, 2),
        "pressure_indicator": (
            "Buying Pressure" if pressure > 0
            else "Selling Pressure" if pressure < 0
            else "Neutral"
        ),
        "average_volume": round(average_volume, 2),
        "volume_anomalies": anomalies,
        "anomaly_threshold": "Mean + 2 standard deviations"
    }