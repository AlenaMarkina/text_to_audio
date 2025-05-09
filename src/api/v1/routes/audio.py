from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.audio import AudioRetrieveSchema
from repository.description import audio_repository
from repository.audio import audio_repository
from repository.place_of_interest import place_repository
from repository.audio import audio_repository
from services.convert_text_to_audio import TextConvertor

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[AudioRetrieveSchema]:
    """Просмотр всех описаний к аудиозаписям."""

    return await audio_repository.filter(session)


@router.get("/{audio_id}")
async def retrieve(session: Session, audio_id: UUID) -> AudioRetrieveSchema:
    """Получение информации об описании аудиозаписи."""

    audio = await audio_repository.get(session, id=audio_id)

    if audio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")

    return audio


@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, audio_id: UUID) -> None:
    """Удаление описания аудиозаписи."""

    audio = await audio_repository.get(session, id=audio_id)

    if audio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")

    await audio_repository.delete(session, audio)


# @router.put("/{audio_id}")
# async def update(session: Session, data: DescriptionUpdateSchema, desc_id: UUID) -> DescriptionRetrieveSchema:
#     """Изменение описания достопримечательности."""
#
#     description = await audio_repository.get(session, id=desc_id)
#
#     if description is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
#
#     data = {"desc_path": data.desc_path}
#
#     return await audio_repository.update(session, description, data=data)
