from models.models import Description
from repository.base import SQLAlchemyRepository


class DescriptionRepository(SQLAlchemyRepository[Description]):
    pass


audio_repository = DescriptionRepository(Description)
