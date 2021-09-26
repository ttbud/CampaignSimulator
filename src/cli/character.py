from typing import TypeVar, List

import typer

from src.config.parse import parse
from src.simulator import Simulator

app = typer.Typer()

_T = TypeVar("_T")


def first(items: List[_T], key, value):
    return next(item for item in items if getattr(item, key) == value)


@app.command()
def location(character: str, time: int):
    config = parse('./tests/example.yml')
    sim = Simulator(config.non_player_characters, config.locations, time)
    char = first(config.non_player_characters, 'name', character)
    typer.echo(sim.get_npc_location(char).name)
