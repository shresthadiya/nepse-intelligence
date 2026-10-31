
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.company import Company
from app.services.stock_price_service import StockPriceService
from app.crawlers.stock_price_provider import StockPriceProvider


class StockPriceCrawler:
    """
    Collects historical stock prices for registered companies.
    """

    def __init__(
        self,
        db: Session,
        provider: StockPriceProvider
    ):
        self.db = db
        self.provider = provider
        self.service = StockPriceService()

    def crawl_company(
        self,
        company: Company,
        start_date: date,
        end_date: date
    ):
        records = self.provider.fetch_prices(
            symbol=company.symbol,
            start_date=start_date,
            end_date=end_date
        )

        result = self.service.save_prices(
            db=self.db,
            company_id=company.id,
            records=records
        )

        return result

    def crawl_all(
        self,
        start_date: date,
        end_date: date
    ):
        companies = self.db.query(Company).filter(
            Company.is_active.is_(True)
        ).all()

        results = []
        errors = []

        for company in companies:
            try:
                result = self.crawl_company(
                    company,
                    start_date,
                    end_date
                )

                results.append(result)

            except Exception as error:
                self.db.rollback()

                errors.append({
                    "symbol": company.symbol,
                    "error": str(error)
                })

        return {
            "companies_processed": len(results),
            "companies_failed": len(errors),
            "inserted": sum(
                item["inserted"] for item in results
            ),
            "updated": sum(
                item["updated"] for item in results
            ),
            "results": results,
            "errors": errors
        }

    def crawl_last_30_days(self):
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        return self.crawl_all(
            start_date=start_date,
            end_date=end_date
        )
