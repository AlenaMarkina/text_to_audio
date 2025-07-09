from settings.base import Settings, ROOT_DIR

from pydantic_core.core_schema import FieldValidationInfo
from pydantic import PostgresDsn, SecretStr, field_validator


class SqliteSettings(Settings):
    SQLITE_DB: str
    DSN: str | None = None

    LOG_QUERIES: bool = False
    # sqlite_url = f"sqlite:////Users/alena/PycharmProjects/text_to_audio/{sqlite_file_name}"

    @field_validator("DSN", mode="before")
    @classmethod
    def assemble_dsn(cls, _: str | None, info: FieldValidationInfo):
        scheme = "sqlite+aiosqlite"
        db = info.data["SQLITE_DB"]

        url = f"{scheme}:///{ROOT_DIR}/{db}"
        # print(111111, url)
        return url


settings = SqliteSettings()
print(settings.DSN)
