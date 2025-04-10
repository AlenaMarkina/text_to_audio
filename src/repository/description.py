from models.models import Description
from repository.base import SQLAlchemyRepository


class DescriptionRepository(SQLAlchemyRepository[Description]):
    pass


desc_repository = DescriptionRepository(Description)
