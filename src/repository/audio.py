from models.models import Audio
from repository.base import SQLAlchemyRepository


class AudioRepository(SQLAlchemyRepository[Audio]):
    pass


audio_repository = AudioRepository(Audio)
