from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgresql import get_async_session as pg_session
from db.sqlite import get_async_session as sqlite_session
from settings.base import settings

Session = Annotated[AsyncSession, Depends(sqlite_session if settings.DB_TYPE == 'sqlite' else pg_session)]
