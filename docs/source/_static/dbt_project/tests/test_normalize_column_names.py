import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession


@pytest.mark.parametrize(
    "macro_generator",
    ["macro.dbt_project.normalize_column_names"],
    indirect=True,
)
@pytest.mark.parametrize(
    "column_name,expected_column_name",
    [
        ("unit", "unit"),
        ("column with spaces", "column_with_spaces"),
        ("c!h?a#r$a(c)t%e&rs", "characters"),
        ("trailing white spaces  ", "trailing_white_spaces"),
        ("column.with.periods", "column_with_periods"),
        ("9leading number", "_9leading_number"),
        ("UPPERCASE", "uppercase"),
    ],
)
def test_normalize_column_names(
    spark_session: SparkSession,
    macro_generator: MacroGenerator,
    column_name: str,
    expected_column_name: str,
) -> None:
    """Test normalize column names with different scenarios."""
    normalized_column_names = macro_generator([column_name])
    out = spark_session.sql(
        f"SELECT {normalized_column_names} FROM (SELECT True AS `{column_name}`)"
    )
    assert out.columns[0] == expected_column_name, normalized_column_names
