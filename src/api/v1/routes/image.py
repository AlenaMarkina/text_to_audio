from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.image import ImageCreateSchema, ImageRetrieveSchema, ImageUpdateSchema
from repository.image import image_repository

router = APIRouter()


@router.get("/")
def retrieve_all(session: Session) -> list[ImageRetrieveSchema]:
    """Просмотр всех фотографий с достопримечательностями."""

    return image_repository.filter(session)


@router.get("/{image_id}")
def retrieve(session: Session, image_id: UUID) -> ImageRetrieveSchema:
    """Получение информации о фотографии с достопримечательностью."""

    image = image_repository.get(session, id=str(image_id))

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return image


@router.post("/")
def create(session: Session, data: ImageCreateSchema) -> ImageRetrieveSchema:
    """Создание фотографии с достопримечательностью."""
    is_exist = image_repository.exists(session, image_path=data.image_path)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Image already exists"
        )

    data = {
        'id': str(uuid4()),
        'place_of_interest_id': str(data.place_of_interest_id),
        'image_path': data.image_path}

    return image_repository.create(session, data=data)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(session: Session, image_id: UUID) -> None:
    """Удаление фотографии с достопримечательностью."""

    image = image_repository.get(session, id=str(image_id))

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    image_repository.delete(session, image)


@router.put("/{image_id}")
def update(session: Session, data: ImageUpdateSchema, image_id: UUID) -> ImageRetrieveSchema:
    """Изменение фотографии с достопримечательностью."""

    image = image_repository.get(session, id=str(image_id))

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    new_image = image_repository.update(session, image, {"image_path": data.image_path})

    return new_image
