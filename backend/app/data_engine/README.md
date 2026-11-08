# Market Data Engine

The data engine normalizes provider responses into the canonical Candle model and applies quality gates before any analysis can consume them.

## Contract

Each adapter implements MarketDataProvider and returns MarketDataBatch with provider identity, symbol, timeframe, fetch timestamp and normalized candles.

## Hard rejection rules

- Provider fetch time must be timezone-aware and within the configured freshness window.
- Candle timestamps must be timezone-aware and cannot be in the future.
- Candle symbol and timeframe must match the requested batch.
- OHLC values must be internally consistent.
- A batch with any quality issue is rejected as a whole in this first safe implementation.

Provider adapters are intentionally separate by market family. Deriv synthetic indices require a dedicated Deriv adapter and symbol mapping. No live provider is configured yet; no sample or fabricated prices are treated as live data.
