from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class PlaceOfInterestBaseSchema(Base):
    name: str
    city_id: UUID


class PlaceOfInterestCreateSchema(PlaceOfInterestBaseSchema):
    pass


class PlaceOfInterestUpdateSchema(PlaceOfInterestBaseSchema):
    pass


class PlaceOfInterestRetrieveSchema(PlaceOfInterestBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
