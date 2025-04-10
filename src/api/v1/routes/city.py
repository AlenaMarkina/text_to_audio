from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.city import CityCreateSchema, CityUpdateSchema, CityRetrieveSchema
from repository.city import city_repository

router = APIRouter()


@router.get("/")
def retrieve_all(session: Session) -> list[CityRetrieveSchema]:
    """Просмотр всех городов."""

    return city_repository.filter(session)


@router.get("/{city_id}")
def retrieve(session: Session, city_id: UUID) -> CityRetrieveSchema:
    """Получение информации о городе."""

    city = city_repository.get(session, id=str(city_id))

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    return city


@router.post("/")
def create(session: Session, data: CityCreateSchema) -> CityRetrieveSchema:
    """Создание города."""
    is_exist = city_repository.exists(session, name=data.name)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists"
        )

    return city_repository.create(session, data={'id': str(uuid4()), 'name': data.name})


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(session: Session, city_id: UUID) -> None:
    """Удаление города."""

    city = city_repository.get(session, id=str(city_id))

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    city_repository.delete(session, city)


@router.put("/{city_id}")
def update(
    session: Session,
    data: CityUpdateSchema,
    city_id: UUID,
) -> CityRetrieveSchema:
    """Изменение города."""

    city = city_repository.get(session, id=str(city_id))

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    new_city = city_repository.update(session, city, {"name": data.name})

    return new_city
