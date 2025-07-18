from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class DescriptionBaseSchema(Base):
    landmark_id: UUID
    desc_path: str


class DescriptionCreateSchema(DescriptionBaseSchema):
    pass


class DescriptionUpdateSchema(DescriptionBaseSchema):
    pass


class DescriptionRetrieveSchema(DescriptionBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
