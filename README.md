# Market Signal AI

Multi-market market-analysis and trading-signal platform for Forex, cryptocurrencies, conventional volatility benchmarks and Deriv synthetic indices.

> Research and decision-support software only. Signals are hypotheses, not guarantees of profit. No order execution is enabled in the initial release.

## Initial architecture

- **API:** Python 3.12, FastAPI, Pydantic v2
- **Persistence:** PostgreSQL, SQLAlchemy 2, Alembic
- **Market data:** provider adapters with explicit freshness and provenance metadata
- **Analysis:** indicator library, strategy registry, confluence/scoring engine
- **Operations:** scheduled scans, health checks, structured logs
- **Validation:** deterministic tests, backtesting and out-of-sample validation before strategies are promoted

## Market groups

1. Forex spot pairs
2. Crypto spot pairs
3. Conventional volatility benchmarks and volatility measures
4. Deriv synthetic indices (dedicated adapter; never assume they are interchangeable with exchange-traded markets)

## Safety principles

- Never emit a trade signal from stale, missing, malformed or unverified data.
- Every actionable signal must define entry, invalidation/stop level, targets, timeframe, timestamp and rationale.
- Conflicting or insufficient evidence produces `NO_TRADE`.
- Risk limits are advisory and configurable; no profit is guaranteed.
- No broker credentials, private keys or live order execution in this initial version.

## Development

See [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md) and `backend/README.md`.

```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API starts without a database for local health checks. Set `DATABASE_URL` to enable PostgreSQL persistence as database integration is implemented.
