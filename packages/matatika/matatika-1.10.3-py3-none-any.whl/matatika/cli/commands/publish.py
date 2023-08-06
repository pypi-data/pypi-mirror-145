# pylint: disable=too-many-locals

"""CLI 'publish' command"""

# standard
from pathlib import Path
# external
import click
# local
from matatika.cli.display import Column, Table
from matatika.cli.utility import Resolver
from matatika.cli.parse_service import parse_yaml, parse_notebook
from .root import matatika


NOTEBOOK = ['.ipynb']
YAML = ['.yml', '.yaml']
SUPPORTED_FILETYPES = NOTEBOOK + YAML


@matatika.command('publish', short_help='Publish one or more dataset(s)')
@click.pass_context
@click.argument('dataset-file', type=click.Path(exists=True))
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
@click.option("--dataset-alias", '-alias', type=click.STRING, help="Dataset Alias")
def publish(ctx, dataset_file, workspace_id, dataset_alias):
    """Publish one or more dataset(s) from a YAML file into a workspace"""

    ctx.obj['workspace_id'] = workspace_id
    client = Resolver(ctx).client()

    file_ext = Path(dataset_file).suffix

    if file_ext not in SUPPORTED_FILETYPES:
        click.secho("Filetype not supported", fg='red')
        return

    if file_ext in YAML:
        datasets = parse_yaml(dataset_file, dataset_alias, file_ext)
        if datasets is None:
            click.secho("Cannot specify alias option with more than one dataset", fg='red')
            return

    elif file_ext in NOTEBOOK:
        datasets = parse_notebook(dataset_file, dataset_alias, file_ext)

    published_datasets = client.publish(datasets)

    click.secho(f"Successfully published {len(published_datasets)} dataset(s)\n",
                fg='green')

    ids = Column("DATASET ID")
    aliases = Column("ALIAS")
    titles = Column("TITLE")
    statuses = Column("STATUS")

    for dataset, status_code in published_datasets:
        if status_code == 201:
            status = click.style("NEW", fg='magenta')
        else:
            status = click.style("UPDATED", fg='cyan')

        if not dataset.alias:
            dataset.alias = click.style(str(dataset.alias), fg='yellow')

        ids.add(dataset.dataset_id)
        aliases.add(dataset.alias)
        titles.add(dataset.title)
        statuses.add(status)

    table = Table(ids, aliases, titles, statuses)
    click.echo(table)
