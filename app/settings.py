from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

from app.constants import (
    DatabaseConstants,
    JWTConstants,
    LoggerConstants,
    RedisConstants,
    RegistryConstants,
    ServerConstants,
    SuperUserConstants,
)
from app.schemas import LoggerLevel


load_dotenv()


class DockerSettings(BaseSettings):
    registry_url: str = Field(
        RegistryConstants.DEFAULT_PATH, alias="REGISTRY_URL"
    )


class ApiSettings(BaseSettings):
    host: str = Field(ServerConstants.DEFAULT_HOST, alias="API_HOST")
    port: int = Field(ServerConstants.DEFAULT_PORT, alias="API_PORT")


class DatabaseSettings(BaseSettings):
    uri: str = Field(DatabaseConstants.DEFAULT_URI, alias="DATABASE_URI")


class LoggerSettings(BaseSettings):
    level: LoggerLevel = Field(
        LoggerConstants.DEFAULT_LEVEL, alias="LOGGER_LEVEL"
    )


import os


class AuthJWTSettings(BaseSettings):
    access_ttl: int = Field(
        JWTConstants.DEFAULT_ACCESS_TTL, alias="ACCESS_TOKEN_TTL"
    )
    refresh_ttl: int = Field(
        JWTConstants.DEFAULT_REFRESH_TTL, alias="REFRESH_TOKEN_TTL"
    )

    private_key_path: str = Field(
        JWTConstants.DEFAULT_PRIVATE_KEY_PATH, alias="PRIVATE_JWT_KEY_PATH"
    )

    public_key_path: str = Field(
        JWTConstants.DEFAULT_PUBLIC_KEY_PATH, alias="PUBLIC_JWT_KEY_PATH"
    )

    max_user_sessions: int = Field(
        JWTConstants.DEFAULT_MAX_USER_SESSIONS, alias="MAX_USER_SESSIONS"
    )

    algorithm: str = JWTConstants.DEFAULT_ALGORITHM


class RedisSettings(BaseSettings):
    host: str = Field(RedisConstants.DEFAULT_HOST, alias="REDIS_HOST")
    port: int = Field(RedisConstants.DEFAULT_PORT, alias="REDIS_PORT")


class SuperUserSettings(BaseSettings):
    username: str = Field(
        SuperUserConstants.DEFAULT_USERNAME, alias="SUPER_USER_USERNAME"
    )
    password: str = Field(
        SuperUserConstants.DEFAULT_PASSWORD, alias="SUPER_USER_PASSWORD"
    )


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    logger: LoggerSettings = LoggerSettings()
    api: ApiSettings = ApiSettings()
    docker: DockerSettings = DockerSettings()
    jwt: AuthJWTSettings = AuthJWTSettings()
    redis: RedisSettings = RedisSettings()
    super_user: SuperUserSettings = SuperUserSettings()
