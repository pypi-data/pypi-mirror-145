import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('publicize')
@click.argument("dataset_id", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, dataset_id):
    """Publicize a dataset

Output:

    Dictionary with info and datasets
    """
    return ctx.gi.dataset.publicize(dataset_id)
