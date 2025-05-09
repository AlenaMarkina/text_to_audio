from models.models import Image
from repository.base import SQLAlchemyRepository


class ImageRepository(SQLAlchemyRepository[Image]):
    pass


image_repository = ImageRepository(Image)
