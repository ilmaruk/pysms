import datetime
import random
import typing
import uuid

import transliterate

from faker import Faker
from pysms.models import Player

# TODO: add country population as "weight"
nations = {
    "bul": {
        "locales": ["bg_BG"],
        "translit": "ru"
    },
    "fra": {
        "locales": ["fr_FR"]
    },
    "spa": {
        "locales": ["es_ES"]
    },
    "ita": {
        "locales": ["it_IT"]
    },
    "rus": {
        "locales": ["ru_RU"],
        "translit": "ru"
    },
    "ukr": {
        "locales": ["uk_UA"],
        "translit": "ru"
    }
}


def allowed_locales() -> typing.List[str]:
    """Extracts the list of available locales
    from the list of available nations.
    """
    locales = set([])
    for nation in nations.values():
        locales.add(*nation["locales"])
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

    # DOB
    age = random.randint(16, 35)
    dob = datetime.date.today() - datetime.timedelta(days=365*(age-1)) - \
        datetime.timedelta(days=random.randint(0, 366))

    return name, nation, dob


def random_nation() -> str:
    """Selects a random nation, using weights, if available.
    """
    values = list(nations.keys())
    weights = [nation.get("weight", 1) for nation in nations.values()]
    return random.choices(values, weights=weights, k=1)[0]
