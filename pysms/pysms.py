import click

from pysms.persistence import provider_factory
from pysms import creators


@click.group()
def pysms():
    pass


@click.group(name="player")
def player_group():
    pass


@click.command(name="show")
@click.argument("player_id")
def show_player(player_id: str) -> None:
    print(f"pysms player show {player_id}")
    provider = provider_factory()
    player = provider.load_player(player_id)
    print(player)


@click.command(name="create")
def create_player() -> None:
    print("pysms player create")
    player = creators.create_player()
    provider = provider_factory()
    provider.save_player(player)
    print(player)


player_group.add_command(show_player)
player_group.add_command(create_player)
pysms.add_command(player_group)
