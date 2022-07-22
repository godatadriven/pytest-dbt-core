{% macro normalize_column_names(column_names) %}
{%- set re = modules.re -%}

{%- for column_name in column_names -%}

     {%- set normalized_column_name = re.sub('[!?@#$()%&]', '', column_name).strip().replace(' ', '_').replace('.', '_').rstrip('_').lower() -%}

     {# Columns should not start with digits #}
     {%- if normalized_column_name[0].isdigit()  -%}
          {% set normalized_column_name = '_' + normalized_column_name-%}
     {% endif -%}

     `{{ column_name }}` as {{ normalized_column_name }}
     {%- if not loop.last -%}, {% endif -%}

{%- endfor -%}

{% endmacro %}
