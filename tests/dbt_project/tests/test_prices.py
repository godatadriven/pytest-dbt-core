import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession


@pytest.mark.parametrize(
    "macro_generator",
    ["macro.dbt_project.to_cents"],
    indirect=True,
)
def test_create_table(
    spark_session: SparkSession, macro_generator: MacroGenerator
) -> None:
    expected = spark_session.createDataFrame([{"cents": 1000}])
    to_cents = macro_generator("price")
    out = spark_session.sql(
        "with data AS (SELECT 10 AS price) "
        f"SELECT cast({to_cents} AS bigint) AS cents FROM data"
    )
    assert out.collect() == expected.collect()
