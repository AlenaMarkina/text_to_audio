from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint, Numeric, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.constance import PRECISION, SCALE, LANGUAGE, GENDER, CITY_NAME
from settings.postgresql import settings


class Landmark(Base):
    __tablename__ = 'landmarks'
    __table_args__ = (
        UniqueConstraint('city_id', 'name'),
        {'schema': settings.PG_SCHEMA},
    )

    city_id: Mapped[UUID] = mapped_column(ForeignKey(f'{settings.PG_SCHEMA}.cities.id'))
    name: Mapped[str] = mapped_column(String(), nullable=False)
    lat: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
    long: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)

    images: Mapped[list['Image']] = relationship(back_populates='landmark')
    descriptions: Mapped[list['Description']] = relationship(back_populates='landmark')
    audios: Mapped[list['Audio']] = relationship(back_populates='landmark')
    city: Mapped['City'] = relationship(back_populates='landmarks')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.name})'


class Image(Base):
    __tablename__ = 'images'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{settings.PG_SCHEMA}.landmarks.id'), nullable=False)
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)

    landmark: Mapped['Landmark'] = relationship(back_populates="images")

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.path})'


class Description(Base):
    __tablename__ = 'descriptions'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{settings.PG_SCHEMA}.landmarks.id'), nullable=False)
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)

    audio: Mapped['Audio'] = relationship(back_populates='description')
    landmark: Mapped['Landmark'] = relationship(back_populates='descriptions')

    def __str__(self):
        return f'{__class__.__name__}({self.id}, {self.path})'


class Audio(Base):
    __tablename__ = 'audios'

    landmark_id: Mapped[UUID] = mapped_column(ForeignKey(f'{settings.PG_SCHEMA}.landmarks.id'), nullable=False)
    description_id: Mapped[UUID] = mapped_column(ForeignKey(f'{settings.PG_SCHEMA}.descriptions.id'), unique=True, nullable=False)
    path: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    duration_sec: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    language: Mapped[str] = mapped_column(String(LANGUAGE), server_default='ru', nullable=False)
    voice_gender: Mapped[str] = mapped_column(String(GENDER), server_default='male', nullable=False)

    description: Mapped['Description'] = relationship(back_populates="audio")
    landmark: Mapped['Landmark'] = relationship(back_populates='audios')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.path})'


class City(Base):
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(String(CITY_NAME), nullable=False, unique=True)
    lat: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
    long: Mapped[float] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)

    landmarks: Mapped[list['Landmark']] = relationship(back_populates='city')

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.id}, {self.name})'
