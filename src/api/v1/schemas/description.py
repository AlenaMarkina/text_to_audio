from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class DescriptionBaseSchema(Base):
    landmark_id: UUID


class DescriptionCreateSchema(DescriptionBaseSchema):
    landmark_description: str


class DescriptionUpdateSchema(DescriptionBaseSchema):
    landmark_description: str


class DescriptionRetrieveSchema(DescriptionBaseSchema):
    id: UUID
    desc_path: str
    created_at: datetime
    updated_at: datetime
