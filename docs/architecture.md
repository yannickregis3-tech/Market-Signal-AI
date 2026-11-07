# Architecture — initial baseline

## Service boundaries

- API layer: FastAPI routes; validates requests and returns typed responses.
- Domain layer: market instruments, OHLCV candles and signal contracts; no provider-specific code.
- Market-data adapters (next milestone): isolated connectors for FX, crypto, conventional volatility benchmarks and Deriv synthetic indices.
- Analysis engine (planned): indicators, nine strategy families, confluence scoring and explicit abstention.
- Persistence (planned): PostgreSQL via SQLAlchemy 2 and Alembic; raw candles, normalized candles, scans, signals and audit events.
- Workers (planned): scheduled scans and stream consumers, separated from HTTP request workers.

## Data integrity requirements

Every observation must carry provider, instrument, timeframe, event timestamp, received timestamp and source metadata. Reject invalid OHLC candles and stale observations. Provider outages must never be represented as a flat or zero price.

Deriv synthetic indices use a dedicated provider adapter and symbol mapping. Do not merge their feed assumptions with FX, exchange crypto or VIX.

## Signal lifecycle

A strategy emits a candidate, not an order. The signal engine checks data freshness, candle integrity, minimum confluence, conflicting direction, stop placement and risk constraints. If any hard gate fails, return NO_TRADE with reasons. Persist every candidate and decision for later evaluation.

## Security

Secrets are environment-only. Never commit API keys, broker tokens, database passwords or user credentials. The initial product is analysis-only; no live execution endpoint exists.
