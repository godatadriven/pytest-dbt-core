"""The pytest fixtures."""

from __future__ import annotations

import dataclasses
import os

import dbt.tracking
import pytest
from _pytest.fixtures import SubRequest
from dbt import flags, version
from dbt.clients.jinja import MacroGenerator
from dbt.config import project
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


def _get_installed_dbt_version() -> tuple[int, int]:
    """Cast a dbt version to a tuple with major and minor version."""
    installed_dbt_version = version.get_installed_version()
    return int(installed_dbt_version.major), int(installed_dbt_version.minor)


DBT_INSTALLED_VERSION = _get_installed_dbt_version()


@dataclasses.dataclass(frozen=True)
class Args:
    """
    The arguments.

    dbt is written as command line tool, therefore the entrypoints of dbt expect
    (parsed) arguments. To reuse dbt's entrypoints we mock the (minimally)
    arguments here.

    Source
    ------
    See argparse `add_argument` statements in `dbt.main`.
    """

    project_dir: str
    profiles_dir: str
    target: str | None
    profile: str | None
    threads: int | None
    # Required from dbt version 1.8 onwards
    REQUIRE_RESOURCE_NAMES_WITHOUT_SPACES = False


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
    # For the  arguments that are hardcoded to `None`, dbt internals set the
    # appropiate values
    args = Args(
        project_dir=request.config.getoption("--dbt-project-dir"),
        profiles_dir=request.config.getoption("--profiles-dir"),
        target=request.config.getoption("--dbt-target"),
        profile=None,
        threads=None,
    )

    if DBT_INSTALLED_VERSION > (1, 5):
        # See https://github.com/dbt-labs/dbt-core/issues/9183
        project_flags = project.read_project_flags(
            args.project_dir, args.profiles_dir
        )
        flags.set_from_args(args, project_flags)
    else:
        flags.set_from_args(args, user_config=None)

    config = RuntimeConfig.from_args(args)
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
    if DBT_INSTALLED_VERSION > (1, 7):
        from dbt.mp_context import get_mp_context

        register_adapter(config, get_mp_context())
    else:
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
    if DBT_INSTALLED_VERSION > (1, 7):
        from dbt_common.clients.system import get_env
        from dbt_common.context import set_invocation_context

        set_invocation_context(get_env())

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
