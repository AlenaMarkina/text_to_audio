from enum import Enum
from dataclasses import dataclass

PRECISION = 9
SCALE = 6

LANGUAGE = 2
GENDER = 6

CITY_NAME = 100


class CountryEN(Enum):
    RUSSIA = 'Russia'
    GERMANY = 'Germany'
    PORTUGAL = 'Portugal'


class CountryRU(Enum):
    RUSSIA = 'Россия'
    GERMANY = 'Германия'
    PORTUGAL = 'Португалия'


class CityEN(Enum):
    MOSCOW = 'Moscow'
    LISBON = 'Lisbon'
    LUDWIGSBURG = 'Ludwigsburg'


class CityRU(Enum):
    MOSCOW = 'Москва'
    LISBON = 'Лиссабон'
    LUDWIGSBURG = 'Людвигсбург'


class Language(Enum):
    RU = 'ru'


class Voiceover(Enum):
    MALE = 'male'


@dataclass
class Name:
    ru: str
    en: str


class Country(Enum):
    RUSSIA = Name(ru='Россия', en='Russia')
    GERMANY = Name(ru='Германия', en='Germany')
