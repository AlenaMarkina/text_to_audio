from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.constance import PATH_STR_LEN, NAME_STR_LEN


class PlaceOfInterest(Base):
    name: Mapped[str] = mapped_column(String(NAME_STR_LEN), nullable=False, unique=True)
    city_id: Mapped[UUID] = mapped_column(ForeignKey('city.id'))
    images: Mapped[list['Image']] = relationship(back_populates='place_of_interest')
    descriptions: Mapped[list['Description']] = relationship(back_populates='place_of_interest')
    audios: Mapped[list['Audio']] = relationship(back_populates='place_of_interest')
    city: Mapped['City'] = relationship(back_populates='place_of_interests')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.name})'


class Image(Base):
    image_path: Mapped[str] = mapped_column(String(PATH_STR_LEN), nullable=False, unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))
    place_of_interest: Mapped['PlaceOfInterest'] = relationship(back_populates="images")

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.image_path})'


class Description(Base):
    desc_path: Mapped[str] = mapped_column(String(PATH_STR_LEN), nullable=False, unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))
    audio: Mapped['Audio'] = relationship(back_populates='description')
    place_of_interest: Mapped['PlaceOfInterest'] = relationship('descriptions')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.desc_path})'


class Audio(Base):
    audio_path: Mapped[str] = mapped_column(String(PATH_STR_LEN), nullable=False, unique=True)
    description_id: Mapped[UUID] = mapped_column(ForeignKey('description.id'), unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))
    description: Mapped['Description'] = relationship(back_populates="audio")
    place_of_interest: Mapped['PlaceOfInterest'] = relationship(back_populates='audios')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.audio_path})'


class City(Base):
    name: Mapped[str] = mapped_column(String(NAME_STR_LEN), nullable=False, unique=True)
    place_of_interests: Mapped[list['PlaceOfInterest']] = relationship(back_populates='city')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.name})'
