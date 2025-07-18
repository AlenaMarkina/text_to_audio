from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base
from models.constance import CityRU, CityEN


class CityBaseSchema(Base):
    country_id: UUID
    lat: float
    long: float
    city_name_en: CityEN


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    pass


class CityRetrieveSchema(CityBaseSchema):
    city_name_ru: CityRU
    created_at: datetime
    updated_at: datetime
    id: UUID
