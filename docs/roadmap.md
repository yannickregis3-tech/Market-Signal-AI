# Roadmap

## Milestone 0 — repository foundation
- [x] Initialize repository and architecture notes
- [x] Create FastAPI service and health endpoint
- [x] Define market and signal contracts
- [x] Seed instrument catalogue
- [x] Add deterministic API tests
- [ ] Run CI and verify test suite

## Milestone 1 — persistence and configuration
- [ ] PostgreSQL service and secure connection configuration
- [ ] SQLAlchemy models and Alembic migrations
- [ ] Persist instruments, candles, scans and signal decisions
- [ ] Integration tests with a disposable PostgreSQL database

## Milestone 2 — market data
- [ ] Provider contract, retries, rate limits and provenance
- [ ] Forex adapter
- [ ] Crypto adapter
- [ ] Conventional volatility benchmark adapter
- [ ] Dedicated Deriv synthetic indices adapter
- [ ] Freshness monitor and data-quality gates

## Milestone 3 — analysis
- [ ] Indicators and market structure
- [ ] Nine strategy families
- [ ] Confluence and conflict resolver
- [ ] Signal scoring and risk validation
- [ ] Explicit NO_TRADE explanations

## Milestone 4 — validation and operations
- [ ] Backtesting with spread, fees and slippage
- [ ] Walk-forward and out-of-sample validation
- [ ] Demo/paper signal tracking
- [ ] Alerts, monitoring and performance reporting
- [ ] Frontend dashboard (separate milestone)

No strategy is production-ready based only on an in-sample backtest. No profit is guaranteed.
