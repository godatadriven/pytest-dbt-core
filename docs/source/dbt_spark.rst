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

.. literalinclude :: _static/dbt_project/tests/test_spark_get_tables.py
   :language: python

Test
****

Run the Pytest via your preferred interface.

.. code-block:: bash

   pytest
