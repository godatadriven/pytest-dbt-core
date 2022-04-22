{% macro to_cents(column_name) %}
  {{ column_name }} * 100
{% endmacro %}
