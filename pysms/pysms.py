import click

from pysms.persistence import provider_factory
from pysms import creators


@click.group()
def pysms():
    pass


@click.group(name="player")
def player_group():
    pass


@click.command(name="create")
@click.option("--env", "-e", help="The file where to get env variables from")
@click.option("--position", "-p", required=True, help="The player position")
@click.option("--save", "-s", is_flag=True, show_default=True, default=False)
def create_player(env: str, position: str, save: bool) -> None:
    print("pysms player create")
    config = creators.PlayerCreateConfig(_env_file=env)
    print(config)
    player = creators.create_player(config, position)
    if save:
        provider = provider_factory()
        provider.save_player(player)
    print(player.json(indent=2))


@click.command(name="show")
@click.argument("player_id")
def show_player(player_id: str) -> None:
    print(f"pysms player show {player_id}")
    provider = provider_factory()
    player = provider.load_player(player_id)
    print(player.json(indent=2))


@click.group(name="roster")
def roster_group():
    pass


@click.command(name="create")
@click.option("--env", "-e", help="The file where to get env variables from")
@click.option("--save", "-s", is_flag=True, show_default=True, default=False)
def create_roster(env: str, save: bool) -> None:
    print("pysms roster create")
    players_config = creators.PlayerCreateConfig(_env_file=env)
    config = creators.RosterCreateConfig(players=players_config, _env_file=env)
    roster = creators.create_roster(config)
    if save:
        provider = provider_factory()
        provider.save_roster(roster)
    print(roster.json(indent=2))


@click.command(name="show")
@click.argument("roster_id")
def show_roster(roster_id: str) -> None:
    print(f"pysms roster show {roster_id}")
    provider = provider_factory()
    roster = provider.load_roster(roster_id)
    print(roster.json(indent=2))


@click.group(name="team")
def team_group():
    pass


@click.command(name="create")
def create_team() -> None:
    print("pysms team create")
    team = creators.create_team()
    # provider = provider_factory()
    # provider.save_roster(roster)
    print(team.json(indent=2))


@click.group(name="teamsheet")
def teamsheet_group():
    pass


@click.command(name="create")
@click.option("--env", "-e", help="The file where to get env variables from")
def create_teamsheet(env: str) -> None:
    print("pysms teamsheet create")
    # FIXME: for now, let's create a brand new roster
    players_config = creators.PlayerCreateConfig(_env_file=env)
    roster_config = creators.RosterCreateConfig(players=players_config, _env_file=env)
    roster = creators.create_roster(roster_config)

    teamsheet = creators.create_teamsheet(roster)
    print(teamsheet.json(indent=2))


player_group.add_command(create_player)
player_group.add_command(show_player)
pysms.add_command(player_group)

roster_group.add_command(create_roster)
roster_group.add_command(show_roster)
pysms.add_command(roster_group)

team_group.add_command(create_team)
pysms.add_command(team_group)

teamsheet_group.add_command(create_teamsheet)
pysms.add_command(teamsheet_group)
