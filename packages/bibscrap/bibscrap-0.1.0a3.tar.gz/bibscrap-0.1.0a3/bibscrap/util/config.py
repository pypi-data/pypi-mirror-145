import pathlib
import tomli

from typing import TYPE_CHECKING
from typing import Optional, TypedDict


class LoggingConfig(TypedDict):
    """Describes a logging configuration.

    See Also:
        https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    """

    #: Represents the schema version. The only valid value at present is
    #: :py:`1`, but having this key allows the schema to evolve while still
    #: preserving backwards compatibility.
    version: int = 1

    #: Indicates whether the configuration is to be interpreted as incremental
    #: to the existing configuration. This value defaults to :py:`False`, which
    #: means that the specified configuration replaces the existing
    #: configuration with the same semantics as used by the existing
    #: :py:func:`logging.config.fileConfig` API.
    incremental: Optional[bool]

    #: Indicates whether any existing non-root loggers are to be disabled. This
    #: setting mirrors the parameter of the same name in
    #: :py:func:`logging.config.fileConfig`. If absent, this parameter defaults
    #: to :py:`True`. This value is ignored if :py:data:`LoggingConfig.incremental`
    #: is :py:`True`.
    disable_existing_loggers: Optional[bool]

    def __new__(cls, *args, **kwargs):
        print("here")
        return super().__new__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        print("here")
        print(*args, **kwargs)
        super().__init__(*args, **kwargs)


class Config(TypedDict):
    logging: LoggingConfig


DEFAULT_CONFIG_FILES = [
    "pyproject.toml",
    "bibscrap.toml",
]


def read_config() -> dict:
    path = pathlib.Path(".")
    config_path = path / "pyproject.toml"
    if config_path.exists():
        with config_path.open() as config_file:
            config = tomli.loads(config_file.read())
            return config.get("tool", {}).get("bibscrap", {})


def print_config() -> None:
    from pprint import pprint

    config = read_config()
    pprint(config)
