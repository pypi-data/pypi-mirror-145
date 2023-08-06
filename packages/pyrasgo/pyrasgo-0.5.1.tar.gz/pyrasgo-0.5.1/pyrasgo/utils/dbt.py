import os
import re
from pathlib import Path
import yaml

from typing import List, Tuple
from pyrasgo.storage.datawarehouse.base import DataWarehouse
from pyrasgo.storage.datawarehouse.snowflake import SnowflakeDataWarehouse
from pyrasgo.utils.naming import random_table_name
from pyrasgo.schemas.dw_operation import Operation

DBT_MODEL_CONFIG_TEMPLATE = '''
  config(
    {config_args}
  )
'''

def operations_as_cte(
    operations: List[Operation],
):
    """
    Returns a nested CTE statement to render this op set as a CTE
    """
    # Handle single transform chains, we already have the SQL
    if len(operations) == 1:
        print(operations[0])
        return operations[0].operation_sql

    # Handle multi-transform chains
    operation_list = []
    # Need to replace old FQTNs with CTE aliases
    fqtn_mapping = {}
    for operation in operations:
        # create new aliases to replace old FQTNs with
        alias = random_table_name()
        fqtn_mapping[operation.dw_table.fqtn] = alias

        op_sql = operation.operation_sql

        # replace all instances of generated FQTNs with CTE aliases
        for fqtn, alias in fqtn_mapping.items():
            op_sql = op_sql.replace(fqtn, alias)

        # if final op, we're done. join ops and leave last one alone
        # Final op itself might be a CTE, remove the WITH and slap it on the end of this chain
        if operation == operations[-1]:
            return 'WITH ' + ', \n'.join(operation_list) + _collapse_cte(op_sql)

        operation_list.append(f'{alias} AS (\n{op_sql}\n) ')

def _collapse_cte(
    sql: str
) -> str:
    """
    Returns a collapsed CTE if the sql itself is already a CTE (starts with "with")
    """
    return re.sub(r'^(WITH)\s', ', ', sql, 1, flags=re.IGNORECASE)

def create_dbt_files(
        sql_definition: str,
        schema: List[Tuple[str, str]],
        file_name: str,
        output_directory: str = None,
        config_args: dict = None,
        include_schema: bool = False
) -> str:
    """
    Saves a dbt_project.yml and model.sql files to a directory
    """
    output_directory = output_directory or os.getcwd()
    file_name = file_name + '.sql' if file_name[-4:] != '.sql' else file_name
    filepath = os.path.join(output_directory, file_name)
    if config_args:
        # TODO: Should we validate whether args are valid dbt keywords?
        model_config = DBT_MODEL_CONFIG_TEMPLATE.format(
            config_args=config_args
        )
        model_config = '{{' + model_config + '}}'
        sql_definition = f'{model_config}\n\n{sql_definition}'
    with open(filepath, "w") as _file:
        _file.write(sql_definition)
    if include_schema:
        model_name = file_name.replace('.sql', '')
        save_schema_file(output_directory, model_name, schema, config_args)
    return filepath

def save_schema_file(
        output_directory: Path,
        model_name: str,
        schema: List[Tuple[str, str]],
        config_args: dict = None,
    ):
    """
    Writes a table def to a dbt schema file
    """
    filepath = os.path.join(output_directory, 'schema.yml')
    schema_definition = None
    columns_list = []
    for row in schema:
        columns_list.append({"name:": row[0]})
    model_dict = {"name": model_name, "columns": columns_list}
    if config_args:
        model_dict.update({"config": config_args})
    if not os.path.exists(filepath):
        schema_definition = {"version": 2, "models": [model_dict]}
    else:
        schema_definition = [model_dict]
    with open(filepath, "a") as _file:
        yaml.dump(data=schema_definition, Dumper=yaml.SafeDumper, stream=_file, sort_keys=False)
    return filepath

