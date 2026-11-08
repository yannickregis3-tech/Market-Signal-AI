import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Market Signal AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str | None = None
    market_data_max_age_seconds: int = 180
    deriv_public_ws_url: str = "wss://api.derivws.com/trading/v1/options/ws/public"
    deriv_symbol_map_json: str = "{}"
    log_level: str = "INFO"

    @property
    def deriv_symbol_map(self) -> dict[str, str]:
        try:
            value = json.loads(self.deriv_symbol_map_json)
        except json.JSONDecodeError as exc:
            raise ValueError("DERIV_SYMBOL_MAP_JSON must be valid JSON.") from exc
        if not isinstance(value, dict) or not all(
            isinstance(key, str) and isinstance(symbol, str) and symbol.strip()
            for key, symbol in value.items()
        ):
            raise ValueError("DERIV_SYMBOL_MAP_JSON must be a JSON object of string mappings.")
        return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
