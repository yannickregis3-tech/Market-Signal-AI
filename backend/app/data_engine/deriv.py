import asyncio
import json
from datetime import UTC, datetime

from websockets.asyncio.client import connect

from app.data_engine.provider import MarketDataBatch
from app.domain.market import Candle


TIMEFRAME_GRANULARITY: dict[str, int] = {
    "1m": 60,
    "2m": 120,
    "3m": 180,
    "5m": 300,
    "10m": 600,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "8h": 28800,
    "1d": 86400,
}


class DerivProviderError(RuntimeError):
    """Raised when Deriv returns an error or unusable market data."""


class DerivMarketDataProvider:
    """Fetch OHLC candles from Deriv's public, unauthenticated WebSocket API.

    `symbol_map` must contain verified Deriv symbols. We deliberately do not
    guess mappings between our catalogue identifiers and Deriv's market codes.
    """

    name = "deriv"

    def __init__(
        self,
        *,
        symbol_map: dict[str, str],
        websocket_url: str = "wss://api.derivws.com/trading/v1/options/ws/public",
        timeout_seconds: float = 15.0,
    ) -> None:
        self._symbol_map = {key.upper(): value for key, value in symbol_map.items()}
        self._websocket_url = websocket_url
        self._timeout_seconds = timeout_seconds

    async def fetch_active_symbols(self) -> list[dict]:
        """Return Deriv's active-symbol catalogue for explicit mapping review."""
        try:
            async with connect(
                self._websocket_url,
                open_timeout=self._timeout_seconds,
                close_timeout=5,
            ) as websocket:
                await websocket.send(json.dumps({"active_symbols": "full", "req_id": 2}))
                async with asyncio.timeout(self._timeout_seconds):
                    while True:
                        payload = json.loads(await websocket.recv())
                        if payload.get("error"):
                            message = payload["error"].get("message", "Unknown Deriv error")
                            raise DerivProviderError(f"Deriv API error: {message}")
                        if payload.get("msg_type") == "active_symbols":
                            symbols = payload.get("active_symbols", [])
                            return [item for item in symbols if isinstance(item, dict)]
        except TimeoutError as exc:
            raise DerivProviderError("Timed out while retrieving Deriv active symbols.") from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise DerivProviderError(f"Unable to read Deriv symbols: {exc}") from exc

    async def fetch_candles(
        self, symbol: str, timeframe: str, limit: int
    ) -> MarketDataBatch:
        if limit < 1 or limit > 5000:
            raise ValueError("limit must be between 1 and 5000")
        if timeframe not in TIMEFRAME_GRANULARITY:
            raise ValueError(f"Unsupported Deriv timeframe: {timeframe}")

        deriv_symbol = self._symbol_map.get(symbol.upper())
        if not deriv_symbol:
            raise ValueError(
                f"No verified Deriv symbol mapping configured for '{symbol}'."
            )

        request = {
            "ticks_history": deriv_symbol,
            "end": "latest",
            "count": limit,
            "style": "candles",
            "granularity": TIMEFRAME_GRANULARITY[timeframe],
            "req_id": 1,
        }

        try:
            async with connect(
                self._websocket_url,
                open_timeout=self._timeout_seconds,
                close_timeout=5,
            ) as websocket:
                await websocket.send(json.dumps(request))
                async with asyncio.timeout(self._timeout_seconds):
                    while True:
                        raw_message = await websocket.recv()
                        payload = json.loads(raw_message)
                        if payload.get("error"):
                            message = payload["error"].get("message", "Unknown Deriv error")
                            raise DerivProviderError(f"Deriv API error: {message}")
                        if payload.get("msg_type") == "candles":
                            candles = self._parse_candles(
                                payload.get("candles", []), symbol, timeframe
                            )
                            if not candles:
                                raise DerivProviderError(
                                    f"Deriv returned no candles for {deriv_symbol}."
                                )
                            return MarketDataBatch(
                                provider=self.name,
                                symbol=symbol,
                                timeframe=timeframe,
                                fetched_at=datetime.now(UTC),
                                candles=candles,
                            )
        except TimeoutError as exc:
            raise DerivProviderError("Timed out while waiting for Deriv candle data.") from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise DerivProviderError(f"Unable to read Deriv market data: {exc}") from exc

    @staticmethod
    def _parse_candles(
        raw_candles: list[dict], symbol: str, timeframe: str
    ) -> list[Candle]:
        parsed: list[Candle] = []
        for item in raw_candles:
            required = ("epoch", "open", "high", "low", "close")
            if any(item.get(field) is None for field in required):
                continue
            candle = Candle(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=datetime.fromtimestamp(int(item["epoch"]), UTC),
                open=float(item["open"]),
                high=float(item["high"]),
                low=float(item["low"]),
                close=float(item["close"]),
            )
            if candle.validate_ohlc():
                parsed.append(candle)
        return sorted(parsed, key=lambda candle: candle.timestamp)
