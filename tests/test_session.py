from pyspark.sql import SparkSession

from pytest_dbt_core.session import Cursor


def test_cursor_execute_fetchall_returns_one_row(
    spark_session: SparkSession,
) -> None:
    """Test cursor if fetchall cursor returns one row."""

    cursor = Cursor()
    cursor.execute("SELECT 1")
    rows = cursor.fetchall()

    assert rows is not None
    assert len(rows) == 1
