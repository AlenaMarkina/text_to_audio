from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.image import ImageCreateSchema, ImageRetrieveSchema, ImageUpdateSchema
from repository.image import image_repository
from repository.landmark import landmark_repository

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[ImageRetrieveSchema]:
    """Просмотр всех фотографий к достопримечательностям."""

    return await image_repository.filter(session)


@router.get("/{image_id}")
async def retrieve(session: Session, image_id: UUID) -> ImageRetrieveSchema:
    """Получение информации о фотографии к достопримечательности."""

    image = await image_repository.get(session, id=image_id)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return image


@router.post("/")
async def create(session: Session, data: ImageCreateSchema) -> ImageRetrieveSchema:
    """Создание фотографии к достопримечательности."""

    is_landmark_exist = await landmark_repository.exists(session, id=data.landmark_id)

    if not is_landmark_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Landmark with given id does not exist"
        )

    is_image_exist = await image_repository.exists(session, path=data.path)

    if is_image_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Image already exists"
        )

    return await image_repository.create(session, data=data.model_dump())


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, image_id: UUID) -> None:
    """Удаление фотографии к достопримечательности."""

    image = await image_repository.get(session, id=image_id)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    await image_repository.delete(session, image)


@router.put("/{image_id}")
async def update(session: Session, data: ImageUpdateSchema, image_id: UUID) -> ImageRetrieveSchema:
    """Изменение фотографии к достопримечательности."""

    image = await image_repository.get(session, id=image_id)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return await image_repository.update(session, image, data=data.model_dump())
