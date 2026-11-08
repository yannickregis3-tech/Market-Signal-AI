from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.data_engine.provider import MarketDataBatch


@dataclass(frozen=True)
class DataQualityResult:
    accepted: bool
    reasons: tuple[str, ...]
    accepted_candles: tuple


def validate_batch(
    batch: MarketDataBatch,
    *,
    max_age: timedelta,
    now: datetime | None = None,
) -> DataQualityResult:
    """Reject stale, future-dated, malformed or mismatched provider batches."""
    current_time = now or datetime.now(UTC)
    reasons: list[str] = []
    accepted_candles = []

    fetched_at = batch.fetched_at
    if fetched_at.tzinfo is None:
        reasons.append("Provider fetch timestamp must include a timezone.")
    elif fetched_at > current_time + timedelta(seconds=5):
        reasons.append("Provider fetch timestamp is in the future.")
    elif current_time - fetched_at > max_age:
        reasons.append("Provider batch is stale.")

    for candle in batch.candles:
        if candle.symbol.upper() != batch.symbol.upper():
            reasons.append("Candle symbol does not match batch symbol.")
            continue
        if candle.timeframe != batch.timeframe:
            reasons.append("Candle timeframe does not match batch timeframe.")
            continue
        if candle.timestamp.tzinfo is None:
            reasons.append("Candle timestamp must include a timezone.")
            continue
        if candle.timestamp > current_time + timedelta(seconds=5):
            reasons.append("Candle timestamp is in the future.")
            continue
        if not candle.validate_ohlc():
            reasons.append("Candle OHLC values are inconsistent.")
            continue
        accepted_candles.append(candle)

    if not accepted_candles:
        reasons.append("No valid candles remain in the provider batch.")

    return DataQualityResult(
        accepted=not reasons,
        reasons=tuple(dict.fromkeys(reasons)),
        accepted_candles=tuple(accepted_candles) if not reasons else (),
    )
