from typing import Optional, Dict, Any, List, Union

from phidata.asset.file import File
from phidata.asset.table.sql import SqlTable
from phidata.workflow.output_type import OutputType
from phidata.workflow.py import PythonWorkflow, PythonWorkflowArgs, EngineType
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class GetTickerPriceArgs(PythonWorkflowArgs):
    # Args provided by user
    tickers: Optional[Union[str, List[str]]] = None
    # start_date: Start of ticker range in YYYY-MM-DD format.
    start_date: Optional[str] = None
    # end_date: End of ticker range in YYYY-MM-DD format.
    end_date: Optional[str] = None
    frequency: str = "daily"
    response_format: str = "json"
    # valid options = {'open', 'high', 'low', 'close', 'volume',
    # 'adjOpen', 'adjHigh', 'adjLow', 'adjClose', 'adjVolume',
    # 'divCash', 'splitFactor'}
    # metric: Optional[str] = None
    # sort: Optional[str]
    # columns: Optional[List[str]]
    use_session: bool = True
    api_key: Optional[str] = None
    # Required
    output_to: Optional[OutputType] = None
    file: Optional[File] = None
    sql_table: Optional[SqlTable] = None
    # Used by this workflow
    tiingo_config: Optional[Dict[str, Any]]


class GetTickerPrice(PythonWorkflow):
    def __init__(
        self,
        tickers: Optional[Union[str, List[str]]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        frequency: str = "daily",
        response_format: str = "json",
        use_session: bool = True,
        api_key: Optional[str] = None,
        output_to: Optional[OutputType] = None,
        file: Optional[File] = None,
        sql_table: Optional[SqlTable] = None,
        engine: Optional[EngineType] = EngineType.PANDAS,
        name: Optional[str] = "get_ticker_price",
        version: Optional[str] = None,
        enabled: bool = True,
    ):

        super().__init__()
        try:
            self.args: GetTickerPriceArgs = GetTickerPriceArgs(
                tickers=tickers,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                response_format=response_format,
                use_session=use_session,
                api_key=api_key,
                output_to=output_to,
                file=file,
                sql_table=sql_table,
                engine=engine,
                entrypoint=get_ticker_price_entrypoint,
                name=name or "get_ticker_price",
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            logger.error("Exception building GetTickerPrice")
            raise


def get_ticker_price_entrypoint(**kwargs) -> bool:

    args: GetTickerPriceArgs = GetTickerPriceArgs(**kwargs)
    # logger.debug("GetTickerPriceArgs: {}".format(args))

    if args.api_key is None:
        print_error("ApiKey required")
        return False

    if args.tickers is None:
        print_error("Ticker required")
        return False

    if args.response_format != "json":
        print_error("Only JSON response supported")
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

    tickers = args.tickers
    ticker_price_df = pd.DataFrame()
    if isinstance(tickers, list):
        for ticker in tickers:
            _price_df: pd.DataFrame = tiingo_client.get_dataframe(
                tickers=ticker,
                startDate=args.start_date,
                endDate=args.end_date,
                frequency=args.frequency,
                fmt=args.response_format,
            )
            # logger.debug("_price_df:")
            # logger.debug(_price_df)
            _price_df["ticker"] = ticker
            ticker_price_df = ticker_price_df.append(_price_df)
    else:
        ticker_price_df = tiingo_client.get_dataframe(
            tickers=tickers,
            startDate=args.start_date,
            endDate=args.end_date,
            frequency=args.frequency,
            fmt=args.response_format,
        )
        ticker_price_df["ticker"] = args.tickers

    ticker_price_df.reset_index(inplace=True)
    ticker_price_df.set_index(["date", "ticker"], inplace=True)
    # logger.debug("ticker_price_df:")
    # logger.debug(ticker_price_df)
    # logger.debug("index: {}".format(ticker_price_df.index))

    if output_to == OutputType.FILE:
        if args.file is None:
            print_error("File invalid")
            return False

        args.file.write_pandas_df(ticker_price_df)
    elif output_to == OutputType.SQL_TABLE:
        if args.sql_table is None:
            print_error("SqlTable invalid")
            return False

        args.sql_table.write_pandas_df(ticker_price_df)

    return True
