from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.audio import AudioRetrieveSchema
from repository.audio import audio_repository

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[AudioRetrieveSchema]:
    """Просмотр всех аудиозаписей."""

    return await audio_repository.filter(session)


@router.get("/{audio_id}")
async def retrieve(session: Session, audio_id: UUID) -> AudioRetrieveSchema:
    """Получение информации об аудиозаписи."""

    audio = await audio_repository.get(session, id=audio_id)

    if audio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")

    return audio


@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, audio_id: UUID) -> None:
    """Удаление аудиозаписи."""

    audio = await audio_repository.get(session, id=audio_id)

    if audio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")

    await audio_repository.delete(session, audio)


# @router.put("/{audio_id}")
# async def update(session: Session, data: DescriptionUpdateSchema, desc_id: UUID) -> DescriptionRetrieveSchema:
#     """Изменение аудиозаписи."""
#
#     description = await audio_repository.get(session, id=desc_id)
#
#     if description is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
#
#     data = {"desc_path": data.desc_path}
#
#     return await audio_repository.update(session, description, data=data)
