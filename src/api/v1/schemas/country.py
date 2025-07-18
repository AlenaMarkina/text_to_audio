from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base
from models.constance import CountryEN, CountryRU


class CountryBaseSchema(Base):
    country_name_en: CountryEN


class CountryCreateSchema(CountryBaseSchema):
    pass


class CountryUpdateSchema(CountryBaseSchema):
    pass


class CountryRetrieveSchema(CountryBaseSchema):
    country_name_ru: CountryRU
    created_at: datetime
    updated_at: datetime
    id: UUID
