from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ecr as ecr,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct


class StatefulStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for storing raw data for ingestion
        self.data_bucket = s3.Bucket(
            self,
            "DataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # S3 bucket for persisting the FAISS vector store
        self.vector_store_bucket = s3.Bucket(
            self,
            "VectorStoreBucket",
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # ECR repository for the API container image
        self.api_repo = ecr.Repository(
            self,
            "ApiEcrRepo",
            repository_name="codecraft-ai-api",
            removal_policy=RemovalPolicy.RETAIN,  # Keep repo even if stack is destroyed
        )

        # ECR repository for the ingestion container image
        self.ingestion_repo = ecr.Repository(
            self,
            "IngestionEcrRepo",
            repository_name="codecraft-ai-ingestion",
            removal_policy=RemovalPolicy.RETAIN,  # Keep repo even if stack is destroyed
        )

        # --- Stack Outputs ---
        CfnOutput(self, "DataBucketName", value=self.data_bucket.bucket_name)
        CfnOutput(
            self, "VectorStoreBucketName", value=self.vector_store_bucket.bucket_name
        )
        CfnOutput(self, "ApiEcrRepoUri", value=self.api_repo.repository_uri)
        CfnOutput(self, "IngestionEcrRepoUri", value=self.ingestion_repo.repository_uri)
