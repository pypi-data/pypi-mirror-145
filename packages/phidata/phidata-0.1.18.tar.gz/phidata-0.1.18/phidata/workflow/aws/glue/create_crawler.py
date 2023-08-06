from typing import Optional

from phidata.asset.aws.glue.crawler import GlueCrawler
from phidata.utils.log import logger
from phidata.workflow.py.python_workflow_base import (
    PythonWorkflowBase,
    PythonWorkflowBaseArgs,
)


class CreateGlueCrawlerArgs(PythonWorkflowBaseArgs):
    crawler: GlueCrawler
    start_crawler: bool = False


class CreateGlueCrawler(PythonWorkflowBase):
    def __init__(
        self,
        crawler: GlueCrawler,
        start_crawler: bool = False,
        name: str = "create_glue_crawler",
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ):
        super().__init__()
        try:
            self.args: CreateGlueCrawlerArgs = CreateGlueCrawlerArgs(
                crawler=crawler,
                start_crawler=start_crawler,
                name=name,
                task_id=task_id,
                dag_id=dag_id,
                version=version,
                enabled=enabled,
                entrypoint=create_glue_crawler,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def crawler(self) -> GlueCrawler:
        return self.args.crawler

    @crawler.setter
    def crawler(self, crawler: GlueCrawler) -> None:
        if crawler is not None:
            self.args.crawler = crawler

    @property
    def start_crawler(self) -> bool:
        return self.args.start_crawler

    @start_crawler.setter
    def start_crawler(self, start_crawler: bool) -> None:
        if start_crawler is not None:
            self.args.start_crawler = start_crawler


def create_glue_crawler(**kwargs) -> bool:

    args: CreateGlueCrawlerArgs = CreateGlueCrawlerArgs(**kwargs)
    # logger.debug("CreateGlueCrawlerArgs: {}".format(args))

    create_success = args.crawler.create_crawler()
    if create_success:
        logger.info("Create GlueCrawler: success")
        if args.start_crawler:
            logger.info(f"Starting GlueCrawler")
            start_success = args.crawler.start_crawler()
            if start_success:
                logger.info("GlueCrawler started")
            return start_success
    return create_success
