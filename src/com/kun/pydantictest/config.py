from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import DotenvType, ENV_FILE_SENTINEL


class Settings(BaseSettings):
    environment: str = ""
    app_key: str = ""

#    class Config:
#        env_file = ".env"


class ProdConfig(Settings):
    def __init__(self):
        self.environment = "prod_env"
        self.app_key = "prod_key"


class DevConfig(Settings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings(env: str) -> Settings:
    if env == "prod":
        return ProdConfig()
    elif env == "dev":
        return DevConfig()
    else:
        print("Unknown env")
        raise ValueError("Unknown env")
