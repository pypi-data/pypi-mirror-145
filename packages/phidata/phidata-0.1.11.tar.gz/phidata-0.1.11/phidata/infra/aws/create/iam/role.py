import json

from typing import List, Optional
from phidata.infra.aws.resource.iam.role import IamRole, IamPolicy
from phidata.infra.aws.resource.s3 import S3Bucket


def create_glue_iam_role(
    name: str,
    s3_buckets: Optional[List[S3Bucket]] = None,
    skip_create: bool = False,
    skip_delete: bool = False,
) -> IamRole:

    return IamRole(
        name=name,
        assume_role_policy_document=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "glue.amazonaws.com"},
                        "Action": "sts:AssumeRole",
                    }
                ],
            }
        ),
        policies=[
            IamPolicy(
                name=f"glueS3CrawlerPolicy",
                policy_document=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": ["s3:ListBucket"],
                                "Resource": [
                                    f"arn:aws:s3:::{bucket.name}"
                                    for bucket in s3_buckets
                                ],
                            },
                            {
                                "Effect": "Allow",
                                "Action": ["s3:GetObject"],
                                "Resource": [
                                    f"arn:aws:s3:::{bucket.name}/*"
                                    for bucket in s3_buckets
                                ],
                            },
                        ],
                    }
                ),
            )
        ],
        policy_arns=["arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"],
        skip_create=skip_create,
        skip_delete=skip_delete,
    )
