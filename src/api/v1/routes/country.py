from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.country import CountryCreateSchema, CountryUpdateSchema, CountryRetrieveSchema
from repository.country import country_repository
from models.constance import CountryRU

router = APIRouter()


@router.get("/")
async def retrieve_all(session: Session) -> list[CountryRetrieveSchema]:
    """Просмотр всех стран."""

    return await country_repository.filter(session)


@router.get("/{city_id}")
async def retrieve(session: Session, country_id: UUID) -> CountryRetrieveSchema:
    """Получение информации о стране."""

    country = await country_repository.get(session, id=country_id)

    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    return country


@router.post("/")
async def create(session: Session, data: CountryCreateSchema) -> CountryRetrieveSchema:
    """Создание страны."""

    print('\nin create_country()')
    print(f'data: {data}')
    is_exist = await country_repository.exists(session, country_name_en=data.country_name_en)

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Country already exists"
        )

    new_data = data.model_dump()
    new_data['country_name_ru'] = CountryRU[data.country_name_en.name]
    print(f'data1111: {new_data}')

    return await country_repository.create(session, data=new_data)


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session: Session, country_id: UUID) -> None:
    """Удаление страны."""

    country = await country_repository.get(session, id=country_id)

    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    await country_repository.delete(session, country)


@router.put("/{city_id}")
async def update(
    session: Session,
    data: CountryUpdateSchema,
    city_id: UUID,
) -> CountryRetrieveSchema:
    """Изменение города."""

    city = await country_repository.get(session, id=city_id)

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    return await country_repository.update(session, city, data=data.model_dump())
