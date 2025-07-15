from models.models import Landmark
from repository.base import SQLAlchemyRepository


class LandmarkRepository(SQLAlchemyRepository[Landmark]):
    pass


landmark_repository = LandmarkRepository(Landmark)
