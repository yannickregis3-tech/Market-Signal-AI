from app.data_engine.provider import MarketDataProvider


class ProviderRegistry:
    """Explicit provider registry; never silently substitutes a different feed."""

    def __init__(self) -> None:
        self._providers: dict[str, MarketDataProvider] = {}

    def register(self, provider: MarketDataProvider) -> None:
        key = provider.name.strip().lower()
        if not key:
            raise ValueError("Provider name cannot be empty.")
        if key in self._providers:
            raise ValueError(f"Provider already registered: {key}")
        self._providers[key] = provider

    def get(self, name: str) -> MarketDataProvider:
        key = name.strip().lower()
        try:
            return self._providers[key]
        except KeyError as exc:
            raise LookupError(f"No market-data provider registered as '{key}'.") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))
