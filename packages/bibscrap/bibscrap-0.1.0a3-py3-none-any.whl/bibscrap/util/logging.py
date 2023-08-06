"""

"""

import logging
import logging.config
import logging.handlers

from typing import TYPE_CHECKING, Dict, List

from cleo.io.io import IO as CleoIO
from cleo.io.inputs.argv_input import ArgvInput
from cleo.io.outputs.stream_output import StreamOutput

NAMESPACE = "bibscrap"

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "bibscrap": {
            "format": "{asctime} {levelname: <8} {name: <15} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "cli": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "bibscrap",
        },
    },
    "loggers": {
        "bibscrap": {
            "handlers": ["cli"],
            "level": "INFO",
        },
    },
}


def getLogger(name: str) -> logging.Logger:
    logger = logging.getLogger(NAMESPACE + "." + name)
    logging.config.dictConfig(DEFAULT_LOGGING)
