from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_s3 as s3
from constructs import Construct


class AwsCdkTestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(
            self,
            "CodeScanTestBucket",
            # block_public_access=s3.BlockPublicAccess(
            #     block_public_acls=True,
            #     block_public_policy=True,
            #     ignore_public_acls=True,
            #     restrict_public_buckets=True,
            # ),
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            versioned=True,
        )

        vpc = ec2.Vpc(
            self,
            "CodeScanTestVpc",
            vpc_name="CodeScanTestVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="PRIVATE", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                ),
            ],
        )
        sg = ec2.SecurityGroup(
            self,
            "CodeScanTestSg",
            security_group_name="CodeScanTestSg",
            allow_all_outbound=True,
            vpc=vpc,
        )
        # sg.add_ingress_rule(ec2.Peer.ipv4("60.65.7.119/32"), ec2.Port.tcp(22))
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))
