from pydantic import PostgresDsn, SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from settings.base import Settings


class PostgreSQLSettings(Settings):
    PG_USER: str
    PG_PASSWORD: SecretStr
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_SCHEMA: str
    DSN: str | None = None

    LOG_QUERIES: bool = False

    @field_validator("DSN", mode="before")
    @classmethod
    def assemble_dsn(cls, _: str | None, info: FieldValidationInfo) -> PostgresDsn:
        scheme = "postgresql+asyncpg"
        user = info.data["PG_USER"]
        password = info.data["PG_PASSWORD"].get_secret_value()
        host = info.data["PG_HOST"]
        port = info.data["PG_PORT"]
        db = info.data["PG_DB"]

        url = f"{scheme}://{user}:{password}@{host}:{port}/{db}"
        return PostgresDsn(url).unicode_string()


settings = PostgreSQLSettings()

