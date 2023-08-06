COPY INTO {{ destination }}
FROM (
{{ source | indent(4)}}
)
header = true
detailed_output = true
file_format = (type=parquet)
{% if storage_integration %}storage_integration = {{ storage_integration }}{% endif %}
