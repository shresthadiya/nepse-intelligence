
from datetime import date, datetime
from math import isfinite

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.stock_price import StockPrice


class StockPriceService:

    @staticmethod
    def save_prices(db: Session, company_id: int, records: list):
        """
        Validate and save historical stock prices.

        Existing company/date records are updated rather than duplicated.
        """

        company = db.query(Company).filter(
            Company.id == company_id
        ).first()

        if not company:
            raise ValueError(f"Company {company_id} not found")

        inserted = 0
        updated = 0

        try:
            for record in records:

                price_date = record["date"]

                if isinstance(price_date, str):
                    price_date = date.fromisoformat(price_date)
                elif isinstance(price_date, datetime):
                    price_date = price_date.date()

                open_price = float(record["open"])
                high_price = float(record["high"])
                low_price = float(record["low"])
                close_price = float(record["close"])
                volume = int(record["volume"])

                values = [
                    open_price,
                    high_price,
                    low_price,
                    close_price
                ]

                if not all(isfinite(value) and value > 0 for value in values):
                    raise ValueError("Prices must be finite positive numbers")

                if volume < 0:
                    raise ValueError("Volume cannot be negative")

                if high_price < max(open_price, close_price, low_price):
                    raise ValueError("Invalid high price")

                if low_price > min(open_price, close_price, high_price):
                    raise ValueError("Invalid low price")

                existing = db.query(StockPrice).filter(
                    StockPrice.company_id == company_id,
                    StockPrice.date == price_date
                ).first()

                if existing:
                    existing.open = open_price
                    existing.high = high_price
                    existing.low = low_price
                    existing.close = close_price
                    existing.volume = volume
                    updated += 1

                else:
                    stock_price = StockPrice(
                        company_id=company_id,
                        date=price_date,
                        open=open_price,
                        high=high_price,
                        low=low_price,
                        close=close_price,
                        volume=volume
                    )

                    db.add(stock_price)
                    inserted += 1

            db.commit()

            return {
                "company_id": company_id,
                "symbol": company.symbol,
                "inserted": inserted,
                "updated": updated,
                "total_processed": inserted + updated
            }

        except Exception:
            db.rollback()
            raise
