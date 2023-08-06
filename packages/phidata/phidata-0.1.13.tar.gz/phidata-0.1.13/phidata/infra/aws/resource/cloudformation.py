from typing import Optional, Any, List

from botocore.exceptions import ClientError

from phidata.infra.aws.api_client import AwsApiClient
from phidata.infra.aws.resource.base import AwsResource
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class CloudFormationStack(AwsResource):
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#service-resource
    """

    resource_type = "CloudFormationStack"
    service_name = "cloudformation"

    # StackName
    # The name must be unique in the Region in which you are creating the stack.
    name: str
    # Location of file containing the template body.
    # The URL must point to a template (max size: 460,800 bytes) that's located in an
    # Amazon S3 bucket or a Systems Manager document.
    template_url: str
    # parameters: Optional[List[Dict[str, Union[str, bool]]]] = None
    # disable_rollback: Optional[bool] = None

    skip_delete = False

    def _create(self, aws_client: AwsApiClient) -> bool:
        """Creates the CloudFormationStack

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Creating {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            service_resource = self.get_service_resource(aws_client)
            # logger.debug(f"ServiceResource: {service_resource}")
            # logger.debug(f"ServiceResource type: {type(service_resource)}")

            ## Create Stack
            stack = service_resource.create_stack(
                StackName=self.name,
                TemplateURL=self.template_url,
            )
            # logger.debug(f"Stack: {stack}")
            # logger.debug(f"Stack type: {type(stack)}")

            ## Validate Stack creation
            stack.load()
            creation_time = stack.creation_time
            logger.debug(f"creation_time: {creation_time}")
            if creation_time is not None:
                print_info(f"Stack created: {stack.stack_name}")
                self.active_resource = stack
                self.active_resource_class = stack.__class__
                return True
        except Exception as e:
            print_error(e)

        print_error("Stack could not be created, this operation is known to be buggy.")
        print_error("Please deploy the workspace again.")
        return False

    def post_create(self, aws_client: AwsApiClient) -> bool:
        ## Wait for Stack to be created
        if self.wait_for_completion:
            try:
                print_info(
                    "Waiting for Stack to be created, this may take upto 5 minutes"
                )
                waiter = self.get_service_client(aws_client).get_waiter(
                    "stack_create_complete"
                )
                waiter.wait(
                    StackName=self.name,
                    WaiterConfig={
                        "Delay": self.waiter_delay,
                        "MaxAttempts": self.waiter_max_attempts,
                    },
                )
            except Exception as e:
                print_error(
                    "Received errors while waiting for Stack creation, this operation is known to be buggy."
                )
                print_error("Please try again.")
                print_error(e)
                return False
        return True

    def _read(self, aws_client: AwsApiClient) -> Optional[Any]:
        """Returns the CloudFormationStack

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        logger.debug(
            "Reading {} {}".format(self.get_resource_type(), self.get_resource_name())
        )
        try:
            service_resource = self.get_service_resource(aws_client)
            # logger.debug(f"ServiceResource: {service_resource}")
            # logger.debug(f"ServiceResource type: {type(service_resource)}")
            stack = service_resource.Stack(name=self.name)

            stack.load()
            creation_time = stack.creation_time
            logger.debug(f"creation_time: {creation_time}")
            if creation_time is not None:
                logger.debug(f"Stack found: {stack.stack_name}")
                self.active_resource = stack
                self.active_resource_class = stack.__class__
        except ClientError as ce:
            logger.debug(f"ClientError: {ce}")
            pass
        except Exception as e:
            logger.error(e)
        return self.active_resource

    def _delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the CloudFormationStack

        Args:
            aws_client: The AwsApiClient for the current cluster
        """

        logger.debug(
            "Deleting {} | {}".format(
                self.get_resource_type(), self.get_resource_name()
            )
        )
        try:
            stack = self.read(aws_client)
            # logger.debug(f"Stack: {stack}")
            # logger.debug(f"Stack type: {type(stack)}")
            self.active_resource = None
            self.active_resource_class = None
            stack.delete()
            print_info(f"Stack deleted: {stack.stack_name}")
            return True
        except Exception as e:
            logger.error(e)
        return False

    def post_delete(self, aws_client: AwsApiClient) -> bool:
        ## Wait for Stack to be deleted
        if self.wait_for_deletion:
            try:
                print_info("Waiting for Stack to be deleted")
                waiter = self.get_service_client(aws_client).get_waiter(
                    "stack_delete_complete"
                )
                waiter.wait(
                    StackName=self.name,
                    WaiterConfig={
                        "Delay": self.waiter_delay,
                        "MaxAttempts": self.waiter_max_attempts,
                    },
                )
                return True
            except Exception as e:
                print_error(
                    "Received errors while waiting for Stack deletion, this operation is known to be buggy."
                )
                print_error("Please try again or delete resources manually.")
                print_error(e)
        return True

    def get_stack_resource(
        self, aws_client: AwsApiClient, logical_id: str
    ) -> Optional[Any]:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.StackResource
        # logger.debug(f"Getting StackResource {logical_id} for {self.name}")
        try:
            service_resource = self.get_service_resource(aws_client)
            stack_resource = service_resource.StackResource(self.name, logical_id)
            return stack_resource
        except Exception as e:
            logger.error(e)
        return None

    def get_private_subnets(self, aws_client: AwsApiClient) -> Optional[List[str]]:
        try:
            private_subnet_1_stack_resource = self.get_stack_resource(
                aws_client, "PrivateSubnet01"
            )
            private_subnet_1_physical_resource_id = (
                private_subnet_1_stack_resource.physical_resource_id
                if private_subnet_1_stack_resource is not None
                else None
            )
            # logger.debug(f"private_subnet_1: {private_subnet_1_physical_resource_id}")
            private_subnet_2_stack_resource = self.get_stack_resource(
                aws_client, "PrivateSubnet02"
            )
            private_subnet_2_physical_resource_id = (
                private_subnet_2_stack_resource.physical_resource_id
                if private_subnet_2_stack_resource is not None
                else None
            )
            # logger.debug(f"private_subnet_2: {private_subnet_2_physical_resource_id}")

            private_subnets = []
            if private_subnet_1_physical_resource_id is not None:
                private_subnets.append(private_subnet_1_physical_resource_id)
            if private_subnet_2_physical_resource_id is not None:
                private_subnets.append(private_subnet_2_physical_resource_id)

            return private_subnets if (len(private_subnets) > 0) else None
        except Exception as e:
            logger.error(e)
        return None

    def get_public_subnets(self, aws_client: AwsApiClient) -> Optional[List[str]]:
        try:
            public_subnet_1_stack_resource = self.get_stack_resource(
                aws_client, "PublicSubnet01"
            )
            public_subnet_1_physical_resource_id = (
                public_subnet_1_stack_resource.physical_resource_id
                if public_subnet_1_stack_resource is not None
                else None
            )
            # logger.debug(f"public_subnet_1: {public_subnet_1_physical_resource_id}")
            public_subnet_2_stack_resource = self.get_stack_resource(
                aws_client, "PublicSubnet02"
            )
            public_subnet_2_physical_resource_id = (
                public_subnet_2_stack_resource.physical_resource_id
                if public_subnet_2_stack_resource is not None
                else None
            )
            # logger.debug(f"public_subnet_2: {public_subnet_2_physical_resource_id}")

            public_subnets = []
            if public_subnet_1_physical_resource_id is not None:
                public_subnets.append(public_subnet_1_physical_resource_id)
            if public_subnet_2_physical_resource_id is not None:
                public_subnets.append(public_subnet_2_physical_resource_id)

            return public_subnets if (len(public_subnets) > 0) else None
        except Exception as e:
            logger.error(e)
        return None
