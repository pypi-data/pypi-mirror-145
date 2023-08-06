from ...utils import get_client, handle_error_gracefully
import json
import click


@click.group("tables")
def tables():
    """Data Client API for Collections"""
    pass


@tables.command("list",
                help="""
                List tables for a given collection

                ID_OR_SLUG_NAME is the ID or slug name of the target collection.
                """)
@click.pass_context
@click.argument("id_or_slug_name")
@handle_error_gracefully
def list_tables(ctx: click.Context, id_or_slug_name: str):
    click.echo(
        json.dumps(
            [t.dict() for t in get_client(ctx)
                .collections
                .get_data_connect_client(id_or_slug_name)
                .list_tables()],
            indent=4
        )
    )
