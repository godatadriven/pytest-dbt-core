import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession


@pytest.mark.parametrize(
    "macro_generator",
    ["macro.dbt_project.fetch_single_statement"],
    indirect=True,
)
def test_create_table(
    spark_session: SparkSession, macro_generator: MacroGenerator
) -> None:
    out = macro_generator("SELECT 1")
    assert out == 1
