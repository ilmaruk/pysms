import datetime
import random
import typing
import uuid
from pysms.models.player import PlayerPosition, PlayerSide

import pydantic
import transliterate
from faker import Faker

from pysms.utils import rand
from pysms.models import Player

LOW_PROBABILITY = 1
MEDIUM_PROBABILITY = 2
HIGH_PROBABILITY = 3


class PlayerCreateConfig(pydantic.BaseSettings):
    MIN_AGE: int = 16
    MAX_AGE: int = 30
    AVG_MAIN_SKILL: int = 14
    AVG_MEDIUM_SKILL: int = 11
    AVG_SECONDARY_SKILL: int = 7
    AVG_STAMINA: int = 60
    AVG_AGGRESSION: int = 30

    class Config:
        env_prefix: str = "PYSMS_"


nations = {
    "bul": {
        "locales": ["bg_BG"],
        "translit": "ru",
        "weight": LOW_PROBABILITY
    },
    "bra": {
        "locales": ["pt_BR"],
        "weight": HIGH_PROBABILITY
    },
    "por": {
        "locales": ["pt_PT"],
        "weight": HIGH_PROBABILITY
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


def create_player(config: PlayerCreateConfig, position: PlayerPosition) -> Player:
    """Create a new player.
    """
    name, nationality, dob = random_bio(config.MIN_AGE, config.MIN_AGE)
    st, tk, ps, sh = random_skills(
        position, config.AVG_MAIN_SKILL, config.AVG_MEDIUM_SKILL, config.AVG_SECONDARY_SKILL)
    args = {
        "id": uuid.uuid4(),
        "name": name,
        "nationality": nationality,
        "dob": dob,
        "position": position,
        "side": random_side(),
        "stopping": st,
        "tackling": tk,
        "passing": ps,
        "shooting": sh,
        "stamina": round(rand.bounded_gauss(config.AVG_STAMINA, config.AVG_STAMINA/2)),
        "aggression": round(rand.bounded_gauss(config.AVG_AGGRESSION, config.AVG_AGGRESSION/3)),
    }
    return Player(**args)


def random_bio(min_age: int, max_age: int) -> typing.Tuple[str, str, datetime.datetime]:
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

    dob = random_dob(min_age, max_age)

    return name, nation, dob


def random_nation() -> str:
    """Selects a random nation, using weights, if available.
    """
    values = list(nations.keys())
    weights = [nation.get("weight", 1) for nation in nations.values()]
    return random.choices(values, weights=weights, k=1)[0]


def random_dob(min_age: int, max_age: int) -> datetime.date:
    mu = (min_age + max_age) / 2
    sigma = (min_age + max_age) / 2
    age = round(rand.bounded_gauss(mu, sigma))
    return (datetime.date.today() - datetime.timedelta(days=365*(age-1)) -
            datetime.timedelta(days=random.randint(0, 366)))


def random_side() -> PlayerSide:
    sides: typing.List[PlayerSide] = [
        PlayerSide.RIGHT, PlayerSide.LEFT, PlayerSide.CENTRE,
        PlayerSide.RIGHT_CENTRE, PlayerSide.RIGHT_LEFT, PlayerSide.LEFT_CENTRE,
        PlayerSide.ANY
    ]
    weights = [40, 30, 48, 10, 10, 5, 9]
    return random.choices(sides, weights, k=1)[0]


def random_skills(position: PlayerPosition, main_skill: int, medium_skill: int, secondary_skill: int) -> typing.Tuple[int, int, int, int]:
    low_skill = secondary_skill / 2
    values = {
        PlayerPosition.GOALKEEPER: {
            "st": (main_skill, 3),
            "tk": (low_skill, 2),
            "ps": (low_skill, 2),
            "sh": (low_skill, 2),
        },
        PlayerPosition.DEFENDER: {
            "st": (low_skill, 2),
            "tk": (main_skill, 3),
            "ps": (secondary_skill, 2),
            "sh": (secondary_skill, 2),
        },
        PlayerPosition.DEFENDING_MIDFIELDER: {
            "st": (low_skill, 2),
            "tk": (medium_skill, 3),
            "ps": (medium_skill, 3),
            "sh": (secondary_skill, 2),
        },
        PlayerPosition.MIDFIELDER: {
            "st": (low_skill, 2),
            "tk": (secondary_skill, 2),
            "ps": (main_skill, 3),
            "sh": (secondary_skill, 2),
        },
        PlayerPosition.ATTACKING_MIDFIELDER: {
            "st": (low_skill, 2),
            "tk": (secondary_skill, 2),
            "ps": (medium_skill, 3),
            "sh": (medium_skill, 3),
        },
        PlayerPosition.FORWARD: {
            "st": (low_skill, 2),
            "tk": (secondary_skill, 2),
            "ps": (secondary_skill, 2),
            "sh": (main_skill, 3),
        },
    }

    def random_skill(skill: int, factor: int) -> int:
        return round(rand.bounded_gauss(skill, skill / factor))

    st = random_skill(*values[position]["st"])
    tk = random_skill(*values[position]["tk"])
    ps = random_skill(*values[position]["ps"])
    sh = random_skill(*values[position]["sh"])
    return st, tk, ps, sh
