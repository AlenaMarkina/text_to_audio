import uuid
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    registry
)

from settings.base import settings

mapper_registry = registry()


class Base(DeclarativeBase):
    # id: Mapped[UUID] = mapped_column(server_default=text("gen_random_uuid()"), primary_key=True)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=False), server_default=func.now(), onupdate=func.now()
    # )
    id: Mapped[str] = mapped_column(default=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self, excludes: list[str] = None) -> dict[str, Any]:
        db_obj_dict = self.__dict__.copy()
        del db_obj_dict["_sa_instance_state"]
        for exclude in excludes or []:
            del db_obj_dict[exclude]
        return db_obj_dict
