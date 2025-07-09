from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class PlaceOfInterestBaseSchema(Base):
    name: str
    city_id: str


class PlaceOfInterestCreateSchema(PlaceOfInterestBaseSchema):
    pass


class PlaceOfInterestUpdateSchema(PlaceOfInterestBaseSchema):
    lat: float | None
    long: float | None


class PlaceOfInterestRetrieveSchema(PlaceOfInterestBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
