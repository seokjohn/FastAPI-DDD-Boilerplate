import os
from datetime import timedelta
from os import path, environ, mkdir

from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from pydantic import BaseSettings


BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
TEMP_DIR = path.join(BASE_DIR, ".tmp")
if not path.isdir(TEMP_DIR):  # pragma: no cover
    mkdir(TEMP_DIR)

load_dotenv(verbose=True)


class GlobalSettings(BaseSettings):
    """
    기본 Configuration
    """
    ENV_STATE: str = environ.get("ENV_STATE", "dev")
    BASE_DIR: str = BASE_DIR
    TEMP_DIR: str = TEMP_DIR
    
    # JWT
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", None)
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", None)

    # Authorization
    API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=True)
    
    BROKER_URI = environ.get("BROKER_URI", None)
    BACKEND_URI = environ.get("BACKEND_URI", None)
    SCHEDULE_QUEUE = environ.get("SCHEDULE_QUEUE", None)

    # Google
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)


class DevSettings(GlobalSettings):
    DOMAIN = "https://localhost"
    PORT = 8080
    ALLOW_SITE = ["*"]
    DEBUG: bool = False


class ProdSettings(GlobalSettings):
    DOMAIN = ""
    PORT = 8080
    ALLOW_SITE = ["*"]


def get_settings():
    env_state = GlobalSettings().ENV_STATE
    setting_type = {
        "local": DevSettings(),
        "dev": DevSettings(),
        "prod": ProdSettings(),
    }
    return setting_type[env_state]


SETTINGS: GlobalSettings = get_settings()
