from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.description import (
    DescriptionCreateSchema, DescriptionUpdateSchema, DescriptionRetrieveSchema)
from repository.description import audio_repository
from repository.audio import audio_repository
from repository.place_of_interest import place_repository
from repository.audio import audio_repository
from services.convert_text_to_audio import TextConvertor

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[DescriptionRetrieveSchema]:
    """Просмотр всех описаний к достопримечательностям."""

    return await audio_repository.filter(session)


@router.get("/{desc_id}")
async def retrieve(session: Session, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Получение информации об описании достопримечательности."""

    description = await audio_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    return description


@router.post("/")
async def create(session: Session, data: DescriptionCreateSchema) -> DescriptionRetrieveSchema:
    """Создание описания к достопримечательности."""
    is_exist = await audio_repository.exists(session, path=data.path)

    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Description already exists")

    is_place_exist = await place_repository.exists(session, id=data.place_of_interest_id)

    if not is_place_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Place_of_interest with given id does not exist"
        )

    desc_data = {
        'place_of_interest_id': data.place_of_interest_id,
        'path': data.path
    }
    desc = await audio_repository.create(session, data=desc_data)
    # desc = await desc_repository.get(session, path=desc_data.path)

    # TODO: добавить автоматическую генерацию аудио и сохр ее в бд

    convertor = TextConvertor(text_path=desc.path)  # "./statics/text/portugal/lisbon/st_georges_castle333.docx",
    await convertor.init_voice()
    await convertor.set_audiopath_from_textpath()
    await convertor.read_text_file()
    await convertor.convert_text_to_audio()

    audio_data = {
        'place_of_interest_id': data.place_of_interest_id,
        'description_id': desc.id,
        'path': convertor.audio_path
    }
    await audio_repository.create(session, data=audio_data)
    return desc


@router.delete("/{desc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, desc_id: UUID) -> None:
    """Удаление описания достопримечательностям."""

    description = await audio_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    await audio_repository.delete(session, description)


@router.put("/{desc_id}")
async def update(session: Session, data: DescriptionUpdateSchema, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Изменение описания достопримечательности."""

    description = await audio_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    data = {"desc_path": data.desc_path}

    return await audio_repository.update(session, description, data=data)

    #TODO: добавить изменение в аудиозаписи!!!!!!!
