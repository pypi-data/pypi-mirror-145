import json
from typing import Optional

import click
from requests import HTTPError

from dnastack.cli.exporter import normalize, to_json, to_csv
from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.exceptions import ServiceException


def handle_query(data_connect: DataConnectClient,
                 query: str,
                 format: str = "json",
                 decimal_as: str = 'string',
                 output_file: Optional[str] = None):
    iterator = [r for r in data_connect.query(query)]

    try:
        normalized_results = normalize(iterator, map_decimal=str if decimal_as == 'string' else float)
    except HTTPError as h:
        error_json = json.loads(h.response.text)
        error_msg = "Unable to get the paginated response"
        if "errors" in error_json:
            error_msg += f": {error_json['errors'][0]['title']}"
        raise ServiceException(url=data_connect.url, msg=error_msg)

    result_output = to_json(normalized_results) if format == "json" else to_csv(normalized_results)

    if output_file:
        with open(output_file, "w") as fs:
            fs.write(result_output)
    else:
        click.echo(result_output, nl=(format != "csv"))