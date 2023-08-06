from typing import Optional, Any

from phidata.asset.table.sql import SqlTable, SqlType
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger
from phidata.workflow.py.python_workflow_base import (
    PythonWorkflowBase,
    PythonWorkflowBaseArgs,
    EngineType,
)


class RunSqlQueryArgs(PythonWorkflowBaseArgs):
    query: str
    sql_table: SqlTable
    show_sample_data: bool = False
    load_result_to: Optional[SqlTable] = None


class RunSqlQuery(PythonWorkflowBase):
    def __init__(
        self,
        query: str,
        sql_table: SqlTable,
        show_sample_data: bool = False,
        load_result_to: Optional[SqlTable] = None,
        engine: EngineType = EngineType.PANDAS,
        name: str = "run_sql_query",
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ):
        super().__init__()
        try:
            self.args: RunSqlQueryArgs = RunSqlQueryArgs(
                query=query,
                sql_table=sql_table,
                show_sample_data=show_sample_data,
                load_result_to=load_result_to,
                engine=engine,
                name=name,
                task_id=task_id,
                dag_id=dag_id,
                version=version,
                enabled=enabled,
                entrypoint=run_sql_query,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def query(self) -> Optional[str]:
        return self.args.query

    @query.setter
    def query(self, query: str) -> None:
        if query is not None:
            self.args.query = query

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

        # Add the SQLAlchemy engine if conn_id is present
        if self.args.sql_table.db_conn_id is not None:
            logger.info(
                f"Creating DbEngine using db_conn_id: {self.args.sql_table.db_conn_id}"
            )

            if self.args.sql_table.sql_type == SqlType.POSTGRES:
                from airflow.providers.postgres.hooks.postgres import PostgresHook

                pg_hook = PostgresHook(postgres_conn_id=self.args.sql_table.db_conn_id)
                self.args.sql_table.db_engine = pg_hook.get_sqlalchemy_engine()

        if self.args.load_result_to.db_conn_id is not None:
            logger.info(
                f"Creating DbEngine using db_conn_id: {self.args.load_result_to.db_conn_id}"
            )

            if self.args.load_result_to.sql_type == SqlType.POSTGRES:
                from airflow.providers.postgres.hooks.postgres import PostgresHook

                pg_hook = PostgresHook(
                    postgres_conn_id=self.args.load_result_to.db_conn_id
                )
                self.args.load_result_to.db_engine = pg_hook.get_sqlalchemy_engine()

        return super().add_airflow_tasks_to_dag(dag)


def run_sql_query_pandas(args: RunSqlQueryArgs) -> bool:

    import pandas as pd

    query: str = args.query
    sql_table: SqlTable = args.sql_table

    df: Optional[pd.DataFrame] = sql_table.run_sql_query(query)
    if df is None:
        print_error("Result DataFrame is empty")
        return False

    if args.show_sample_data:
        print_info("Sample data:\n{}".format(df.head()))

    if args.load_result_to is not None:
        load_sql_table = args.load_result_to
        if not isinstance(load_sql_table, SqlTable):
            print_error("load_result_to value not of type SqlTable")
            return False

        load_success = load_sql_table.write_pandas_df(df)
        return load_success

    return True


def run_sql_query(**kwargs) -> bool:
    args: RunSqlQueryArgs = RunSqlQueryArgs(**kwargs)

    if args.engine in (EngineType.PANDAS, EngineType.DEFAULT):
        return run_sql_query_pandas(args)
    else:
        print_error(f"EngineType: {args.engine} not yet supported")
        return False
