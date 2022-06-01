"""The entrypoint for the plugin."""

import os

from _pytest.config.argparsing import Parser

from .fixtures import adapter, config, macro_generator, manifest

__all__ = (
    "adapter",
    "config",
    "macro_generator",
    "manifest",
)


def pytest_addoption(parser: Parser) -> None:
    """
    Add pytest options.

    Parameters
    ----------
    parser : Parser
        The parser.
    """
    parser.addoption(
        "--dbt-project-dir",
        help="The dbt project directory.",
        type="string",
        default=os.getcwd(),
    )
    parser.addoption(
        "--dbt-target",
        help="Which target to load for the given profile",
        type="string",
    )
