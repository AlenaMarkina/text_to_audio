from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class AudioBaseSchema(Base):
    path: str
    place_of_interest_id: str
    description_id: str
    lang: str
    gender: str


# class AudioUpdateSchema(AudioBaseSchema):
#     pass


class AudioRetrieveSchema(AudioBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
