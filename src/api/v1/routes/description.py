from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.description import (
    DescriptionCreateSchema, DescriptionUpdateSchema, DescriptionRetrieveSchema)
from repository.description import desc_repository
from repository.place_of_interest import place_repository
from repository.audio import audio_repository
from services.convert_text_to_audio import TextConvertor

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[DescriptionRetrieveSchema]:
    """Просмотр всех описаний к достопримечательностям."""

    return await desc_repository.filter(session)


@router.get("/{desc_id}")
async def retrieve(session: Session, desc_id: str) -> DescriptionRetrieveSchema:
    """Получение информации об описании достопримечательности."""

    description = await desc_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    return description


@router.post("/")
async def create(session: Session, data: DescriptionCreateSchema) -> DescriptionRetrieveSchema:
    """Создание описания к достопримечательности."""
    # TODO: Подумать как правильно обработать ошибку:
    #  если описание создано, но при конвертации в аудио и ее сохр произошла ошибка.
    #  Аудио в этом случае не сохр в папку и в бд. А при повторном запросе выдает ошибку 409!!!!!
    is_exist = await desc_repository.exists(session, path=data.path)

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
    desc = await desc_repository.create(session, data=desc_data)

    convertor = TextConvertor(text_path=desc.path)
    await convertor.init_voice()
    await convertor.set_audiopath_from_textpath()
    await convertor.read_text_file()
    if not await convertor.convert_text_to_audio():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,)

    audio_data = {
        'place_of_interest_id': data.place_of_interest_id,
        'description_id': desc.id,
        'path': convertor.audio_path
    }
    await audio_repository.create(session, data=audio_data)
    return desc


@router.delete("/{desc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, desc_id: str) -> None:
    """Удаление описания достопримечательностям."""

    description = await desc_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    await desc_repository.delete(session, description)


@router.put("/{desc_id}")
async def update(session: Session, data: DescriptionUpdateSchema, desc_id: str) -> DescriptionRetrieveSchema:
    """Изменение описания достопримечательности."""

    description = await desc_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    data = {"path": data.path}

    return await desc_repository.update(session, description, data=data)

    #TODO: добавить изменение в аудиозаписи!!!!!!!
