from typing import Optional, Any, Dict, List

from botocore.exceptions import ClientError

from phidata.infra.aws.api_client import AwsApiClient
from phidata.infra.aws.resource.base import AwsResource
from phidata.infra.aws.resource.iam.role import IamRole
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class GlueCrawlerResource(AwsResource):
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html
    """

    resource_type = "GlueCrawlerResource"
    service_name = "glue"

    # Name of the crawler.
    name: str
    # The IAM role for the crawler
    iam_role: IamRole
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

    def _create(self, aws_client: AwsApiClient) -> bool:
        """Creates the GlueCrawlerResource

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Creating {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            # create a dict of args which are not null, otherwise aws type validation fails
            non_null_args = {}
            if self.database_name:
                non_null_args["DatabaseName"] = self.database_name
            if self.description:
                non_null_args["Description"] = self.description
            if self.targets:
                non_null_args["Targets"] = self.targets
            if self.schedule:
                non_null_args["Schedule"] = self.schedule
            if self.classifiers:
                non_null_args["Classifiers"] = self.classifiers
            if self.table_prefix:
                non_null_args["TablePrefix"] = self.table_prefix
            if self.schema_change_policy:
                non_null_args["SchemaChangePolicy"] = self.schema_change_policy
            if self.recrawl_policy:
                non_null_args["RecrawlPolicy"] = self.recrawl_policy
            if self.lineage_configuration:
                non_null_args["LineageConfiguration"] = self.lineage_configuration
            if self.lake_formation_configuration:
                non_null_args[
                    "LakeFormationConfiguration"
                ] = self.lake_formation_configuration
            if self.configuration:
                non_null_args["Configuration"] = self.configuration
            if self.crawler_security_configuration:
                non_null_args[
                    "CrawlerSecurityConfiguration"
                ] = self.crawler_security_configuration
            if self.tags:
                non_null_args["Tags"] = self.tags

            ## Create crawler
            # Get the service_client
            service_client = self.get_service_client(aws_client)
            # logger.debug(f"ServiceClient: {service_client}")
            # logger.debug(f"ServiceClient type: {type(service_client)}")
            try:
                print_info(f"Creating GlueCrawlerResource: {self.name}")
                iam_role_arn = self.iam_role.get_arn(aws_client)
                create_crawler_response = service_client.create_crawler(
                    Name=self.name,
                    Role=iam_role_arn,
                    **non_null_args,
                )
                # logger.debug(f"GlueCrawlerResource: {create_crawler_response}")
                # logger.debug(f"GlueCrawlerResource type: {type(create_crawler_response)}")

                if create_crawler_response is not None:
                    print_info(f"GlueCrawlerResource created: {self.name}")
                    self.active_resource = create_crawler_response
                    return True
            except Exception as e:
                print_error(
                    "GlueCrawlerResource could not be created, this operation is known to be buggy."
                )
                print_error("Please try again.")
                print_error(e)
                return False
        except Exception as e:
            print_error(
                f"Received error while creating {self.get_resource_type()}, this operation is known to be buggy."
            )
            print_error("Please try again.")
            print_error(e)
        return False

    def _read(self, aws_client: AwsApiClient) -> Optional[Any]:
        """Returns the GlueCrawlerResource

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        logger.debug(
            "Reading {} {}".format(self.get_resource_type(), self.get_resource_name())
        )
        try:
            service_client = self.get_service_client(aws_client)
            get_crawler_response = service_client.get_crawler(Name=self.name)
            # logger.debug(f"GlueCrawlerResource: {get_crawler_response}")
            # logger.debug(f"GlueCrawlerResource type: {type(get_crawler_response)}")

            creation_time = get_crawler_response.get("Crawler", {}).get(
                "CreationTime", None
            )
            last_crawl = get_crawler_response.get("Crawler", {}).get("LastCrawl", None)
            logger.debug(f"GlueCrawlerResource creation_time: {creation_time}")
            # logger.debug(f"GlueCrawlerResource last_crawl: {last_crawl}")
            if creation_time is not None:
                logger.debug(f"GlueCrawlerResource found: {self.name}")
                self.active_resource = get_crawler_response
        except ClientError as ce:
            logger.debug(f"ClientError: {ce}")
            pass
        except Exception as e:
            print_error(f"Received error while reading {self.get_resource_type()}.")
            print_error("Please try again.")
            print_error(e)
        return self.active_resource

    def _delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the GlueCrawlerResource

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Deleting {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            # Delete the GlueCrawlerResource
            service_client = self.get_service_client(aws_client)
            self.active_resource = None
            delete_crawler_response = service_client.delete_crawler(Name=self.name)
            logger.debug(f"GlueCrawlerResource: {delete_crawler_response}")
            logger.debug(f"GlueCrawlerResource type: {type(delete_crawler_response)}")
            print_info(f"GlueCrawlerResource deleted: {self.name}")
            return True
        except Exception as e:
            print_error(
                f"Received error while deleting {self.get_resource_type()}, this operation is known to be buggy."
            )
            print_error("Please try again or delete resources manually.")
            print_error(e)
        return False

    def start_crawler(self, aws_client: AwsApiClient) -> bool:
        """Runs the GlueCrawlerResource

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Running {} | {}".format(self.get_resource_type(), self.get_resource_name())
        )
        try:
            # Get the service_client
            service_client = self.get_service_client(aws_client)
            # logger.debug(f"ServiceClient: {service_client}")
            # logger.debug(f"ServiceClient type: {type(service_client)}")
            start_crawler_response = service_client.start_crawler(Name=self.name)
            # logger.debug(f"start_crawler_response: {start_crawler_response}")

            if start_crawler_response is not None:
                return True
        except Exception as e:
            print_error("GlueCrawler could not be started")
            print_error("Please try again.")
            print_error(e)
        return False
