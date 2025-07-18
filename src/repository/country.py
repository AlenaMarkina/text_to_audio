from models.models import Country
from repository.base import SQLAlchemyRepository


class CountryRepository(SQLAlchemyRepository[Country]):
    pass


country_repository = CountryRepository(Country)
