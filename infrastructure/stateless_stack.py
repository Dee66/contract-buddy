from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    CfnOutput,
    Duration,  # Import Duration directly
)
from constructs import Construct


class StatelessStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,  # Add env_name parameter
        data_bucket: s3.IBucket,
        vector_store_bucket: s3.IBucket,
        api_repo: ecr.IRepository,
        ingestion_repo: ecr.IRepository,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Networking ---
        vpc = ec2.Vpc(self, "Vpc", max_azs=2)

        # --- ECS Cluster ---
        cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)

        # --- IAM Roles for Services ---
        ingestion_role = iam.Role(
            self,
            "IngestionServiceRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="IAM role for the CodeCraft AI Ingestion Service",
        )
        data_bucket.grant_read(ingestion_role, "raw/*")
        vector_store_bucket.grant_read_write(ingestion_role)
        ingestion_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[f"arn:aws:bedrock:{self.region}::foundation-model/*"],
            )
        )

        api_role = iam.Role(
            self,
            "ApiServiceRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="IAM role for the CodeCraft AI API Service",
        )
        vector_store_bucket.grant_read(api_role)
        api_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[f"arn:aws:bedrock:{self.region}::foundation-model/*"],
            )
        )

        # --- Fargate Service for API ---
        api_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ApiService",
            cluster=cluster,
            cpu=256,  # .25 vCPU
            memory_limit_mib=512,  # 0.5 GB
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(api_repo),
                "environment": {
                    "APP_MODE": env_name,
                    "AWS_REGION": self.region,
                    "VECTOR_STORE_BUCKET": vector_store_bucket.bucket_name,
                },
                "task_role": api_role,
                "container_port": 8000,
                # Explicitly define logging for the API container
                "log_driver": ecs.LogDrivers.aws_logs(
                    stream_prefix=f"api-service-{env_name}"
                ),
            },
            public_load_balancer=True,
            desired_count=1,
        )

        # Configure the ALB health check to use the new /health endpoint
        api_service.target_group.configure_health_check(
            path="/health",
            interval=Duration.seconds(30),
            timeout=Duration.seconds(5),
            healthy_threshold_count=2,
            unhealthy_threshold_count=2,
            healthy_http_codes="200",
        )

        # --- Standalone Task Definition for Ingestion ---
        ingestion_task_definition = ecs.FargateTaskDefinition(
            self,
            "IngestionTaskDef",
            task_role=ingestion_role,
            cpu=1024,  # 1 vCPU
            memory_limit_mib=2048,  # 2 GB
        )
        ingestion_task_definition.add_container(
            "IngestionContainer",
            image=ecs.ContainerImage.from_ecr_repository(ingestion_repo),
            environment={
                "APP_MODE": env_name,  # Use the dynamic env_name
                "AWS_REGION": self.region,
                "VECTOR_STORE_BUCKET": vector_store_bucket.bucket_name,
                "DATA_BUCKET": data_bucket.bucket_name,
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="ingestion-task"),
        )

        # --- Stack Outputs ---
        CfnOutput(self, "EcsClusterName", value=cluster.cluster_name)
        CfnOutput(
            self,
            "IngestionTaskDefArn",
            value=ingestion_task_definition.task_definition_arn,
        )
        CfnOutput(self, "IngestionServiceRoleArn", value=ingestion_role.role_arn)
        CfnOutput(self, "ApiServiceRoleArn", value=api_role.role_arn)
        CfnOutput(
            self,
            "ApiLoadBalancerDns",
            value=api_service.load_balancer.load_balancer_dns_name,
        )
        CfnOutput(self, "ApiServiceName", value=api_service.service.service_name)
        CfnOutput(
            self,
            "PrivateSubnetIds",
            description="Comma-separated list of private subnet IDs for the ECS tasks",
            value=",".join([s.subnet_id for s in vpc.private_subnets]),
        )
