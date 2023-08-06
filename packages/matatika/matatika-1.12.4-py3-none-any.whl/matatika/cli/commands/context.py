"""CLI 'context' command and subcommands"""

# external
import click
# local
from matatika.cli.display import Column, Table
from matatika.context import MatatikaContext
from matatika.exceptions import NoDefaultContextSetError
from matatika.cli.variables import VariableType
from .root import matatika


@matatika.group("context", short_help="Context operations")
def context():
    """Base context command"""


@context.command("list", short_help="List all configured contexts")
@click.pass_obj
def list_(obj):
    """Lists all configured contexts"""

    contexts = MatatikaContext(obj['context_home']).get_all_contexts()

    names = Column("CONTEXT NAME")
    auth_tokens = Column("AUTH TOKEN")
    client_ids = Column("CLIENT ID")
    endpoint_urls = Column("ENDPOINT URL")
    workspace_ids = Column("WORKSPACE ID")

    for name, variables in contexts.items():
        names.add(name)
        auth_tokens.add(variables.get('auth_token'))
        client_ids.add(variables.get('client_id'))
        endpoint_urls.add(variables.get('endpoint_url'))
        workspace_ids.add(variables.get('workspace_id'))

    table = Table(names, auth_tokens, client_ids, endpoint_urls, workspace_ids)
    click.echo(table)


@context.command("create", short_help="Create a new context")
@click.pass_obj
@click.argument("context-name")
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--client-id", "-i", help="Client ID")
@click.option("--client-secret", "-s", help="Client secret")
@click.option("--endpoint-url", "-e", default='https://catalog.matatika.com/api',
              help="Endpoint URL")
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def create(obj, context_name, **kwargs):
    """Creates a new context"""

    options = {key: val and str(val) for key, val in kwargs.items()}
    MatatikaContext(obj['context_home']).create_context(context_name, options)


@context.command("delete", short_help="Delete a context")
@click.pass_obj
@click.argument("context-name")
def delete(obj, context_name):
    """Deletes an existing context"""

    matatika_context = MatatikaContext(obj['context_home'])

    try:
        default_context_name, _default_context_variables = matatika_context.get_default_context()

        if context_name == default_context_name:
            matatika_context.set_default_context(None)

    except NoDefaultContextSetError:
        pass

    finally:
        matatika_context.delete_context(context_name)


@context.command("use", short_help="Set a default context")
@click.pass_obj
@click.argument("context-name")
def use(obj, context_name):
    """Set a context to use by default"""

    MatatikaContext(obj['context_home']).set_default_context(context_name)


@context.command("info", short_help="Show the default context")
@click.pass_obj
def info(obj):
    """Shows the default context"""

    name, variables = MatatikaContext(
        obj['context_home']).get_default_context()
    variables.pop('client_secret', None)

    labels = Column()
    values = Column()

    labels.add("CONTEXT NAME", *[VariableType(l).label()
               for l in variables.keys()])
    values.add(name, *variables.values())

    table = Table(labels, values)
    click.echo(table.create(separator="\t-->\t"))


@context.command("update", short_help="Update the default context")
@click.pass_obj
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--client-id", "-i", help="Client ID")
@click.option("--client-secret", "-s", help="Client secret")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def update(obj, **kwargs):
    """Updates the default context"""

    options = {key: str(val) for key, val in kwargs.items() if val}
    MatatikaContext(obj['context_home']
                    ).update_default_context_variables(options)
