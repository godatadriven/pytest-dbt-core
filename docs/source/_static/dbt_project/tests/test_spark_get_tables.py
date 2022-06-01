import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession


@pytest.mark.parametrize(
    "macro_generator", ["macro.spark_utils.get_tables"], indirect=True
)
def test_get_tables(
    spark_session: SparkSession, macro_generator: MacroGenerator
) -> None:
    """The get tables macro should return the created table."""
    expected_table = "default.example"
    spark_session.sql(f"CREATE TABLE {expected_table} (id int) USING parquet")
    tables = macro_generator()
    assert tables == [expected_table]
