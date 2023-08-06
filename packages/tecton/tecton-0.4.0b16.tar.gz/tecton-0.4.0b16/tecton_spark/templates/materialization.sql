SELECT
  {%- for column in materialization_schema.columns %}
  {{ column.name }}
  {#- https://docs.snowflake.com/en/user-guide/data-unload-considerations.html#explicitly-converting-numeric-columns-to-parquet-data-types -#}
  {%- if cast_for_copy and column.feature_server_type == column_type_pb2.COLUMN_TYPE_INT64 %}::BIGINT AS {{column.name}}{%- endif %}
  {%- if not loop.last %}, {%- endif %}
  {%- endfor %}
FROM (
{{ source | indent(4)}}
)
WHERE {{ timestamp_key }} >= TO_TIMESTAMP_NTZ('{{ start_time }}')
  AND {{ timestamp_key }} <  TO_TIMESTAMP_NTZ('{{ end_time }}')
