
from abc import ABC, abstractmethod
from datetime import date


class StockPriceProvider(ABC):
    """
    Interface for authorized historical NEPSE data providers.

    Provider implementations must return normalized OHLC records.
    """

    @abstractmethod
    def fetch_prices(
        self,
        symbol: str,
        start_date: date,
        end_date: date
    ) -> list[dict]:
        """
        Expected record format:

        {
            "date": "2026-10-01",
            "open": 245.0,
            "high": 250.0,
            "low": 243.0,
            "close": 248.0,
            "volume": 12500
        }
        """
        raise NotImplementedError
