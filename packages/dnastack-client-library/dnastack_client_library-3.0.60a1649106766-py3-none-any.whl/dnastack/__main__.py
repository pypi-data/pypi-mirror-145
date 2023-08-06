import click

from .cli import *
from .constants import (
    __version__,
)


@click.group("dnastack")
@click.version_option(__version__, message="%(version)s")
def dnastack():
    """DNAstack Client CLI

    https://www.dnastack.com
    """
    pass


@dnastack.command("version")
def get_version():
    click.echo(__version__)


# noinspection PyTypeChecker
dnastack.add_command(dataconnect_commands.dataconnect)
# noinspection PyTypeChecker
dnastack.add_command(config_commands.config)
# noinspection PyTypeChecker
dnastack.add_command(file_commands.files)
# noinspection PyTypeChecker
dnastack.add_command(auth_commands.auth)
# noinspection PyTypeChecker
dnastack.add_command(collections_commands.collections)
# noinspection PyTypeChecker
dnastack.add_command(wes_commands.wes)

if __name__ == "__main__":
    dnastack.main(prog_name="dnastack")
