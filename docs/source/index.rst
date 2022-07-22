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

Create a macro:

.. literalinclude :: _static/dbt_project/macros/normalize_column_names.sql
   :language: jinja

Unit test a macro:

.. literalinclude :: _static/dbt_project/tests/test_normalize_column_names.py
   :language: python

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
