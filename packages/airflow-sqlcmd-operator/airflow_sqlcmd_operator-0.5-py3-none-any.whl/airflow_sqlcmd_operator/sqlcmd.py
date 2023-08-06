import os

from airflow.hooks.base_hook import BaseHook
from airflow.operators.bash_operator import BashOperator
from airflow.utils.decorators import apply_defaults


class SqlcmdOperator(BashOperator):

    template_fields = ("task_id", "bash_command", "sql_command", "sql_folder", "sql_file")
    # Currently works only with fixed sqlcmd binary
    # Must keep a whitespace at the end of the string.
    sql_command = "/opt/mssql-tools/bin/sqlcmd -b -C -S {{ params.host }} -i {{ params.file }} "

    def add_user_config(self, user, password):
        """Returns the sqlcmd command with the user and password."""
        sql_command = self.sql_command
        sql_command += f"-U {user} -P {password}"
        return sql_command

    @apply_defaults
    def __init__(self, *, mssql_conn_id, sql_folder, sql_file, **kwargs):

        db = BaseHook.get_connection(mssql_conn_id)

        params = {
            "host": db.host,
            "login": db.login,
            "password": db.password,
            "file": self.sql_script_path(sql_folder, sql_file),
        }

        sql_command = self.sql_command
        if params["login"] and params["login"] != "":
            sql_command = self.add_user_config(params["login"], params["password"])

        super(SqlcmdOperator, self).__init__(bash_command=sql_command, params=params, **kwargs)
        self.mssql_conn_id = mssql_conn_id
        self.sql_folder = sql_folder
        self.sql_file = sql_file

    def sql_script_path(self, sql_folder, sql_file):
        """Returns the corrected file path with quotation marks."""
        path = os.path.join(sql_folder, sql_file)
        return f"'{path}'"
