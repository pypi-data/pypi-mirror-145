{% from 'copier_macro.sql' import copy_into %}
{{ copy_into(destination, source, storage_integration) }}
