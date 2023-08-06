from typing import Optional, Union, Sequence
from typing_extensions import Literal

from sqlalchemy.engine import Engine, Connection

from phidata.asset.table.sql import SqlTable, SqlTableArgs, SqlType
from phidata.utils.cli_console import print_info, print_error


class PostgresTableArgs(SqlTableArgs):
    # Table Name
    name: str
    sql_type: SqlType = SqlType.POSTGRES


class PostgresTable(SqlTable):
    def __init__(
        self,
        # Table Name
        name: str,
        db_conn_id: Optional[str] = None,
        db_conn_url: Optional[str] = None,
        db_engine: Optional[Union[Engine, Connection]] = None,
        if_exists: Literal["fail", "replace", "append"] = "replace",
        db_schema: Optional[str] = None,
        index: bool = None,
        index_label: Optional[Union[str, Sequence]] = None,
        chunksize: Optional[int] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: PostgresTableArgs = PostgresTableArgs(
                name=name,
                db_conn_id=db_conn_id,
                db_conn_url=db_conn_url,
                db_engine=db_engine,
                if_exists=if_exists,
                db_schema=db_schema,
                index=index,
                index_label=index_label,
                chunksize=chunksize,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            print_error(f"Args for {self.__class__.__name__} are not valid")
            raise
