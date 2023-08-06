from typing import Optional, Any, Union, Sequence
from typing_extensions import Literal

from sqlalchemy.engine import Engine, Connection

from phidata.asset import DataAsset, DataAssetArgs
from phidata.utils.enums import ExtendedEnum
from phidata.utils.cli_console import print_error, print_info
from phidata.utils.log import logger


class SqlType(ExtendedEnum):
    POSTGRES = "POSTGRES"


class SqlTableArgs(DataAssetArgs):
    # Table Name
    name: str
    sql_type: Optional[SqlType] = None
    # airflow connection_id can be used for running workflows in docker
    db_conn_id: Optional[str] = None
    # a db_conn_url can be used to create the sqlalchemy.engine.Engine object
    db_conn_url: Optional[str] = None
    # sqlalchemy.engine.(Engine or Connection)
    # Using SQLAlchemy makes it possible to use any DB supported by that library.
    # NOTE: db_engine is required when running locally
    db_engine: Optional[Union[Engine, Connection]] = None
    # How to behave if the table already exists.
    # fail: Raise a ValueError.
    # replace: Drop the table before inserting new values.
    # append: Insert new values to the existing table.
    if_exists: Literal["fail", "replace", "append"] = "replace"
    # Specify the schema (if database flavor supports this).
    # If None, use default schema.
    db_schema: Optional[str] = None
    # Write DataFrame index as a column.
    # Uses index_label as the column name in the table.
    index: Optional[bool] = None
    # Column label for index column(s).
    # If None is given (default) and index is True, then the index names are used.
    # A sequence should be given if the DataFrame uses MultiIndex.
    index_label: Optional[Union[str, Sequence]] = None
    # Specify the number of rows in each batch to be written at a time.
    # By default, all rows will be written at once.
    chunksize: Optional[int] = None


class SqlTable(DataAsset):
    """Base Class for Sql tables"""

    def __init__(self) -> None:
        super().__init__()
        self.args: Optional[SqlTableArgs] = None

    @property
    def sql_type(self) -> Optional[SqlType]:
        return self.args.sql_type if self.args else None

    @property
    def db_conn_id(self) -> Optional[str]:
        return self.args.db_conn_id if self.args else None

    @db_conn_id.setter
    def db_conn_id(self, db_conn_id: str) -> None:
        if db_conn_id is not None:
            self.args.db_conn_id = db_conn_id

    @property
    def db_conn_url(self) -> Optional[str]:
        return self.args.db_conn_url if self.args else None

    @db_conn_url.setter
    def db_conn_url(self, db_conn_url: str) -> None:
        if db_conn_url is not None:
            self.args.db_conn_url = db_conn_url

    @property
    def db_engine(self) -> Optional[Union[Engine, Connection]]:
        return self.args.db_engine if self.args else None

    @db_engine.setter
    def db_engine(self, db_engine: Optional[Union[Engine, Connection]]) -> None:
        if db_engine is not None:
            self.args.db_engine = db_engine

    @property
    def if_exists(self) -> Literal["fail", "replace", "append"]:
        return self.args.if_exists

    @if_exists.setter
    def if_exists(self, if_exists: Literal["fail", "replace", "append"]) -> None:
        if if_exists is not None:
            self.args.if_exists = if_exists

    @property
    def db_schema(self) -> Optional[str]:
        return self.args.db_schema if self.args else None

    @db_schema.setter
    def db_schema(self, db_schema: Optional[str]) -> None:
        if db_schema is not None:
            self.args.db_schema = db_schema

    @property
    def index(self) -> Optional[bool]:
        return self.args.index if self.args else None

    @index.setter
    def index(self, index: Optional[bool]) -> None:
        if index is not None:
            self.args.index = index

    @property
    def index_label(self) -> Optional[Union[str, Sequence]]:
        return self.args.index_label if self.args else None

    @index_label.setter
    def index_label(self, index_label: Optional[Union[str, Sequence]]) -> None:
        if index_label is not None:
            self.args.index_label = index_label

    @property
    def chunksize(self) -> Optional[int]:
        return self.args.chunksize if self.args else None

    @chunksize.setter
    def chunksize(self, chunksize: Optional[int]) -> None:
        if chunksize is not None:
            self.args.chunksize = chunksize

    def create_db_engine_using_conn_url(self) -> None:
        # Create the SQLAlchemy engine using db_conn_url

        if self.db_conn_url is None:
            return

        from sqlalchemy import create_engine

        logger.info(f"Creating db_engine using db_conn_url: {self.db_conn_url}")
        db_engine = (create_engine(self.db_conn_url),)
        if isinstance(db_engine, tuple) and len(db_engine) > 0:
            self.db_engine = db_engine[0]
        else:
            self.db_engine = db_engine

    def create_db_engine_using_conn_id(self) -> None:
        # Create the SQLAlchemy engine using db_conn_id

        if self.db_conn_id is None:
            return

        try:
            from airflow.providers.postgres.hooks.postgres import PostgresHook
        except Exception as e:
            print_error(f"Error while creating db_engine using db_conn_id: {self.db_conn_id}")
            print_error(e)
            return

        logger.info(f"Creating db_engine using db_conn_id: {self.db_conn_id}")
        if self.sql_type == SqlType.POSTGRES:
            pg_hook = PostgresHook(postgres_conn_id=self.db_conn_id)
            self.db_engine = pg_hook.get_sqlalchemy_engine()

    ######################################################
    ## Write to table
    ######################################################

    def write_pandas_df(self, df: Optional[Any] = None) -> bool:
        # SqlTable not yet initialized
        if self.args is None:
            return False

        # Check name is available
        if self.name is None:
            print_error("SqlTable name not available")
            return False

        # Check engine is available
        if self.db_engine is None:
            if self.db_conn_url is not None:
                self.create_db_engine_using_conn_url()
            elif self.db_conn_id is not None:
                self.create_db_engine_using_conn_id()
            if self.db_engine is None:
                print_error("DbEngine not available")
                return False

        # write to table
        import pandas as pd

        if df is None or not isinstance(df, pd.DataFrame):
            print_error("DataFrame invalid")
            return False

        logger.debug("Writing DF to table: {}".format(self.name))
        non_null_args = {}
        if self.db_schema:
            non_null_args["schema"] = self.db_schema
        if self.index:
            non_null_args["index"] = self.index
        if self.index_label:
            non_null_args["index_label"] = self.index_label
        if self.chunksize:
            non_null_args["chunksize"] = self.chunksize
        # logger.debug(f"non_null_args: {non_null_args}")
        try:
            with self.db_engine.connect() as connection:
                df.to_sql(
                    name=self.name,
                    con=connection,
                    if_exists=self.if_exists,
                    **non_null_args,
                )
            print_info("Done")
            return True
        except Exception:
            print_error("Could not write to table: {}".format(self.name))
            raise

    ######################################################
    ## Read table
    ######################################################

    def run_sql_query(self, sql_query: str) -> Optional[Any]:
        """
        Read SQL query into a DataFrame.
        Returns a DataFrame corresponding to the result set of the query string.
        """

        # SqlTable not yet initialized
        if self.args is None:
            return False

        # Check db_engine is available
        if self.db_engine is None:
            if self.db_conn_url is not None:
                self.create_db_engine_using_conn_url()
            elif self.db_conn_id is not None:
                self.create_db_engine_using_conn_id()
            if self.db_engine is None:
                print_error("DbEngine not available")
                return False

        # run sql query
        import pandas as pd

        non_null_args = {}
        if self.index:
            non_null_args["index_col"] = self.index
        if self.chunksize:
            non_null_args["chunksize"] = self.chunksize

        print_info("Running Query:\n{}".format(sql_query))
        # logger.debug(f"non_null_args: {non_null_args}")
        try:
            with self.db_engine.connect() as connection:
                result_df = pd.read_sql_query(
                    sql=sql_query,
                    con=connection,
                    **non_null_args,
                )
            print_info("Query finished")
            return result_df
        except Exception:
            print_error("Could not run query on table: {}".format(self.name))
            raise
