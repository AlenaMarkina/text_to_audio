from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint, Numeric, SmallInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.constance import (PRECISION, SCALE, LANGUAGE, GENDER, Language, Voiceover,
                              CountryEN, CountryRU, CityEN, CityRU)
from settings.postgresql import settings

schema = settings.PG_SCHEMA


class Landmark(Base):
    __tablename__ = 'landmarks'
    __table_args__ = (
        UniqueConstraint('city_id', 'landmark_name_en'),
        {'schema': schema},
    )

    city_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.cities.id'))
    landmark_name_ru: Mapped[str] = mapped_column(String(), nullable=False)
    landmark_name_en: Mapped[str] = mapped_column(String(), nullable=False)
    lat: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
    long: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)

    images: Mapped[list['Image']] = relationship(back_populates='landmark')
    descriptions: Mapped[list['Description']] = relationship(back_populates='landmark')
    audios: Mapped[list['Audio']] = relationship(back_populates='landmark')
    city: Mapped['City'] = relationship(back_populates='landmarks')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.landmark_name_ru}, {self.landmark_name_en})'


class Image(Base):
    __tablename__ = 'images'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.landmarks.id'), nullable=False)
    image_path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)

    landmark: Mapped['Landmark'] = relationship(back_populates="images")

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.image_path})'


class Description(Base):
    __tablename__ = 'descriptions'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.landmarks.id'), nullable=False)
    desc_path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)

    audio: Mapped['Audio'] = relationship(back_populates='description')
    landmark: Mapped['Landmark'] = relationship(back_populates='descriptions')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.desc_path})'


class Audio(Base):
    __tablename__ = 'audios'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.landmarks.id'), nullable=False)
    desc_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.descriptions.id'), unique=True, nullable=False)
    audio_path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    language: Mapped[str] = mapped_column(String(LANGUAGE), server_default=Language.RU.value, nullable=False)
    voiceover: Mapped[str] = mapped_column(String(GENDER), server_default=Voiceover.MALE.value, nullable=False)

    description: Mapped['Description'] = relationship(back_populates="audio")
    landmark: Mapped['Landmark'] = relationship(back_populates='audios')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.audio_path})'


class City(Base):
    __tablename__ = 'cities'

    country_id: Mapped[UUID] = mapped_column(ForeignKey(f'{schema}.countries.id'), nullable=False)
    city_name_en: Mapped[str] = mapped_column(
        Enum(CityEN, name='cityen', values_callable=lambda x: [i.value for i in x]),
        nullable=False,
        unique=True
    )
    city_name_ru: Mapped[str] = mapped_column(
        Enum(CityRU, name='cityru', validate_strings=True, values_callable=lambda x: [i.value for i in x]),
        nullable=False,
        unique=True
    )
    lat: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
    long: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)

    landmarks: Mapped[list['Landmark']] = relationship(back_populates='city')
    country: Mapped['Country'] = relationship(back_populates='cities')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.city_name_ru}, {self.city_name_en})'


class Country(Base):
    __tablename__ = 'countries'

    country_name_en: Mapped[str] = mapped_column(
        Enum(CountryEN, name='countryen', validate_strings=True, values_callable=lambda x: [i.value for i in x]),
        nullable=False,
        unique=True
    )
    country_name_ru: Mapped[str] = mapped_column(
        Enum(CountryRU, name='countryru', validate_strings=True, values_callable=lambda x: [i.value for i in x]),
        nullable=False,
        unique=True
    )

    cities: Mapped[list['City']] = relationship(back_populates='country')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.country_name_ru}, {self.country_name_en})'
