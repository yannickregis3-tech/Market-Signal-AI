from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SignalDirection(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    NO_TRADE = "NO_TRADE"


class SignalStatus(StrEnum):
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"
    INVALIDATED = "invalidated"
    EXPIRED = "expired"


class SignalPreview(BaseModel):
    symbol: str
    direction: SignalDirection = SignalDirection.NO_TRADE
    status: SignalStatus = SignalStatus.CANDIDATE
    timeframe: str
    confidence: float = Field(default=0, ge=0, le=100)
    entry: float | None = None
    stop_loss: float | None = None
    take_profits: list[float] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    data_timestamp: datetime | None = None
    generated_at: datetime
