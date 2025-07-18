from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base
from models.constance import Language, Voiceover


class AudioBaseSchema(Base):
    landmark_id: UUID
    desc_id: UUID
    audio_path: str
    duration_sec: int
    language: Language
    voice_gender: Voiceover


# class AudioUpdateSchema(AudioBaseSchema):
#     pass


class AudioRetrieveSchema(AudioBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
