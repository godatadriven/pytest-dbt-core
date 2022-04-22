dbt-spark
#########

`dbt-spark` users are recommend to use the Spark connection method when testing.
Together with the `pytest Spark plugin <https://github.com/malexer/pytest-spark>`_,
a on-the-fly Spark session removes the need for hosting Spark.

Installation
************

Install `dbt-spark`, `pytest-dbt-core` and `pytest-spark` via pip with

.. code-block:: bash

   python -m pip install dbt-spark pytest-dbt-core pytest-spark


Configuration
*************

Configure `pytest-spark` via `pytest configuration <https://docs.pytest.org/en/6.2.x/customize.html#configuration>`_.

.. code-block:: cfg

   # setup.cfg
   [tool:pytest]
   spark_options =
       spark.executor.instances: 1
       spark.sql.catalogImplementation: in-memory

Usage
*****

Use the `spark_session` fixture to set-up the unit test for your macro:

.. code-block:: python

   from __future__ import annotations

   import pytest
   from dbt.clients.jinja import MacroGenerator
   from pyspark.sql import SparkSession


   @pytest.mark.parametrize(
       "macro_generator", ["macro.spark_utils.get_tables"], indirect=True
   )
   def test_create_table(
       spark_session: SparkSession, macro_generator: MacroGenerator
   ) -> None:
       expected_table = "default.example"
       spark_session.sql(f"CREATE TABLE {expected_table} (id int) USING parquet")
       tables = macro_generator()
       assert tables == [expected_table]

Test
****

Run the Pytest via your preferred interface.

.. code-block:: bash

   pytest
