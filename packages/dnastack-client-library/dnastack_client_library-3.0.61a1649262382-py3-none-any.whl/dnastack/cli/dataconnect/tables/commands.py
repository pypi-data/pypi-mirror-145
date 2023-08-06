import json

import click

from ...utils import get_client, handle_error_gracefully


@click.group("tables")
def tables():
    pass


@tables.command("list")
@click.pass_context
@handle_error_gracefully
def list_tables(ctx: click.Context):
    click.echo(
        json.dumps(
            [
                t.dict()
                for t in get_client(ctx).dataconnect.list_tables()
            ],
            indent=4
        )
    )


@tables.command("get")
@click.pass_context
@click.argument("table_name")
@handle_error_gracefully
def get(ctx: click.Context, table_name):
    click.echo(
        json.dumps(
            get_client(ctx).dataconnect.table(table_name).info.dict(),
            indent=4,
        )
    )
