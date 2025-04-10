from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import Base

T = TypeVar("T", bound=Base)


class SQLAlchemyRepository[T]:
    def __init__(self, model: type[T]) -> None:
        self._model = model

    def exists(self, session: Session, **attrs) -> bool:
        query = select(self._model).filter_by(**attrs)

        return (session.execute(query)).scalars().first() is not None

    def get(
        self, session: Session, options: Any | None = None, **attrs
    ) -> T | None:
        query = select(self._model).filter_by(**attrs)
        if options is not None:
            if isinstance(options, list):
                for option in options:
                    query = query.options(option)
            else:
                query = query.options(options)

        return (session.execute(query)).scalars().first()

    def filter(
        self, session: Session, options: Any | None = None, **attrs
    ) -> list[T]:
        query = select(self._model).filter_by(**attrs)

        if options is not None:
            if isinstance(options, list):
                for option in options:
                    query = query.options(option)
            else:
                query = query.options(options)

        return (session.execute(query)).scalars().all()

    def create(
        self, session: Session, data: dict[str, Any], commit: bool = True
    ) -> T:
        obj = self._model(**data)
        session.add(obj)
        session.flush()

        if commit:
            session.commit()

        return obj

    def update(
        self,
        session: Session,
        obj: T,
        data: dict[str, Any],
        commit: bool = True,
    ) -> T:
        for key, value in data.items():
            setattr(obj, key, value)
        session.flush()

        if commit:
            session.commit()

        return obj

    def delete(self, session: Session, obj: T, commit: bool = True) -> None:
        session.delete(obj)
        session.flush()

        if commit:
            session.commit()
