import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession
from pyspark.sql import types as T  # noqa: N812


@pytest.mark.parametrize(
    "macro_generator",
    ["macro.dbt_project.normalize_column_names"],
    indirect=True,
)
@pytest.mark.parametrize(
    "column,expected_column",
    [
        ("unit", "unit"),
        ("column with spaces", "column_with_spaces"),
        ("c!h?a#r$a(c)t%e&rs", "characters"),
    ],
)
def test_normalize_column_names_spaces_are_replaced_with_underscores(
    spark_session: SparkSession,
    macro_generator: MacroGenerator,
    column: str,
    expected_column: str,
) -> None:
    """The spaces in the column names should be replaced with underscores."""
    schema = T.StructType([T.StructField(column, T.BooleanType(), True)])
    df = spark_session.createDataFrame(
        spark_session.sparkContext.emptyRDD(), schema=schema
    )

    df.createOrReplaceTempView("replace_spaces_with_underscores")
    normalized_column_names = macro_generator(df.columns)
    out = spark_session.sql(
        f"SELECT {normalized_column_names} FROM replace_spaces_with_underscores"
    )

    assert out.columns[0] == expected_column
