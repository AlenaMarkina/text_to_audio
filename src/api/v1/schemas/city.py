from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class CityBaseSchema(Base):
    name: str


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    pass


class CityRetrieveSchema(CityBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
