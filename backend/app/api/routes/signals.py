from datetime import UTC, datetime

from fastapi import APIRouter

from app.domain.signal import SignalPreview

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("/preview/{symbol}", response_model=SignalPreview)
def preview_signal(symbol: str, timeframe: str = "1h") -> SignalPreview:
    # Safe default: without verified, fresh candles and strategy confirmation,
    # the engine abstains instead of inventing a BUY or SELL recommendation.
    return SignalPreview(
        symbol=symbol.upper(),
        timeframe=timeframe,
        generated_at=datetime.now(UTC),
        rationale=[
            "No verified live market-data provider is connected yet.",
            "No signal is emitted until freshness, data integrity and strategy confluence pass.",
        ],
    )
