from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic.networks import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings

from src.core.pydantic_types import TimezoneInfo


class AppSettings(BaseSettings, env_prefix="app_"):
    name: str = "Relikt Arte API"
    version: int = 1
    secret_key: str
    domain: str = "localhost:8000"
    protocol: str = "http"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}"


class CorsSettings(BaseSettings, env_prefix="cors_"):
    origins: list[str]


class DatabaseSettings(BaseSettings, env_prefix="postgres_"):
    db: str
    user: str
    password: str
    host: str
    port: int

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class JWTSettings(BaseSettings, env_prefix="jwt_"):
    algorithm: str
    access_token_expire: int
    refresh_token_expire: int


class StaticSettings(BaseSettings, env_prefix="static_"):
    dir: str = "static"
    max_file_size: int
    allowed_types: list[str]


class RedisSettings(BaseSettings, env_prefix="redis_"):
    password: str


class RabbitSettings(BaseSettings, env_prefix="rabbitmq_"):
    user: str
    password: str

    @property
    def url(self) -> str:
        return str(
            AmqpDsn.build(
                scheme="amqp",
                username=self.user,
                password=self.password,
                host="message_queue",
            )
        )


class Settings(BaseSettings):
    debug: bool
    timezone: TimezoneInfo

    # App
    app: AppSettings = Field(default_factory=AppSettings)
    # Cors
    cors: CorsSettings = Field(default_factory=CorsSettings)
    # Database
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # JWT
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    # Static
    static: StaticSettings = Field(default_factory=StaticSettings)
    # Redis
    redis: RedisSettings = Field(default_factory=RedisSettings)
    # RabbitMQ
    rabbit: RabbitSettings = Field(default_factory=RabbitSettings)


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings()


settings: Settings = get_settings()
