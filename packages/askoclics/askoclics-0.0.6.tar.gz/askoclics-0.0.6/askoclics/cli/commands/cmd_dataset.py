import click
from askoclics.cli.commands.dataset.delete import cli as delete
from askoclics.cli.commands.dataset.list import cli as list
from askoclics.cli.commands.dataset.publicize import cli as publicize


@click.group()
def cli():
    """
    Manipulate datasets managed by Askomics
    """
    pass


cli.add_command(delete)
cli.add_command(list)
cli.add_command(publicize)
