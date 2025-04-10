from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.place_of_interest import (
    PlaceOfInterestCreateSchema, PlaceOfInterestUpdateSchema, PlaceOfInterestRetrieveSchema
)
from repository.place_of_interest import place_repository

router = APIRouter()


@router.get("/")
def retrieve_all(session: Session) -> list[PlaceOfInterestRetrieveSchema]:
    """Просмотр всех достопримечательностей."""

    return place_repository.filter(session)


@router.get("/{place_id}")
def retrieve(session: Session, place_id: UUID) -> PlaceOfInterestRetrieveSchema:
    """Получение информации о достопримечательности."""

    place_of_interest = place_repository.get(session, id=str(place_id))

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    return place_of_interest


@router.post("/")
def create(session: Session, data: PlaceOfInterestCreateSchema) -> PlaceOfInterestRetrieveSchema:
    """Создание достопримечательности."""
    is_exist = place_repository.exists(session, name=data.name)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place of interest already exists"
        )

    data = {
        'id': str(uuid4()),
        'city_id': str(data.city_id),
        'name': data.name}

    return place_repository.create(session, data=data)


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(session: Session, place_id: UUID) -> None:
    """Удаление достопримечательности."""

    place_of_interest = place_repository.get(session, id=str(place_id))

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    place_repository.delete(session, place_of_interest)


@router.put("/{place_id}")
def update(
    session: Session,
    data: PlaceOfInterestUpdateSchema,
    place_id: UUID,
) -> PlaceOfInterestRetrieveSchema:
    """Изменение достопримечательности."""

    place_of_interest = place_repository.get(session, id=str(place_id))

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    new_place = place_repository.update(session, place_of_interest, {"name": data.name})

    return new_place
