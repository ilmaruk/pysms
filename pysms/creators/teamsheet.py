import typing
from urllib.parse import scheme_chars

from pysms.models import Teamsheet, Roster, Player, Formation, ALLOWED_FORMATIONS
from pysms.models.player import PlayerPosition

MAX_SUBS = 7


def create_teamsheet(roster: Roster) -> Teamsheet:
    field_players, formation = choose_formation(roster.players, ALLOWED_FORMATIONS)
    bench_players: typing.List[Player] = []
    return Teamsheet(team=roster.team, formation=formation, field=field_players, bench=bench_players)


def choose_formation(players: typing.List[Player], formations: typing.List[Formation]) -> typing.Tuple[typing.List[Player], Formation]:
    best_players: typing.List[Player] = []
    best_formation: Formation
    best_value = -1
    for formation in formations:
        pls, value = pick_with_schema(players, formation)
        if value > best_value:
            best_value = value
            best_players = pls
            best_formation = formation

    return best_players, best_formation


def pick_with_schema(players: typing.List[Player], formation: Formation) -> typing.Tuple[typing.List[Player], int]:
    """Picks the best formation for a given schema.
    """
    pls: typing.List[Player] = []
    value = 0

    # Ignore injured and suspended players
    available = [p for p in players if not (p.stats.injury or p.stats.suspension)]

    # Goalkeeper (always 1)
    subset, val = extract_players(available, 1, (3, 1, 1, 1))
    pls.extend(subset)
    value += val

    # Defenders
    subset, val = extract_players(available, formation[0], (1, 3, 2, 1))
    pls.extend(subset)
    value += val

    # Midfielders
    subset, val = extract_players(available, formation[1], (1, 2, 3, 2))
    pls.extend(subset)
    value += val

    # Forwards
    subset, val = extract_players(available, formation[2], (1, 1, 2, 3))
    pls.extend(subset)
    value += val

    return pls, value


def extract_players(players: typing.List[Player], count: int, mult: typing.Tuple[int, int, int, int]) -> typing.Tuple[typing.List[Player], int]:
    """Extract {count} players from a list of players, sorted on their weighted skills.
    """
    pls = sorted(
        players,
        key=lambda p: (p.stopping * mult[0] + p.tackling * mult[1] + p.passing * mult[2] + p.shooting * mult[3]) * p.stats.fitness,
        reverse=True)[:count]
    value = 0
    for p in pls:
        value += p.tackling
    return pls, value

