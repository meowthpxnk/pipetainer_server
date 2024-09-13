import os

from app.schemas import LoggerLevel


class JWTConstants:
    DEFAULT_PRIVATE_KEY_PATH = "jwt_keys/private_jwt.pem"
    DEFAULT_PUBLIC_KEY_PATH = "jwt_keys/public_jwt.pem"

    DEFAULT_MAX_USER_SESSIONS = 5

    DEFAULT_ALGORITHM = "RS256"

    DEFAULT_ACCESS_TTL = 900
    DEFAULT_REFRESH_TTL = 28800


class LoggerConstants:
    DEFAULT_LEVEL = LoggerLevel.INFO


class DatabaseConstants:
    DEFAULT_URI = "sqlite:///database.db"


class ServerConstants:
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 2000


class RegistryConstants:
    DEFAULT_PATH = ""


class SuperUserConstants:
    DEFAULT_USERNAME = "admin"
    DEFAULT_PASSWORD = "admin_password"


class RedisConstants:
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = "6379"


class DeviceConstants:
    BASE_DEVICE_CONFIG = os.path.join(
        os.path.abspath("."), "config", ".base.device.yml"
    )


class WSManagerConstants:
    DEVICE_CACHE_PATTERN = "DEVICE.CACHE_DATA."
