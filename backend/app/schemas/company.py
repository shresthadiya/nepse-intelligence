from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class CompanyResponse(BaseModel):
    id: int
    symbol: str
    name: str
    sector: Optional[str] = None
    is_active: bool

class StockPriceResponse(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class CompanyPriceHistoryResponse(BaseModel):
    company_id: int
    symbol: str
    range: str
    prices: List[StockPriceResponse]