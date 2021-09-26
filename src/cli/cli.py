import typer

from src.cli import character

app = typer.Typer()
app.add_typer(character.app, name="character")


def run():
    app()
