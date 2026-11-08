# Market data providers

## Deriv

The Deriv adapter uses the public WebSocket endpoint:

`wss://api.derivws.com/trading/v1/options/ws/public`

It supports unauthenticated active-symbol discovery and OHLC candle history. No account token or trading permission is needed for these public market-data calls.

Before enabling a catalogue instrument, retrieve the active-symbol list with `DerivMarketDataProvider.fetch_active_symbols()` and verify the exact `symbol` code and display name. Pass only verified mappings into `DerivMarketDataProvider(symbol_map=...)`. The adapter intentionally refuses to guess codes from catalogue labels.

Supported candle intervals: 1m, 2m, 3m, 5m, 10m, 15m, 30m, 1h, 2h, 4h, 8h and 1d. A returned batch must still pass the shared freshness and OHLC quality gate before it can be used by a strategy.

## CBOE VIX

The CBOE VIX is a distinct index, not a Deriv synthetic index. CBOE's public product page displays delayed data; its real-time Global Indices Feed is a separately licensed service. Do not treat a scraped delayed quote as a real-time trading feed, and do not redistribute CBOE index data without the appropriate rights.

## Provider safety rules

- Preserve the upstream provider name and timestamp for every batch.
- Reject stale, malformed, future-dated or symbol-mismatched data.
- Never substitute one provider silently for another.
- Keep a market unavailable until its provider and exact symbol mapping are verified.
- A missing or unhealthy feed must result in NO_TRADE, not a fabricated signal.
