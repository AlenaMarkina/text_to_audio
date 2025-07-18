from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class LandmarkBaseSchema(Base):
    city_id: UUID
    landmark_name_en: str
    landmark_name_ru: str
    lat: float
    long: float


class LandmarkCreateSchema(LandmarkBaseSchema):
    pass


class LandmarkUpdateSchema(LandmarkBaseSchema):
    pass


class LandmarkRetrieveSchema(LandmarkBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
