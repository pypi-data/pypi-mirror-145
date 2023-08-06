from pathlib import Path
from typing import Optional, Any

from phidata.asset.file import File, FileType
from phidata.asset.table.sql import SqlTable
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger
from phidata.workflow.py.python_workflow_base import (
    PythonWorkflowBase,
    PythonWorkflowBaseArgs,
    EngineType,
)


class UploadFileToSqlArgs(PythonWorkflowBaseArgs):
    file: File
    sql_table: SqlTable


class UploadFileToSql(PythonWorkflowBase):
    def __init__(
        self,
        file: File,
        sql_table: SqlTable,
        engine: EngineType = EngineType.PANDAS,
        name: str = "load_file_to_sql",
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ):
        super().__init__()
        try:
            self.args: UploadFileToSqlArgs = UploadFileToSqlArgs(
                file=file,
                sql_table=sql_table,
                engine=engine,
                name=name,
                task_id=task_id,
                dag_id=dag_id,
                version=version,
                enabled=enabled,
                entrypoint=load_file_to_sql_table,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def file(self) -> Optional[File]:
        return self.args.file

    @file.setter
    def file(self, file: File) -> None:
        if file is not None:
            self.args.file = file

    @property
    def sql_table(self) -> Optional[SqlTable]:
        return self.args.sql_table

    @sql_table.setter
    def sql_table(self, sql_table: SqlTable) -> None:
        if sql_table is not None:
            self.args.sql_table = sql_table

    def add_airflow_tasks_to_dag(self, dag: Any) -> bool:
        """
        This function adds the airflow tasks for this workflow to a DAG.
        This function is called by the create_airflow_dag() and runs on the remote machine where airflow is available.

        Majority of the heavy lifting is done by super().add_airflow_tasks_to_dag()
        But we populate the sql_table.db_engine value using the sql_table.db_conn_id
        before calling super().add_airflow_tasks_to_dag()
        """
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        # Add the SQLAlchemy engine if conn_id is present
        if self.args.sql_table.db_conn_id is not None:
            logger.info(
                f"Creating DbEngine using db_conn_id: {self.args.sql_table.db_conn_id}"
            )
            pg_hook = PostgresHook(postgres_conn_id=self.args.sql_table.db_conn_id)
            self.args.sql_table.db_engine = pg_hook.get_sqlalchemy_engine()

        return super().add_airflow_tasks_to_dag(dag)


def load_file_to_sql_table_pandas(args: UploadFileToSqlArgs) -> bool:

    import pandas as pd

    file_to_load: Optional[File] = args.file
    if file_to_load is None:
        print_error("File not available")
        return False
    file_path: Optional[Path] = file_to_load.file_path
    if file_path is None:
        print_error("FilePath not available")
        return False
    file_type: Optional[FileType] = file_to_load.file_type
    if file_type is None:
        print_error("FileType not available")
        return False
    # logger.debug("File: {}".format(file_to_load.args))

    sql_table: Optional[SqlTable] = args.sql_table
    if sql_table is None:
        print_error("SqlTable not available")
        return False
    # logger.debug("SqlTable: {}".format(sql_table.args))

    logger.info("Reading: {}".format(file_path))
    df: Optional[pd.DataFrame] = None
    if file_type == FileType.CSV:
        df = pd.read_csv(file_path)
    elif file_type == FileType.JSON:
        df = pd.read_json(file_path)
    elif file_type == FileType.TSV:
        df = pd.read_csv(file_path, sep="\t")

    if df is not None:
        # logger.info()("DataFrame:\n{}".format(df.head()))
        logger.info("Writing to table: {}".format(sql_table.name))
        upload_success = sql_table.write_pandas_df(df)
        return upload_success
    else:
        logger.info("Could not read file into DataFrame")
        return False


def load_file_to_sql_table(**kwargs) -> bool:
    args: UploadFileToSqlArgs = UploadFileToSqlArgs(**kwargs)
    # logger.debug("LoadFileToSqlTableArgs: {}".format(args))

    if args.engine in (EngineType.PANDAS, EngineType.DEFAULT):
        return load_file_to_sql_table_pandas(args)
    else:
        print_error(f"EngineType: {args.engine} not yet supported")
        return False
