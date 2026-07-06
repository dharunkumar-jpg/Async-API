from functools import lru_cache    #iru cache stores the caches result of function
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.

    BaseSettings automatically reads environment variables and
    assigns them to the corresponding class attributes.

    it also validates their data type, centralizes the all application configuration in one place
    """
    app_name: str
    DATABASE_URL: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    debug: bool
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
#decorator caches the result of get setting
@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The configuration is loaded only once during the application's
    lifetime and reused everywhere.
    """
    return Settings()
settings = get_settings()