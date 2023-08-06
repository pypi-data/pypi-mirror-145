"""Console script for markdown_manager."""
from .markdown_manager import move_to_dos
from .markdown_manager import create_files

import click


@click.group()
def cli():
    pass


@click.command()
@click.argument("base_path")
def move_to_do(base_path):
    click.echo("Moving todos")
    move_to_dos(base_path)
    click.echo("Todos moved")


@click.command()
@click.argument("base_path")
@click.option(
    "--days_to_create", default=30, help="number of days in advance to create"
)
def create_all_files(base_path, days_to_create):
    click.echo("Creating files")
    create_files(base_path, days_to_create)
    click.echo("Files created")


cli.add_command(create_all_files)
cli.add_command(move_to_do)


if __name__ == "__main__":
    cli()
