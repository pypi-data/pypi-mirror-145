from typing import Optional, List, Dict

from pydantic import BaseModel

from phidata.asset.aws import AwsAsset, AwsAssetArgs
from phidata.infra.aws.resource.s3 import S3Bucket
from phidata.infra.aws.resource.iam.role import IamRole
from phidata.infra.aws.resource.glue.crawler import GlueCrawlerResource
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class GlueS3Target(BaseModel):
    # The directory path in the S3 bucket to target
    dir: str = ""
    # The s3 bucket to target
    bucket: S3Bucket
    # A list of glob patterns used to exclude from the crawl.
    # For more information, see https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html
    exclusions: Optional[List[str]] = None
    # The name of a connection which allows a job or crawler to access data in Amazon S3 within an
    # Amazon Virtual Private Cloud environment (Amazon VPC).
    connection_name: Optional[str] = None
    # Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset.
    # If not set, all the files are crawled. A valid value is an integer between 1 and 249.
    sample_size: Optional[int] = None
    # A valid Amazon SQS ARN. For example, arn:aws:sqs:region:account:sqs .
    event_queue_arn: Optional[str] = None
    # A valid Amazon dead-letter SQS ARN. For example, arn:aws:sqs:region:account:deadLetterQueue .
    dlq_event_queue_arn: Optional[str] = None


class GlueCrawlerArgs(AwsAssetArgs):
    # Name of the crawler.
    name: str
    # The IAM role for the crawler
    iam_role: IamRole
    # List of GlueS3Target to add to the targets dict
    s3_targets: Optional[List[GlueS3Target]] = None
    # The Glue database where results are written,
    # such as: arn:aws:daylight:us-east-1::database/sometable/* .
    database_name: Optional[str] = None
    # A description of the new crawler.
    description: Optional[str] = None
    # A list of collection of targets to crawl.
    targets: Optional[Dict[str, List[dict]]] = None
    # A cron expression used to specify the schedule
    # For example, to run something every day at 12:15 UTC,
    # you would specify: cron(15 12 * * ? *) .
    schedule: Optional[str] = None
    # A list of custom classifiers that the user has registered.
    # By default, all built-in classifiers are included in a crawl,
    # but these custom classifiers always override the default classifiers for a given classification.
    classifiers: Optional[List[str]] = None
    # The table prefix used for catalog tables that are created.
    table_prefix: Optional[str] = None
    # The policy for the crawler's update and deletion behavior.
    schema_change_policy: Optional[Dict[str, str]] = None
    # A policy that specifies whether to crawl the entire dataset again,
    # or to crawl only folders that were added since the last crawler run.
    recrawl_policy: Optional[Dict[str, str]] = None
    lineage_configuration: Optional[Dict[str, str]] = None
    lake_formation_configuration: Optional[Dict[str, str]] = None
    # Crawler configuration information. This versioned JSON string
    # allows users to specify aspects of a crawler's behavior.
    configuration: Optional[str] = None
    # The name of the SecurityConfiguration structure to be used by this crawler.
    crawler_security_configuration: Optional[str] = None
    # The tags to use with this crawler request.
    tags: Optional[Dict[str, str]] = None

    ## Resource management
    # If True, skip resource creation if active resources with the same name exist.
    use_cache: bool = True
    # If True, logs extra debug messages
    use_verbose_logs: bool = False
    # If True, does not create the resource when `phi ws up` command is run
    skip_create: bool = False
    # If True, does not delete the resource when `phi ws down` command is run
    skip_delete: bool = False


class GlueCrawler(AwsAsset):
    def __init__(
        self,
        # Name of the crawler.
        name: str,
        # The IAM role for the crawler
        iam_role: IamRole,
        # List of GlueS3Target to add to the targets dict
        s3_targets: Optional[List[GlueS3Target]] = None,
        # The Glue database where results are written,
        # such as: arn:aws:daylight:us-east-1::database/sometable/* .
        database_name: Optional[str] = None,
        # A description of the new crawler.
        description: Optional[str] = None,
        # A list of collection of targets to crawl.
        targets: Optional[Dict[str, List[dict]]] = None,
        # A cron expression used to specify the schedule
        # For example, to run something every day at 12:15 UTC,
        # you would specify: cron(15 12 * * ? *) .,
        schedule: Optional[str] = None,
        # A list of custom classifiers that the user has registered.
        # By default, all built-in classifiers are included in a crawl,
        # but these custom classifiers always override the default classifiers for a given classification.
        classifiers: Optional[List[str]] = None,
        # The table prefix used for catalog tables that are created.
        table_prefix: Optional[str] = None,
        # The policy for the crawler's update and deletion behavior.
        schema_change_policy: Optional[Dict[str, str]] = None,
        # A policy that specifies whether to crawl the entire dataset again,
        # or to crawl only folders that were added since the last crawler run.
        recrawl_policy: Optional[Dict[str, str]] = None,
        lineage_configuration: Optional[Dict[str, str]] = None,
        lake_formation_configuration: Optional[Dict[str, str]] = None,
        # Crawler configuration information. This versioned JSON string
        # allows users to specify aspects of a crawler's behavior.
        configuration: Optional[str] = None,
        # The name of the SecurityConfiguration structure to be used by this crawler.
        crawler_security_configuration: Optional[str] = None,
        # The tags to use with this crawler request.
        tags: Optional[Dict[str, str]] = None,
        ## Resource management
        # If True, skip resource creation if active resources with the same name exist.
        use_cache: bool = True,
        # If True, logs extra debug messages
        use_verbose_logs: bool = False,
        # If True, does not create the resource when `phi ws up` command is run
        skip_create: bool = False,
        # If True, does not delete the resource when `phi ws down` command is run
        skip_delete: bool = False,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: GlueCrawlerArgs = GlueCrawlerArgs(
                name=name,
                iam_role=iam_role,
                s3_targets=s3_targets,
                database_name=database_name,
                description=description,
                targets=targets,
                schedule=schedule,
                classifiers=classifiers,
                table_prefix=table_prefix,
                schema_change_policy=schema_change_policy,
                recrawl_policy=recrawl_policy,
                lineage_configuration=lineage_configuration,
                lake_formation_configuration=lake_formation_configuration,
                configuration=configuration,
                crawler_security_configuration=crawler_security_configuration,
                tags=tags,
                use_cache=use_cache,
                use_verbose_logs=use_verbose_logs,
                skip_create=skip_create,
                skip_delete=skip_delete,
                version=version,
                enabled=enabled,
            )
            self._glue_crawler_resource: Optional[GlueCrawlerResource] = None
        except Exception as e:
            print_error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def glue_crawler_resource(self) -> GlueCrawlerResource:
        # use cached value if available
        if self._glue_crawler_resource:
            return self._glue_crawler_resource

        # Create GlueCrawlerResource
        logger.debug("Initializing GlueCrawlerResource")
        try:
            # Update crawler targets
            # start with user provided targets
            crawler_targets: Optional[Dict[str, List[dict]]] = self.args.targets

            # Add GlueS3Targets to crawler_targets
            if self.args.s3_targets is not None:
                # create S3Targets dicts using s3_targets
                new_s3_targets_list: List[dict] = []
                for s3_target in self.args.s3_targets:
                    _new_s3_target_path = (
                        f"s3://{s3_target.bucket.name}/{s3_target.dir}"
                    )
                    # start with the only required argument
                    _new_s3_target_dict = {"Path": _new_s3_target_path}
                    # add any optional arguments
                    if s3_target.exclusions is not None:
                        _new_s3_target_dict["Exclusions"] = s3_target.exclusions
                    if s3_target.connection_name is not None:
                        _new_s3_target_dict[
                            "ConnectionName"
                        ] = s3_target.connection_name
                    if s3_target.sample_size is not None:
                        _new_s3_target_dict["SampleSize"] = s3_target.sample_size
                    if s3_target.event_queue_arn is not None:
                        _new_s3_target_dict["EventQueueArn"] = s3_target.event_queue_arn
                    if s3_target.dlq_event_queue_arn is not None:
                        _new_s3_target_dict[
                            "DlqEventQueueArn"
                        ] = s3_target.dlq_event_queue_arn

                    new_s3_targets_list.append(_new_s3_target_dict)

                # Add new S3Targets to crawler_targets
                if crawler_targets is None:
                    crawler_targets = {}
                # logger.debug(f"new_s3_targets_list: {new_s3_targets_list}")
                existing_s3_targets = crawler_targets.get("S3Targets", [])
                # logger.debug(f"existing_s3_targets: {existing_s3_targets}")
                new_s3_targets = existing_s3_targets + new_s3_targets_list
                # logger.debug(f"new_s3_targets: {new_s3_targets}")
                crawler_targets["S3Targets"] = new_s3_targets

            # TODO: add more targets as needed
            logger.debug(f"GlueCrawler targets: {crawler_targets}")

            self._glue_crawler_resource = GlueCrawlerResource(
                name=self.args.name,
                iam_role=self.args.iam_role,
                database_name=self.args.database_name,
                description=self.args.description,
                targets=crawler_targets,
                schedule=self.args.schedule,
                classifiers=self.args.classifiers,
                table_prefix=self.args.table_prefix,
                schema_change_policy=self.args.schema_change_policy,
                recrawl_policy=self.args.recrawl_policy,
                lineage_configuration=self.args.lineage_configuration,
                lake_formation_configuration=self.args.lake_formation_configuration,
                configuration=self.args.configuration,
                crawler_security_configuration=self.args.crawler_security_configuration,
                tags=self.args.tags,
                use_cache=self.args.use_cache,
                use_verbose_logs=self.args.use_verbose_logs,
                skip_create=self.args.skip_create,
                skip_delete=self.args.skip_delete,
            )
            return self._glue_crawler_resource
        except Exception as e:
            print_error(f"Could not create GlueCrawlerResource")
            raise

    ######################################################
    ## Create GlueCrawler
    ######################################################

    def create_crawler(self) -> bool:

        # GlueCrawler not yet initialized
        if self.args is None:
            return False

        from phidata.infra.aws.api_client import AwsApiClient

        try:
            # aws_region, aws_profile loaded from local env if provided
            # by WorkspaceConfig
            aws_api_client = AwsApiClient(
                aws_region=self.aws_region,
                aws_profile=self.aws_profile,
            )
            glue_crawler_resource = self.glue_crawler_resource
            create_success = glue_crawler_resource.create(aws_api_client)
            return create_success
        except Exception as e:
            print_error("Could not create GlueCrawler, please try again")
            print_info("--- stacktrace ---")
            logger.exception(e)
            print_info("--- stacktrace ---")
        return False

    ######################################################
    ## Start GlueCrawler
    ######################################################

    def start_crawler(self) -> bool:

        # GlueCrawler not yet initialized
        if self.args is None:
            return False

        from phidata.infra.aws.api_client import AwsApiClient

        try:
            aws_api_client = AwsApiClient(
                aws_region=self.aws_region,
                aws_profile=self.aws_profile,
            )
            glue_crawler_resource = self.glue_crawler_resource
            active_glue_crawler_resource = glue_crawler_resource.read(aws_api_client)
            if active_glue_crawler_resource is None:
                print_error("No GlueCrawler available")
                return False

            start_success = glue_crawler_resource.start_crawler(aws_api_client)
            return start_success
        except Exception as e:
            print_error("Could not start GlueCrawler, please try again")
            print_info("--- stacktrace ---")
            logger.exception(e)
            print_info("--- stacktrace ---")
        return False
