from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Market Signal AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str | None = None
    market_data_max_age_seconds: int = 180
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
