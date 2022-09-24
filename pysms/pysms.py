import click

import pydantic

from .models import Player
from pysms.persistence import provider_factory
from pysms import creators


@click.group()
def pysms():
    pass


@click.group(name="show")
def show_group():
    pass


@click.command(name="player")
@click.argument("player_id")
def show_player(player_id: str) -> None:
    print(f"pysms show player {player_id}")
    provider = provider_factory()
    player = provider.load_player(player_id)
    print(player)


@click.group(name="create")
def create_group():
    pass


@click.command(name="player")
def create_player() -> None:
    print(f"pysms create player")
    player = creators.create_player()
    provider = provider_factory()
    provider.save_player(player)
    print(player)


create_group.add_command(create_player)
pysms.add_command(create_group)

show_group.add_command(show_player)
pysms.add_command(show_group)
