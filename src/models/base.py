from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    registry
)

from src.models.constance import ID_LEN

mapper_registry = registry()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), onupdate=func.now()
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
