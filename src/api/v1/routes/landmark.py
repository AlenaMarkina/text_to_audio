from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.landmark import LandmarkCreateSchema, LandmarkUpdateSchema, LandmarkRetrieveSchema
from repository.landmark import landmark_repository
from repository.city import city_repository

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[LandmarkRetrieveSchema]:
    """Просмотр всех достопримечательностей."""

    return await landmark_repository.filter(session)


@router.get("/{landmark_id}")
async def retrieve(session: Session, landmark_id: UUID) -> LandmarkRetrieveSchema:
    """Получение информации о достопримечательности."""

    landmark = await landmark_repository.get(session, id=landmark_id)

    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")

    return landmark


@router.post("/")
async def create(session: Session, data: LandmarkCreateSchema) -> LandmarkRetrieveSchema:
    """Создание достопримечательности."""

    is_city_exist = await city_repository.exists(session, id=data.city_id)

    if not is_city_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with given id does not exist"
        )

    is_landmark_exist = await landmark_repository.exists(
        session,
        city_id=data.city_id,
        landmark_name_en=data.landmark_name_en
    )

    if is_landmark_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Landmark already exists"
        )

    return await landmark_repository.create(session, data=data.model_dump())


@router.delete("/{landmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, landmark_id: UUID) -> None:
    """Удаление достопримечательности."""

    landmark = await landmark_repository.get(session, id=landmark_id)

    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")

    await landmark_repository.delete(session, landmark)


@router.put("/{landmark_id}")
async def update(
    session: Session,
    data: LandmarkUpdateSchema,
    landmark_id: UUID,
) -> LandmarkRetrieveSchema:
    """Изменение достопримечательности."""

    landmark = await landmark_repository.get(session, id=landmark_id)

    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")

    return await landmark_repository.update(session, landmark, data=data.model_dump())
