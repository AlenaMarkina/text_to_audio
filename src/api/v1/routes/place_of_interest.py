from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.place_of_interest import (
    PlaceOfInterestCreateSchema, PlaceOfInterestUpdateSchema, PlaceOfInterestRetrieveSchema
)
from repository.place_of_interest import place_repository
from repository.city import city_repository

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[PlaceOfInterestRetrieveSchema]:
    """Просмотр всех достопримечательностей."""

    return await place_repository.filter(session)


@router.get("/{place_id}")
async def retrieve(session: Session, place_id: str) -> PlaceOfInterestRetrieveSchema:
    """Получение информации о достопримечательности."""

    place_of_interest = await place_repository.get(session, id=place_id)

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    return place_of_interest


@router.post("/")
async def create(session: Session, data: PlaceOfInterestCreateSchema) -> PlaceOfInterestRetrieveSchema:
    """Создание достопримечательности."""
    is_exist = await place_repository.exists(session, name=data.name)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place of interest already exists"
        )

    is_city_exist = await city_repository.exists(session, id=data.city_id)

    if not is_city_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with given id does not exist"
        )

    data = {
        'city_id': data.city_id,
        'name': data.name
    }

    return await place_repository.create(session, data=data)


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, place_id: str) -> None:
    """Удаление достопримечательности."""

    place_of_interest = await place_repository.get(session, id=place_id)

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    await place_repository.delete(session, place_of_interest)


@router.put("/{place_id}")
async def update(
    session: Session,
    data: PlaceOfInterestUpdateSchema,
    place_id: str,
) -> PlaceOfInterestRetrieveSchema:
    """Изменение достопримечательности."""

    place_of_interest = await place_repository.get(session, id=place_id)

    if place_of_interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place of interest not found")

    data = {"name": data.name, 'lat': data.lat, 'long': data.long}

    return await place_repository.update(session, place_of_interest, data=data)
