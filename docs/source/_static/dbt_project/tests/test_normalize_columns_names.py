import pytest
from dbt.clients.jinja import MacroGenerator
from pyspark.sql import SparkSession, types as T


@pytest.mark.parametrize(
    "macro_generator", ["macro.dbt_project.normalize_column_names"], indirect=True
)
def test_normalize_column_names_spaces_are_replaced_with_underscores(
    spark_session: SparkSession, macro_generator: MacroGenerator
) -> None:
    """The spaces in the column names should be replaced with underscores."""
    expected_columns = ["column_with_spaces"]

    schema = T.StructType([T.StructField("column with spaces", T.BooleanType(), True)])
    df = spark_session.createDataFrame(spark_session.sparkContext.emptyRDD(), schema=schema)

    df.createOrReplaceTempView("replace_spaces_with_underscores")
    normalized_column_names = macro_generator(df.columns)
    out = spark_session.sql(f"SELECT {normalized_column_names} FROM replace_spaces_with_underscores")

    assert out.columns == expected_columns
