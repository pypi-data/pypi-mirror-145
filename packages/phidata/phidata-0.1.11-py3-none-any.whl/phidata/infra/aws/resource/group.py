from typing import List, Optional

from pydantic import BaseModel

from phidata.infra.aws.resource.acm.certificate import AcmCertificate
from phidata.infra.aws.resource.cloudformation import CloudFormationStack
from phidata.infra.aws.resource.ec2.volume import EbsVolume
from phidata.infra.aws.resource.eks.cluster import EksCluster
from phidata.infra.aws.resource.eks.fargate_profile import EksFargateProfile
from phidata.infra.aws.resource.eks.node_group import EksNodeGroup
from phidata.infra.aws.resource.iam.role import IamRole
from phidata.infra.aws.resource.iam.policy import IamPolicy
from phidata.infra.aws.resource.glue.crawler import GlueCrawlerResource
from phidata.infra.aws.resource.s3 import S3Bucket


class AwsResourceGroup(BaseModel):
    """The AwsResourceGroup class contains the data for all AwsResources"""

    name: str = "aws-resources"
    enabled: bool = True

    iam_roles: Optional[List[IamRole]] = None
    iam_policies: Optional[List[IamPolicy]] = None
    acm_certificates: Optional[List[AcmCertificate]] = None
    s3_buckets: Optional[List[S3Bucket]] = None
    volumes: Optional[List[EbsVolume]] = None
    cloudformation_stacks: Optional[List[CloudFormationStack]] = None
    eks_cluster: Optional[EksCluster] = None
    eks_fargate_profiles: Optional[List[EksFargateProfile]] = None
    eks_nodegroups: Optional[List[EksNodeGroup]] = None
    glue_crawlers: Optional[List[GlueCrawlerResource]] = None
