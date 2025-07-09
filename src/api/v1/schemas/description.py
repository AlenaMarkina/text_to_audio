from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class DescriptionBaseSchema(Base):
    path: str
    place_of_interest_id: str


class DescriptionCreateSchema(DescriptionBaseSchema):
    pass


class DescriptionUpdateSchema(DescriptionBaseSchema):
    pass


class DescriptionRetrieveSchema(DescriptionBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
