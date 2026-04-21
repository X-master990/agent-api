# Runtime and environment configuration for TrustMesh.
# Nested settings use env vars like "DATABASE__HOSTNAME" or "CRYPTO__ISSUER".


import logging.config
from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent


class Runtime(BaseModel):
    environment: str = "development"
    allowed_hosts: list[str] = ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]
    backend_cors_origins: list[AnyHttpUrl] = []


class Database(BaseModel):
    hostname: str = "postgres"
    username: str = "postgres"
    password: SecretStr = SecretStr("passwd-change-me")
    port: int = 5432
    db: str = "postgres"


class Prometheus(BaseModel):
    enabled: bool = False
    port: int = 9090
    addr: str = "0.0.0.0"
    stop_delay_secs: int = 0


class Crypto(BaseModel):
    issuer: str = "trustmesh.dev"
    private_key_encryption_secret: SecretStr = SecretStr(
        "trustmesh-dev-private-key-secret-change-me"
    )
    default_credential_ttl_seconds: int = Field(default=24 * 60 * 60, gt=60)


class Settings(BaseSettings):
    runtime: Runtime = Field(default_factory=Runtime)
    database: Database = Field(default_factory=Database)
    crypto: Crypto = Field(default_factory=Crypto)
    prometheus: Prometheus = Field(default_factory=Prometheus)

    log_level: str = "INFO"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.database.username,
            password=self.database.password.get_secret_value(),
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.db,
        )

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def logging_config(log_level: str) -> None:
    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} [{levelname}] {name}: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "": {
                "level": log_level,
                "handlers": ["stream"],
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(conf)


logging_config(log_level=get_settings().log_level)
