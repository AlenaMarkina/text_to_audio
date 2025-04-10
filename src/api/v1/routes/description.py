from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.description import (
    DescriptionCreateSchema, DescriptionUpdateSchema, DescriptionRetrieveSchema)
from repository.description import desc_repository

router = APIRouter()


@router.get("/")
def retrieve_all(session: Session) -> list[DescriptionRetrieveSchema]:
    """Просмотр всех описаний к достопримечательностям."""

    return desc_repository.filter(session)


@router.get("/{desc_id}")
def retrieve(session: Session, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Получение информации об описании достопримечательности."""

    description = desc_repository.get(session, id=str(desc_id))

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    return description


@router.post("/")
def create(session: Session, data: DescriptionCreateSchema) -> DescriptionRetrieveSchema:
    """Создание описания к достопримечательности."""
    is_exist = desc_repository.exists(session, desc_path=data.desc_path)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Description already exists"
        )

    data = {
        'id': str(uuid4()),
        'place_of_interest_id': str(data.place_of_interest_id),
        'desc_path': data.desc_path}

    return desc_repository.create(session, data=data)


@router.delete("/{desc_path}", status_code=status.HTTP_204_NO_CONTENT)
def delete(session: Session, desc_id: UUID) -> None:
    """Удаление описания достопримечательностям."""

    description = desc_repository.get(session, id=str(desc_id))

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    desc_repository.delete(session, description)


@router.put("/{desc_id}")
def update(session: Session, data: DescriptionUpdateSchema, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Изменение описания достопримечательности."""

    description = desc_repository.get(session, id=str(desc_id))

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    new_description = desc_repository.update(session, description, {"desc_path": data.desc_path})

    return new_description
