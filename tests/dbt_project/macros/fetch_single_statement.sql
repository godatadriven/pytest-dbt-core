{% macro fetch_single_statement(statement, default_value="") %}

  {% set results = run_query(statement) %}

  {% if execute %}
    {% set value = results.columns[0].values()[0] %}
  {% else %}
    {% set value = default_value %}
  {% endif %}

  {{ return( value ) }}

{% endmacro %}
