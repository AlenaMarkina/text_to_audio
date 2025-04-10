from models.models import City
from repository.base import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository[City]):
    pass


city_repository = CityRepository(City)
