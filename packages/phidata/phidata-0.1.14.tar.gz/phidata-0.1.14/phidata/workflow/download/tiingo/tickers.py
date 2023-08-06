from typing import Optional, Dict, Any, List, Union

from phidata.asset.file import File
from phidata.asset.table.sql import SqlTable
from phidata.workflow.output_type import OutputType
from phidata.workflow.py import PythonWorkflow, PythonWorkflowArgs, EngineType
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class GetTickersArgs(PythonWorkflowArgs):
    # Args provided by user
    # ['Stock', 'ETF', 'Mutual Fund']
    asset_types: List[str] = []
    use_session: bool = True
    api_key: Optional[str] = None
    # Required
    output_to: Optional[OutputType] = None
    file: Optional[File] = None
    sql_table: Optional[SqlTable] = None
    # Used by this workflow
    tiingo_config: Optional[Dict[str, Any]]


class GetTickers(PythonWorkflow):
    def __init__(
        self,
        asset_types: Optional[List[str]] = None,
        use_session: bool = True,
        api_key: Optional[str] = None,
        output_to: Optional[OutputType] = None,
        file: Optional[File] = None,
        sql_table: Optional[SqlTable] = None,
        engine: Optional[EngineType] = EngineType.PANDAS,
        name: Optional[str] = "get_tickers",
        version: Optional[str] = None,
        enabled: bool = True,
    ):

        super().__init__()
        try:
            self.args: GetTickersArgs = GetTickersArgs(
                asset_types=asset_types or [],
                use_session=use_session,
                api_key=api_key,
                output_to=output_to,
                file=file,
                sql_table=sql_table,
                engine=engine,
                entrypoint=get_tickers_entrypoint,
                name=name or "get_tickers",
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            logger.error("Exception building GetTickers")
            raise


def get_tickers_entrypoint(**kwargs) -> bool:

    args: GetTickersArgs = GetTickersArgs(**kwargs)
    # logger.debug("GetTickersArgs: {}".format(args))

    if args.api_key is None:
        print_error("ApiKey required")
        return False

    if args.engine != EngineType.PANDAS:
        print_error("Only PANDAS engine supported")
        return False

    if args.output_to is None or not isinstance(args.output_to, OutputType):
        print_error("OutputType invalid")
        return False
    output_to = args.output_to

    import pandas as pd
    from tiingo import TiingoClient

    tiingo_config: Dict[str, Any] = {
        "session": args.use_session or True,
        "api_key": args.api_key,
    }
    tiingo_client: TiingoClient = TiingoClient(tiingo_config)

    # tickers_df = tiingo_client.list_tickers(assetTypes=args.asset_types)
    list_tickers_response = tiingo_client.list_stock_tickers()
    # logger.debug("list_tickers_response:")
    # logger.debug("list_tickers_response type: {}".format(type(list_tickers_response)))
    # logger.debug(list_tickers_response[:5])
    tickers_df = pd.DataFrame(list_tickers_response)
    tickers_df.rename(
        columns={
            "assetType": "asset_type",
            "priceCurrency": "price_currency",
            "startDate": "start_date",
            "endDate": "end_date",
        },
        inplace=True,
    )
    # logger.debug("tickers_df:")
    # logger.debug(tickers_df[:5])
    logger.debug("# tickers: {}".format(len(tickers_df)))

    if output_to == OutputType.FILE:
        if args.file is None:
            print_error("File invalid")
            return False

        args.file.write_pandas_df(tickers_df)
    elif output_to == OutputType.SQL_TABLE:
        if args.sql_table is None:
            print_error("SqlTable invalid")
            return False

        args.sql_table.write_pandas_df(tickers_df)

    return True
