"""The pytest fixtures."""

from __future__ import annotations

import dataclasses
import os

import dbt.tracking
import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from dbt.clients.jinja import MacroGenerator
from dbt.config.runtime import RuntimeConfig
from dbt.context import providers
from dbt.contracts.graph.manifest import Manifest
from dbt.parser.manifest import ManifestLoader
from dbt.tracking import User

from .session import _SparkConnectionManager

from dbt.adapters.factory import (  # isort:skip
    AdapterContainer,
    get_adapter,
    register_adapter,
)


dbt.tracking.active_user = User(os.getcwd())


def pytest_addoption(parser: Parser) -> None:
    """
    Add pytest option.

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


@dataclasses.dataclass(frozen=True)
class Args:
    """
    The arguments.

    dbt is written as command line tool, therefore the entrypoints of dbt expect
    (parsed) arguments. To reuse dbt's entrypoints we mock the (minimally)
    arguments here.
    """

    project_dir: str = os.getcwd()


@pytest.fixture
def config() -> RuntimeConfig:
    """
    Get the (runtime) config.

    Returns
    -------
    RuntimeConfig
        The runtime config.
    """
    # requires a profile in your project wich also exists in your profiles file
    config = RuntimeConfig.from_args(Args())
    return config


@pytest.fixture
def adapter(config: RuntimeConfig) -> AdapterContainer:
    """
    Get the adapter.

    Parameters
    ----------
    config : RuntimeConfig
        The runtime config.

    Returns
    -------
    AdapterContainer
        The adapter.
    """
    register_adapter(config)
    adapter = get_adapter(config)

    connection_manager = _SparkConnectionManager(adapter.config)
    adapter.connections = connection_manager

    adapter.acquire_connection()

    return adapter


@pytest.fixture
def manifest(
    adapter: AdapterContainer,
) -> Manifest:
    """
    Get the dbt manifest.

    Parameters
    ----------
    adapter : AdapterContainer
        The adapter.

    Returns
    -------
    Manifest
        The manifest.
    """
    manifest = ManifestLoader.get_full_manifest(adapter.config)
    return manifest


@pytest.fixture
def macro_generator(
    request: SubRequest, config: RuntimeConfig, manifest: Manifest
) -> MacroGenerator:
    """
    Get a macro generator.

    Parameters
    ----------
    request : SubRequest
        The pytest request containing the macro name.
    config : RuntimeConfig
        The runtime config.
    manifest : Manifest
        The manifest.

    Returns
    -------
    MacroGenerator
        The macro generator.
    """
    macro = manifest.macros[request.param]
    context = providers.generate_runtime_macro_context(
        macro, config, manifest, macro.package_name
    )
    macro_generator = MacroGenerator(macro, context)
    return macro_generator
