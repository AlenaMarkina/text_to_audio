import asyncio
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import selectinload

from api.v1.deps.session import Session
from api.v1.schemas.city import CityCreateSchema, CityUpdateSchema, CityRetrieveSchema
from repository.city import city_repository
from models.models import City

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[CityRetrieveSchema]:
    """Просмотр всех городов."""

    return await city_repository.filter(session)


@router.get("/{city_id}")
async def retrieve(session: Session, city_id: UUID) -> CityRetrieveSchema:
    """Получение информации о городе."""

    city = await city_repository.get(session, id=city_id)

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    return city


@router.post("/")
async def create(session: Session, data: CityCreateSchema) -> CityRetrieveSchema:
    """Создание города."""
    is_exist = await city_repository.exists(session, name=data.name)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists"
        )

    data = {'name': data.name}

    return await city_repository.create(session, data=data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, city_id: UUID) -> None:
    """Удаление города."""

    city = await city_repository.get(session, id=city_id)

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    await city_repository.delete(session, city)


@router.put("/{city_id}")
async def update(
    session: Session,
    data: CityUpdateSchema,
    city_id: UUID,
) -> CityRetrieveSchema:
    """Изменение города."""

    city = await city_repository.get(session, id=city_id)

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    data = {"name": data.name}

    return await city_repository.update(session, city, data=data)
