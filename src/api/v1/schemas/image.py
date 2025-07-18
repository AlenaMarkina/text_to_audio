from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class ImageBaseSchema(Base):
    landmark_id: UUID
    image_path: str


class ImageCreateSchema(ImageBaseSchema):
    pass


class ImageUpdateSchema(ImageBaseSchema):
    pass


class ImageRetrieveSchema(ImageBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
