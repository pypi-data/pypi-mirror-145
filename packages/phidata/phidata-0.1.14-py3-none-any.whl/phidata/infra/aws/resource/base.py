from typing import Any, Optional

from phidata.infra.base.resource import InfraResource
from phidata.infra.aws.api_client import AwsApiClient
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class AwsResource(InfraResource):
    """Base class for Aws Resources"""

    service_name: str
    service_client: Optional[Any] = None
    service_resource: Optional[Any] = None

    resource_available: Optional[bool] = None
    resource_updated: Optional[bool] = None
    resource_deleted: Optional[bool] = None

    def is_valid(self) -> bool:
        # Resources can add validation checks here
        return True

    def get_service_client(self, aws_client: AwsApiClient):
        if self.service_client is None:
            self.service_client = aws_client.boto3_session.client(
                service_name=self.service_name, region_name=aws_client.aws_region
            )
        return self.service_client

    def get_service_resource(self, aws_client: AwsApiClient):
        if self.service_resource is None:
            self.service_resource = aws_client.boto3_session.resource(
                service_name=self.service_name, region_name=aws_client.aws_region
            )
        return self.service_resource

    def _create(self, aws_client: AwsApiClient) -> bool:
        logger.error(f"@_create method not defined for {self.__class__.__name__}")
        return False

    def create(self, aws_client: AwsApiClient) -> bool:
        """Creates the resource on the Aws Cluster

        Args:
            aws_client: The AwsApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        # Skip resource creation if skip_create = True
        if self.skip_create:
            print_info(f"Skipping create: {self.get_resource_name()}")
            return True
        if self.use_cache and self.is_active(aws_client):
            self.resource_available = True
            print_info(
                f"{self.get_resource_type()}: {self.get_resource_name()} available"
            )
        else:
            self.resource_available = self._create(aws_client)
        if self.resource_available:
            # print_info(
            #     f"Running post-create steps for {self.get_resource_type()}: {self.get_resource_name()}."
            # )
            return self.post_create(aws_client)
        return self.resource_available

    def post_create(self, aws_client: AwsApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def _read(self, aws_client: AwsApiClient) -> Any:
        logger.error(f"@_read method not defined for {self.__class__.__name__}")
        return False

    def read(self, aws_client: AwsApiClient) -> Any:
        """Reads the resource from the Aws Cluster

        Args:
            aws_client: The AwsApiClient for the current Cluster
        """
        if not self.is_valid():
            return None
        if self.use_cache and self.active_resource is not None:
            return self.active_resource
        return self._read(aws_client)

    def _update(self, aws_client: AwsApiClient) -> Any:
        logger.error(f"@_update method not defined for {self.__class__.__name__}")
        return False

    def update(self, aws_client: AwsApiClient) -> bool:
        """Updates the resource on the Aws Cluster

        Args:
            aws_client: The AwsApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        if self.is_active(aws_client):
            self.resource_updated = self._update(aws_client)
        else:
            print_info(
                f"{self.get_resource_type()}: {self.get_resource_name()} not active."
            )
            return True
        if self.resource_updated:
            # print_info(
            #     f"Running post-update steps for {self.get_resource_type()}: {self.get_resource_name()}."
            # )
            return self.post_update(aws_client)
        return self.resource_updated

    def post_update(self, aws_client: AwsApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def _delete(self, aws_client: AwsApiClient) -> Any:
        logger.error(f"@_delete method not defined for {self.__class__.__name__}")
        return False

    def delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the resource from the Aws Cluster

        Args:
            aws_client: The AwsApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        # Skip resource deletion if skip_delete = True
        if self.skip_delete:
            print_info(f"Skipping delete: {self.get_resource_name()}")
            return True
        if self.is_active(aws_client):
            self.resource_deleted = self._delete(aws_client)
        else:
            print_info(
                f"{self.get_resource_type()}: {self.get_resource_name()} not active."
            )
            return True
        if self.resource_deleted:
            # print_info(
            #     f"Running post-delete steps for {self.get_resource_type()}: {self.get_resource_name()}."
            # )
            return self.post_delete(aws_client)
        return self.resource_deleted

    def post_delete(self, aws_client: AwsApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def is_active(self, aws_client: AwsApiClient) -> bool:
        """Returns True if the resource is active on the Aws Cluster"""
        active_resource = self.read(aws_client=aws_client)
        if active_resource is not None:
            return True
        return False
