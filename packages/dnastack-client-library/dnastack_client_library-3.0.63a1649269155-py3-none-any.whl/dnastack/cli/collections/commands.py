import click

from .tables import commands as tables_commands
from ..dataconnect.helper import handle_query
from ..exporter import normalize, to_json
from ..utils import get_client, handle_error_gracefully


@click.group("collections")
def collections():
    pass


@collections.command(name="list", help="List collections")
@click.pass_context
@handle_error_gracefully
def list_collections(ctx: click.Context):
    listed_collections = get_client(ctx).collections.list_collections()
    click.echo(to_json(normalize(listed_collections)))


@collections.command("query", help="Query data")
@click.pass_context
@click.argument("collection_name")
@click.argument("query")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
)
@click.option(
    "--decimal-as",
    type=click.Choice(["string", "float"]),
    show_choices=True,
    default="string",
    show_default=True,
)
@handle_error_gracefully
def query_collection(ctx: click.Context, collection_name: str, query: str, format: str = "json", decimal_as: str = 'string'):
    return handle_query(get_client(ctx).collections.get_data_connect_client(collection_name), query, format, decimal_as)


# noinspection PyTypeChecker
collections.add_command(tables_commands.tables)
