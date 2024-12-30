from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Extra
class Settings(BaseSettings):
    app_title: str
    app_description: str
    app_version: str
    pg_url: PostgresDsn

    class Config:
        env_file = None
        env_file_encoding = "utf-8"
        extra = Extra.allow
        env_prefix = "BK_"


settings = Settings()