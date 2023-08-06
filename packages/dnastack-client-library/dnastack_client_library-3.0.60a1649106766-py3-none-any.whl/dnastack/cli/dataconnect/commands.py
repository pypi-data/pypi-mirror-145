import json
from typing import Optional

import click
from requests import HTTPError

from .helper import handle_query
from .tables import commands as tables_commands
from ..exporter import to_json, normalize, to_csv
from ..utils import get_client, handle_error_gracefully
from ...exceptions import ServiceException


@click.group("dataconnect")
def dataconnect():
    pass


@dataconnect.command("query")
@click.pass_context
@click.argument("query")
@click.option(
    "-o",
    "--output",
    help="The path to the output file (Note: If the option is specified, there will be no output to stdout.)",
    required=False,
    default=None
)
@click.option(
    "-f",
    "--format",
    help="Output Format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True
)
@click.option(
    "--decimal-as",
    type=click.Choice(["string", "float"]),
    show_choices=True,
    default="string",
    show_default=True,
)
@handle_error_gracefully
def data_connect_query(ctx: click.Context, query: str, output: Optional[str] = None, format: str = "json", decimal_as: str = 'string'):
    return handle_query(get_client(ctx).data_connect, query, format, decimal_as, output_file=output)


# noinspection PyTypeChecker
dataconnect.add_command(tables_commands.tables)
