# Enable logging for "requests"

import logging
from http.client import HTTPConnection
from typing import Optional

from dnastack.feature_flags import in_global_debug_mode
from dnastack.helpers.environments import env

logging_format = '[ %(asctime)s | %(levelname)s ] %(name)s: %(message)s'
overriding_logging_level_name = env('DNASTACK_LOG_LEVEL', 'ERROR')
default_logging_level = getattr(logging, overriding_logging_level_name) \
    if overriding_logging_level_name in ('DEBUG', 'INFO', 'WARNING', 'ERROR') \
    else logging.WARNING

if in_global_debug_mode:
    default_logging_level = logging.DEBUG
    HTTPConnection.debuglevel = 1

logging.basicConfig(format=logging_format,
                    level=default_logging_level)

# Configure the logger of HTTP client (global settings)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(default_logging_level)
requests_log.propagate = True


def get_logger(name: str, level: Optional[int] = None):
    formatter = logging.Formatter(logging_format)

    handler = logging.StreamHandler()
    handler.setLevel(level or default_logging_level)
    handler.setFormatter(formatter)

    logger = logging.Logger(name)
    logger.setLevel(level or default_logging_level)
    logger.addHandler(handler)

    return logger
