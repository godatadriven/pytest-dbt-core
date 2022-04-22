.. pytest-dbt-core documentation master file, created by
   sphinx-quickstart on Fri Jan 28 08:41:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pytest-dbt-core
###############

Write unit tests for your dbt logic with `pytest-dbt-core`!
`pytest-dbt-core` is a `pytest <https://docs.pytest.org>`_ plugin for testing your
`dbt <https://getdbt.com>`_ projects.

Installation
************

Install `pytest-dbt-core` via pip with

.. code-block:: bash

   python -m pip install pytest-dbt-core

Usage
******

Unit test a macro:

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   configuration.rst
   dbt_spark.rst
   projects.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
