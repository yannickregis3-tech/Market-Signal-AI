from app.core.config import Settings, settings
from app.data_engine.deriv import DerivMarketDataProvider
from app.data_engine.registry import ProviderRegistry


def build_provider_registry(config: Settings = settings) -> ProviderRegistry:
    """Build only providers whose required configuration is explicitly present."""
    registry = ProviderRegistry()
    symbol_map = config.deriv_symbol_map
    if symbol_map:
        registry.register(
            DerivMarketDataProvider(
                symbol_map=symbol_map,
                websocket_url=config.deriv_public_ws_url,
            )
        )
    return registry
