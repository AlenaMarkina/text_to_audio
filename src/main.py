from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from settings.postgresql import settings as postgresql_settings
from settings.sqlite import settings as sqlite_settings
from settings.base import settings as base_settings
from db import postgresql
from db import sqlite

from api.v1.router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    if base_settings.DB_TYPE == 'postgres':
        postgresql.async_engine = create_async_engine(postgresql_settings.DSN, echo=postgresql_settings.LOG_QUERIES)
        postgresql.async_session = async_sessionmaker(postgresql.async_engine, expire_on_commit=False)
    elif base_settings.DB_TYPE == 'sqlite':
        print(111111, sqlite_settings.DSN)
        sqlite.async_engine = create_async_engine(sqlite_settings.DSN, echo=sqlite_settings.LOG_QUERIES)
        sqlite.async_session = async_sessionmaker(sqlite.async_engine, expire_on_commit=False)

    print(222222, sqlite.async_session)
    yield
    if base_settings.DB_TYPE == 'postgres':
        await postgresql.async_engine.dispose()
    elif base_settings.DB_TYPE == 'sqlite':
        await sqlite.async_engine.dispose()


app = FastAPI(
    title='Text to audio API',
    # openapi_url=api_settings.OPENAPI_URL,
    docs_url='/api/text_to_audio/docs',
    # redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    # root_path="/content",
)

# app.include_router(v1_router)
app.include_router(router)
