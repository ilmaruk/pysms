import datetime
import random
import typing
import uuid

import transliterate

from faker import Faker
from pysms.models import Player

LOW_PROBABILITY = 1
MEDIUM_PROBABILITY = 2
HIGH_PROBABILITY = 3

MIN_AGE = 18
MAX_AGE = 35

# TODO: add country population as "weight"
nations = {
    "bul": {
        "locales": ["bg_BG"],
        "translit": "ru",
        "weight": LOW_PROBABILITY
    },
    "fra": {
        "locales": ["fr_FR"],
        "weight": HIGH_PROBABILITY
    },
    "spa": {
        "locales": ["es", "es_ES"],
        "weight": HIGH_PROBABILITY
    },
    "ita": {
        "locales": ["it_IT"],
        "weight": HIGH_PROBABILITY
    },
    "rus": {
        "locales": ["ru_RU"],
        "translit": "ru",
        "weight": MEDIUM_PROBABILITY
    },
    "swi": {
        "locales": ["it_CH", "fr_CH", "de_CH"],
        "weight": LOW_PROBABILITY
    },
    "ger": {
        "locales": ["de", "de_DE"],
        "weight": HIGH_PROBABILITY
    },
    "ukr": {
        "locales": ["uk_UA"],
        "translit": "ru",
        "weight": MEDIUM_PROBABILITY
    }
}


def allowed_locales() -> typing.List[str]:
    """Extracts the list of available locales
    from the list of available nations.
    """
    locales = set([])
    for nation in nations.values():
        locales.update(nation["locales"])
    return list(locales)


fake = Faker(allowed_locales())


def create_player() -> Player:
    """Create a new player.
    """
    name, nationality, dob = random_bio()
    args = {
        "id": uuid.uuid4(),
        "name": name,
        "nationality": nationality,
        "dob": dob
    }
    return Player(**args)


def random_bio() -> typing.Tuple[str, str, datetime.datetime]:
    """Selects a nationality and generates a random name.
    """
    nation = random_nation()
    locale = random.choice(nations[nation]["locales"])

    # Not using name_male() to avoid titles.
    name = fake[locale].first_name_male() + " " + fake[locale].last_name_male()

    # Transliterates the name, if necessary
    translit_from = nations[nation].get("translit")
    if translit_from:
        name = transliterate.translit(name, translit_from, reversed=True)

    dob = random_dob(MIN_AGE, MAX_AGE)

    return name, nation, dob


def random_nation() -> str:
    """Selects a random nation, using weights, if available.
    """
    values = list(nations.keys())
    weights = [nation.get("weight", 1) for nation in nations.values()]
    return random.choices(values, weights=weights, k=1)[0]


def random_dob(min_age: int, max_age: int) -> datetime.date:
    age = random.randint(MIN_AGE, MAX_AGE)
    return (datetime.date.today() - datetime.timedelta(days=365*(age-1)) -
            datetime.timedelta(days=random.randint(0, 366)))
