import typing
from urllib.parse import scheme_chars

from pysms.models import Teamsheet, Roster, Player, Formation, ALLOWED_FORMATIONS
from pysms.models.player import PlayerPosition, player_max_contribution, player_contribution

MAX_SUBS = 7


def create_teamsheet(roster: Roster) -> Teamsheet:
    available = [p for p in roster.players if not (
        p.stats.injury or p.stats.suspension)]
    goalkeepers = sorted([p for p in available if p.position == PlayerPosition.GOALKEEPER],
                         key=lambda p: player_contribution(p, PlayerPosition.GOALKEEPER), reverse=True)
    outfields = sorted([p for p in available if p.position != PlayerPosition.GOALKEEPER],
                       key=lambda p: player_max_contribution(p)[1], reverse=True)
    field_players = [goalkeepers[0]] + outfields[:10]
    bench_players = [goalkeepers[1]] + outfields[10:9+MAX_SUBS]
    return Teamsheet(team=roster.team, field=field_players, bench=bench_players)
