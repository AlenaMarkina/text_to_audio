from uuid import UUID

from sqlalchemy import ForeignKey, String, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
# from models.constance import PATH_STR_LEN, NAME_STR_LEN


class PlaceOfInterest(Base):
    __table_args__ = (UniqueConstraint('city_id', 'name'), )

    name: Mapped[str] = mapped_column(String(), nullable=False)
    lat: Mapped[float] = mapped_column(Float(), nullable=False)
    long: Mapped[float] = mapped_column(Float(), nullable=False)
    city_id: Mapped[UUID] = mapped_column(ForeignKey('city.id'))

    images: Mapped[list['Image']] = relationship(back_populates='place_of_interest')
    descriptions: Mapped[list['Description']] = relationship(back_populates='place_of_interest')
    audios: Mapped[list['Audio']] = relationship(back_populates='place_of_interest')
    city: Mapped['City'] = relationship(back_populates='place_of_interests')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.name})'


class Image(Base):
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))

    place_of_interest: Mapped['PlaceOfInterest'] = relationship(back_populates="images")

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.path})'


class Description(Base):
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))

    audio: Mapped['Audio'] = relationship(back_populates='description')
    place_of_interest: Mapped['PlaceOfInterest'] = relationship(back_populates='descriptions')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.path})'


class Audio(Base):
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    place_of_interest_id: Mapped[UUID] = mapped_column(ForeignKey('placeofinterest.id'))
    description_id: Mapped[UUID] = mapped_column(ForeignKey('description.id'), unique=True)
    lang: Mapped[str] = mapped_column(String(), server_default='ru')
    gender: Mapped[str] = mapped_column(String(), server_default='male')

    description: Mapped['Description'] = relationship(back_populates="audio")
    place_of_interest: Mapped['PlaceOfInterest'] = relationship(back_populates='audios')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.path})'


class City(Base):
    name: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    place_of_interests: Mapped[list['PlaceOfInterest']] = relationship(back_populates='city')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.name})'
