# from sqlalchemy import Engine
# from sqlalchemy.orm import sessionmaker, Session
#
#
# # sqlite_file_name = "audio_guide.db3"
# # sqlite_url = f"sqlite:////Users/alena/PycharmProjects/text_to_audio/{sqlite_file_name}"
# #
# # connect_args = {"check_same_thread": False}
# # engine = create_engine(sqlite_url, connect_args=connect_args)
# # Session = sessionmaker(engine)
#
#
# engine: Engine | None = None
# session: sessionmaker[Session] | None = None
#
#
# def get_session():
#     with session() as s:
#         yield s


from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

async_engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session