from models.models import Landmark
from repository.base import SQLAlchemyRepository


class PlaceOfInterestRepository(SQLAlchemyRepository[Landmark]):
    pass


place_repository = PlaceOfInterestRepository(Landmark)
