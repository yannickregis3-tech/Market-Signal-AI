# Roadmap

## Milestone 0 — repository foundation
- [x] Initialize repository and architecture notes
- [x] Create FastAPI service and health endpoint
- [x] Define market and signal contracts
- [x] Seed instrument catalogue
- [x] Add deterministic API tests
- [ ] Run CI and verify test suite

## Milestone 1 — persistence and configuration
- [x] Define SQLAlchemy models and initial Alembic migration
- [x] Provision temporary Render PostgreSQL staging database
- [ ] Configure a secure application-to-database connection
- [ ] Apply migrations and verify the schema
- [ ] Persist instruments, candles, scans and signal decisions
- [ ] Integration tests with a disposable PostgreSQL database

## Milestone 2 — market data
- [x] Provider contract, provenance, freshness and OHLC quality gates
- [x] Dedicated Deriv WebSocket adapter and active-symbol discovery
- [x] Explicit provider registry and safe configuration factory
- [ ] Verify Deriv symbols and configure the production symbol map
- [ ] Forex adapter
- [ ] Crypto adapter
- [ ] Conventional volatility benchmark adapter
- [ ] Provider retries, rate limits and operational monitoring

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

## Current staging constraints
- The Render PostgreSQL database is on the Free plan and expires on 8 December 2026.
- The Render database currently has an empty IP allowlist; hosted MCP queries are therefore blocked. Do not open access to all IPs as a workaround.
- The Deriv adapter remains inactive until real symbol codes are verified and configured.
- GitHub Actions status has not yet reported a successful run; do not treat tests as passed.

No strategy is production-ready based only on an in-sample backtest. No profit is guaranteed.
