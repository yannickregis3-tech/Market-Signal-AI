from datetime import datetime
from typing import Protocol, Sequence

from pydantic import BaseModel, ConfigDict, Field

from app.domain.market import Candle


class MarketDataBatch(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: str
    symbol: str
    timeframe: str
    fetched_at: datetime
    candles: Sequence[Candle] = Field(min_length=1)


class MarketDataProvider(Protocol):
    name: str

    async def fetch_candles(
        self, symbol: str, timeframe: str, limit: int
    ) -> MarketDataBatch:
        """Fetch normalized candles from one upstream market-data source."""
        ...
