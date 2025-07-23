from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Landmark, Country, City
from repository.base import SQLAlchemyRepository


class LandmarkRepository(SQLAlchemyRepository[Landmark]):
    async def join(self, session: AsyncSession, landmark_id):
        query = select(Landmark.id, Landmark.landmark_name_en, City.city_name_en, Country.country_name_en).join(
            Landmark.city).join(City.country).where(Landmark.id == landmark_id)

        return (await session.execute(query)).fetchone()


landmark_repository = LandmarkRepository(Landmark)
