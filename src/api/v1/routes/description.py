from uuid import UUID

from sqlalchemy.exc import ProgrammingError, PendingRollbackError, DatabaseError
from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.description import (
    DescriptionCreateSchema, DescriptionUpdateSchema, DescriptionRetrieveSchema)
from repository.description import desc_repository
from repository.landmark import landmark_repository
from repository.audio import audio_repository
from services.convert_text_to_audio import TextConvertor
from services.description_service import TextToAudioService

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[DescriptionRetrieveSchema]:
    """Просмотр всех описаний к достопримечательностям."""

    return await desc_repository.filter(session)


@router.get("/{desc_id}")
async def retrieve(session: Session, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Получение информации об описании достопримечательности."""

    description = await desc_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    return description


@router.post("/")
async def create(session: Session, data: DescriptionCreateSchema):
    """Создание описания к достопримечательности."""
    # TODO: Подумать как правильно обработать ошибку:
    #  если описание создано, но при конвертации в аудио и ее сохр произошла ошибка.
    #  Аудио в этом случае не сохр в папку и в бд. А при повторном запросе выдает ошибку 409!!!!!

    print('\nin create_description()')

    is_landmark_exist = await landmark_repository.exists(session, id=data.landmark_id)

    if not is_landmark_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Landmark with given id does not exist"
        )

    landmark_info = await landmark_repository.join(session, landmark_id=data.landmark_id)
    print(f'join: {landmark_info}\n')

    print(f'text: \n{data.landmark_description!r}')

    tts = TextToAudioService(
        country=landmark_info[3].value,
        city=landmark_info[2].value,
        landmark_name=landmark_info[1],
        landmark_description=data.landmark_description
    )
    await tts.worker()

    is_desc_exist = await desc_repository.exists(session, desc_path=tts.desc.rel_path)

    if is_desc_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Description already exists")

    desc_data = {
        'landmark_id': data.landmark_id,
        'desc_path': tts.desc.rel_path
    }
    desc = await desc_repository.create(session, data=desc_data)
    print(f'DESCRIPTION CREATED ID: {desc.id}')
    _id = desc.id

    audio_data = {
        'landmark_id': data.landmark_id,
        'desc_id': desc.id,
        'audio_path': tts.audio.rel_path,
        'duration_sec': tts.audio.duration_sec
    }
    await audio_repository.create(session, data=audio_data)
    print(f'AUDIO CREATED ID')

    return desc


@router.delete("/{desc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, desc_id: UUID) -> None:
    """Удаление описания достопримечательностям."""

    description = await desc_repository.get(session, id=desc_id)

    if description is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")

    await desc_repository.delete(session, description)


@router.put("/{desc_id}")
async def update(session: Session, data: DescriptionUpdateSchema, desc_id: UUID) -> DescriptionRetrieveSchema:
    """Изменение описания достопримечательности и автоматически обновление аудио файла"""

    # description = await desc_repository.get(session, id=desc_id)
    #
    # if description is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
    #
    # data = {"path": data.path}
    #
    # return await desc_repository.update(session, description, data=data)

    #TODO: добавить изменение в аудиозаписи!!!!!!!

    pass
