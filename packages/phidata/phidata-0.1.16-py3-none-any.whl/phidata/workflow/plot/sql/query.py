from typing import Optional, Any

from phidata.asset.table.sql import SqlTable
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger
from phidata.workflow.py.python_workflow_base import (
    PythonWorkflowBase,
    PythonWorkflowBaseArgs,
    EngineType,
)


class PlotSqlQueryArgs(PythonWorkflowBaseArgs):
    query: str
    sql_table: SqlTable
    show_sample_data: bool = False


class PlotSqlQuery(PythonWorkflowBase):
    def __init__(
        self,
        query: str,
        sql_table: SqlTable,
        show_sample_data: bool = False,
        engine: EngineType = EngineType.PANDAS,
        name: str = "plot_sql_query",
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ):
        super().__init__()
        try:
            self.args: PlotSqlQueryArgs = PlotSqlQueryArgs(
                query=query,
                sql_table=sql_table,
                show_sample_data=show_sample_data,
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
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        # Add the SQLAlchemy engine if conn_id is present
        if self.args.sql_table.db_conn_id is not None:
            logger.info(
                f"Creating DbEngine using db_conn_id: {self.args.sql_table.db_conn_id}"
            )
            pg_hook = PostgresHook(postgres_conn_id=self.args.sql_table.db_conn_id)
            self.args.sql_table.db_engine = pg_hook.get_sqlalchemy_engine()

        return super().add_airflow_tasks_to_dag(dag)


def run_sql_query_pandas(args: PlotSqlQueryArgs) -> bool:

    import pandas as pd
    import matplotlib.pyplot as plt

    query: str = args.query
    sql_table: SqlTable = args.sql_table

    print_info("Running Query:\n{}".format(query))
    df: Optional[pd.DataFrame] = sql_table.run_sql_query(query)

    if df is None:
        print_error("Could not run query")
        return False

    if args.show_sample_data:
        print_info("Sample data:\n{}".format(df.head()))
        print_info("Plotting")
        df.plot("ds", "active_users")
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    return True


def run_sql_query(**kwargs) -> bool:
    args: PlotSqlQueryArgs = PlotSqlQueryArgs(**kwargs)

    if args.engine in (EngineType.PANDAS, EngineType.DEFAULT):
        return run_sql_query_pandas(args)
    else:
        print_error(f"EngineType: {args.engine} not yet supported")
        return False
