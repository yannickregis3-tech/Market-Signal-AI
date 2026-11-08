from datetime import UTC, datetime

import pytest

from app.data_engine.deriv import (
    DerivMarketDataProvider,
    DerivProviderError,
    TIMEFRAME_GRANULARITY,
)


def test_deriv_timeframe_granularity_is_explicit():
    assert TIMEFRAME_GRANULARITY["1m"] == 60
    assert TIMEFRAME_GRANULARITY["1h"] == 3600
    assert TIMEFRAME_GRANULARITY["1d"] == 86400


def test_deriv_symbol_mapping_is_required_and_never_guessed():
    provider = DerivMarketDataProvider(symbol_map={})
    with pytest.raises(ValueError, match="No verified Deriv symbol mapping"):
        import asyncio

        asyncio.run(provider.fetch_candles("DERIV_VOL10", "1m", 20))


def test_deriv_candle_parser_normalizes_ohlc_and_utc_timestamps():
    epoch = int(datetime(2026, 1, 1, tzinfo=UTC).timestamp())
    candles = DerivMarketDataProvider._parse_candles(
        [
            {
                "epoch": epoch,
                "open": 100.0,
                "high": 105.0,
                "low": 98.0,
                "close": 103.0,
            }
        ],
        "DERIV_VOL10",
        "5m",
    )
    assert len(candles) == 1
    assert candles[0].timestamp == datetime(2026, 1, 1, tzinfo=UTC)
    assert candles[0].symbol == "DERIV_VOL10"
    assert candles[0].validate_ohlc()


def test_deriv_candle_parser_discards_incomplete_or_invalid_rows():
    candles = DerivMarketDataProvider._parse_candles(
        [
            {"epoch": 1, "open": 10, "high": 9, "low": 8, "close": 9},
            {"epoch": 2, "open": 10, "high": 12, "low": 8},
        ],
        "DERIV_VOL10",
        "1m",
    )
    assert candles == []
