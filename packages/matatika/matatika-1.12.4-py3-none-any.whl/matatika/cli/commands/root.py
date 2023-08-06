"""CLI entrypoint 'matatika' command"""

import sys
from pathlib import Path
import pkg_resources
from auth0.v3.exceptions import Auth0Error
import click
from requests.exceptions import HTTPError
from matatika.context import MatatikaContext
from matatika.exceptions import MatatikaException, NoDefaultContextSetError
from matatika.library import MatatikaClient

version = pkg_resources.require("matatika")[0].version


class ExceptionHandler(click.Group):
    """CLI entrypoint and error handling"""

    def invoke(self, ctx):
        """Invoke method override"""

        try:
            super().invoke(ctx)

        except (Auth0Error, HTTPError, MatatikaException) as err:
            click.secho(str(err), fg='red')
            sys.exit(1)


@click.group(cls=ExceptionHandler)
@click.pass_context
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--client-id", "-i", help="Client ID")
@click.option("--client-secret", "-s", help="Client secret")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--trace", "-t", is_flag=True, help="Trace variable sources")
@click.option("--context-home", "-c",
              type=click.Path(file_okay=False, writable=True),
              default=f'{Path.home()}/.matatika',
              envvar="MATATIKA_CONTEXT_HOME",
              help="Context home directory")
@click.version_option(version=version)
def matatika(ctx, **kwargs):
    """CLI entrypoint and base command"""

    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)


@matatika.resultcallback()
@click.pass_obj
def process_result(obj: dict, _result, **_kwargs):
    """Result callback for `matatika` command group"""

    client: MatatikaClient = obj.get('client')

    if not client:
        return

    matatika_context = MatatikaContext(obj['context_home'])

    try:
        matatika_context.update_default_context_variables(
            {'auth_token': client.auth_token})
    except NoDefaultContextSetError:
        pass
