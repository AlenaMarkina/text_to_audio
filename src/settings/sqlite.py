from src.settings.base import Settings


class SqliteSettings(Settings):
    SQLITE_DB: str


settings = SqliteSettings()
