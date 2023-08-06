import csv
import io
import json
from typing import Any, List, Callable, Tuple, Mapping

import click
import sys
from click import UsageError, Option

from .. import PublisherClient
from ..feature_flags import in_global_debug_mode


def get_client(ctx: click.Context) -> PublisherClient:
    """Return the created PublisherClient instance"""
    return PublisherClient()


    # CLICK EXTENSIONS
class MutuallyExclusiveOption(Option):
    """
    A click Option wrapper for sets of options where one but not both must be specified
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        original_help = kwargs.get("help", "")
        if self.mutually_exclusive:
            additional_help_text = "This is mutually exclusive with " \
                                   + " and ".join(sorted(self.mutually_exclusive)) + "."
            kwargs["help"] = f"{original_help}. Note that {additional_help_text}" if original_help else additional_help_text
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx: click.Context, opts: Mapping[str, Any], args: List[str]) -> Tuple[Any, List[str]]:
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


def parse_key_value_param(parameter: str, param_name: str) -> str:
    """Parse a parameters specified in a K=V format and dumps to a JSON str"""
    param_key_value = parameter.split("=")

    if len(param_key_value) != 2:
        click.secho(
            f"Invalid format for {param_name}. Must be a single key-value pair in the format K=V",
            fg="red",
        )
        sys.exit(1)

    return json.dumps({param_key_value[0].strip(): param_key_value[1].strip()})


def handle_error_gracefully(command: Callable) -> Callable:
    """
    Handle error gracefully

    This is disabled in the debug mode.
    """
    def handle_invocation(*args, **kwargs):
        if in_global_debug_mode:
            # In the debug mode, no error will be handled gracefully so that the developers can see the full detail.
            command(*args, **kwargs)
        else:
            try:
                command(*args, **kwargs)
            except Exception as e:
                click.secho(e, fg="red")
                sys.exit(1)
    return handle_invocation
