# from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.v1.router import router
from db import sqlite


sqlite_file_name = "audio_guide.db3"
sqlite_url = f"sqlite:////Users/alena/PycharmProjects/text_to_audio/{sqlite_file_name}"


# @asynccontextmanager
def lifespan(_: FastAPI):
    sqlite.engine = create_engine(sqlite_url)
    sqlite.session = sessionmaker(sqlite.engine, expire_on_commit=False)
    yield
    sqlite.engine.dispose()


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
