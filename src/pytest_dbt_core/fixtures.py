"""The pytest fixtures."""

from __future__ import annotations

import dataclasses
import os

import dbt.tracking
import pytest
from _pytest.fixtures import SubRequest
from dbt.clients.jinja import MacroGenerator
from dbt.config.runtime import RuntimeConfig
from dbt.context import providers
from dbt.contracts.graph.manifest import Manifest
from dbt.parser.manifest import ManifestLoader
from dbt.tracking import User

from dbt.adapters.factory import (  # isort:skip
    AdapterContainer,
    get_adapter,
    register_adapter,
)


dbt.tracking.active_user = User(os.getcwd())


@dataclasses.dataclass(frozen=True)
class Args:
    """
    The arguments.

    dbt is written as command line tool, therefore the entrypoints of dbt expect
    (parsed) arguments. To reuse dbt's entrypoints we mock the (minimally)
    arguments here.
    """

    project_dir: str


@pytest.fixture
def config(request: SubRequest) -> RuntimeConfig:
    """
    Get the (runtime) config.

    Parameters
    ----------
    request : SubRequest
        The pytest request.

    Returns
    -------
    RuntimeConfig
        The runtime config.
    """
    project_dir = request.config.getoption("--dbt-project-dir")
    config = RuntimeConfig.from_args(Args(project_dir=project_dir))
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
