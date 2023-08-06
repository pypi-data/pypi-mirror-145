from pathlib import Path
from typing import Optional

from phidata.asset.file import File
from phidata.asset.aws import AwsAsset, AwsAssetArgs
from phidata.infra.aws.resource.s3 import S3Bucket
from phidata.utils.cli_console import print_info, print_error
from phidata.utils.log import logger


class S3ObjectArgs(AwsAssetArgs):
    key: str
    bucket: S3Bucket
    fail_if_object_exists: bool = False


class S3Object(AwsAsset):
    def __init__(
        self,
        key: str,
        bucket: S3Bucket,
        fail_if_object_exists: bool = False,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:

        super().__init__()
        try:
            self.args: S3ObjectArgs = S3ObjectArgs(
                key=key,
                bucket=bucket,
                name=key,
                fail_if_object_exists=fail_if_object_exists,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            print_error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def key(self) -> str:
        return self.args.key

    @key.setter
    def key(self, key: str) -> None:
        if key is not None:
            self.args.key = key

    @property
    def bucket(self) -> S3Bucket:
        return self.args.bucket

    @bucket.setter
    def bucket(self, bucket: S3Bucket) -> None:
        if bucket is not None:
            self.args.bucket = bucket

    ######################################################
    ## Write to s3
    ######################################################

    def write_file(self, file: File) -> bool:

        ######################################################
        ## Validate
        ######################################################

        # S3Object not yet initialized
        if self.args is None:
            return False

        # Check file_path is available
        file_path: Optional[Path] = file.file_path
        if file_path is None or not isinstance(file_path, Path):
            print_error("FilePath invalid")
            return False

        bucket_name = self.bucket.name
        object_key = self.args.key
        print_info("Uploading")
        print_info(f"  File: {file_path}")
        print_info(f"  To  : {bucket_name}/{object_key}")

        ######################################################
        ## Upload
        ######################################################
        import botocore.exceptions
        from phidata.infra.aws.api_client import AwsApiClient

        try:
            # aws_region, aws_profile loaded from local env if provided
            # by WorkspaceConfig
            aws_api_client = AwsApiClient(
                aws_region=self.aws_region,
                aws_profile=self.aws_profile,
            )
            s3_bucket = self.bucket.read(aws_api_client)
            # logger.info("Bucket: {}".format(s3_bucket))
            # logger.info("Bucket type: {}".format(type(s3_bucket)))

            if s3_bucket is None:
                print_error(
                    f"Could not find bucket: {bucket_name}. Please confirm it exists."
                )
                return False

            # upload file to bucket
            s3_object_size = 0
            s3_object = s3_bucket.Object(key=object_key)
            try:
                s3_object.load()
                s3_object_size = s3_object.content_length
                # logger.info("s3_object_size: {}".format(s3_object_size))
            except botocore.exceptions.ClientError as e:
                pass
            if s3_object_size >= 1 and self.args.fail_if_object_exists:
                logger.info(f"Object {bucket_name}/{object_key} already exists")
                return False
            # logger.info("s3_object type: {}".format(type(s3_object)))
            # logger.info("s3_object: {}".format(s3_object))

            logger.info("Uploading S3Object")
            s3_object.upload_file(Filename=str(file_path.resolve()))
            logger.info("S3Object uploaded")
            return True
        except Exception as e:
            print_error("Could not upload S3Object, please try again")
            print_info("--- stacktrace ---")
            logger.exception(e)
            print_info("--- stacktrace ---")
        return False
