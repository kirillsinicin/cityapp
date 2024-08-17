from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: PostgresDsn

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")


settings = Settings()
