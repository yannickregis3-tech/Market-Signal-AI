from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class MarketGroup(StrEnum):
    FOREX = "forex"
    CRYPTO = "crypto"
    VOLATILITY = "volatility"
    DERIV_SYNTHETIC = "deriv_synthetic"


class MarketInstrument(BaseModel):
    model_config = ConfigDict(frozen=True)
    symbol: str
    display_name: str
    group: MarketGroup
    quote_currency: str | None = None
    provider: str | None = None
    enabled: bool = True


class Candle(BaseModel):
    model_config = ConfigDict(frozen=True)
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float | None = Field(default=None, ge=0)

    def validate_ohlc(self) -> bool:
        return self.high >= max(self.open, self.close, self.low) and self.low <= min(
            self.open, self.close, self.high
        )
