import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "prod"
    SW_HOST: str
    SW_USER: str
    SW_PASS: str

    class Config:
        env_file = ".env"

class TestSettings(Settings):
    ENVIRONMENT: str = "test"

SETTINGS = {
    "test": TestSettings
}

@lru_cache
def load_settings():
    return SETTINGS.get(os.getenv("CLI_ENVIRONMENT"), Settings)()
