from models.models import PlaceOfInterest
from repository.base import SQLAlchemyRepository


class PlaceOfInterestRepository(SQLAlchemyRepository[PlaceOfInterest]):
    pass


place_repository = PlaceOfInterestRepository(PlaceOfInterest)
