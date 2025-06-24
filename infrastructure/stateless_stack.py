from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_secretsmanager as secretsmanager,
    aws_ssm as ssm,
    aws_logs as logs,
    aws_cloudwatch as cloudwatch,
    CfnOutput,
    Duration,
    RemovalPolicy,
)
from constructs import Construct
import json


class StatelessStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str = "dev",
        data_bucket: s3.IBucket = None,
        vector_store_bucket: s3.IBucket = None,
        api_repo: ecr.IRepository = None,
        ingestion_repo: ecr.IRepository = None,
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

        # --- Secrets Management: Use or create per-environment vault ---
        secret_name = f"codecraft-ai/secrets/{env_name}"
        try:
            # Try to look up an existing secret (recommended for dev/staging/prod)
            env_secret = secretsmanager.Secret.from_secret_name_v2(
                self, "EnvSecret", secret_name
            )
        except Exception:
            # If not found, create a new one (for ephemeral/test environments)
            env_secret = secretsmanager.Secret(
                self,
                "EnvSecret",
                secret_name=secret_name,
                description=f"Centralized secret vault for CodeCraft AI ({env_name})",
                generate_secret_string=secretsmanager.SecretStringGenerator(
                    secret_string_template=json.dumps(
                        {
                            "API_KEY": "replace_me",
                            # ...add other required keys with dummy values...
                        }
                    ),
                    generate_string_key="PLACEHOLDER",
                    password_length=32,
                    exclude_punctuation=True,
                ),
            )

        # --- Fargate Service for API ---
        api_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ApiService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(api_repo),
                "environment": {
                    "APP_MODE": env_name,
                    "AWS_REGION": self.region,
                    "VECTOR_STORE_BUCKET": vector_store_bucket.bucket_name,
                },
                # Inject the full secret JSON and API_KEY as env vars
                "secrets": {
                    "APP_SECRETS_JSON": ecs.Secret.from_secrets_manager(env_secret),
                    "API_KEY": ecs.Secret.from_secrets_manager(
                        env_secret, field="API_KEY"
                    ),
                },
                "task_role": api_role,
                "container_port": 8000,
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
            cpu=1024,
            memory_limit_mib=2048,
        )
        ingestion_task_definition.add_container(
            "IngestionContainer",
            image=ecs.ContainerImage.from_ecr_repository(ingestion_repo),
            environment={
                "APP_MODE": env_name,
                "AWS_REGION": self.region,
                "VECTOR_STORE_BUCKET": vector_store_bucket.bucket_name,
                "DATA_BUCKET": data_bucket.bucket_name,
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="ingestion-task"),
        )

        # --- Centralized AppConfig in SSM Parameter Store ---
        app_config = {
            "vector_store_bucket": vector_store_bucket.bucket_name,
            "data_bucket": data_bucket.bucket_name,
            "log_level": "INFO",
            "api_timeout_seconds": 30,
            "feature_flags": {"enable_experimental": False},
        }
        ssm_param = ssm.StringParameter(
            self,
            "AppConfigParameter",
            string_value=json.dumps(app_config),
            parameter_name=f"/codecraft-ai/{env_name}/AppConfig",
            description=f"Centralized application config for CodeCraft AI ({env_name})",
        )

        # --- Grant ECS Task Roles permission to read config ---
        for role in [api_role, ingestion_role]:
            ssm_param.grant_read(role)

        # --- CloudWatch Log Group for ECS (with cost-efficient retention) ---
        logs.LogGroup(
            self,
            "ApiEcsLogGroup",
            log_group_name=f"/ecs/codecraft-ai-api-{env_name}",
            retention=logs.RetentionDays.ONE_DAY
            if env_name == "dev"
            else logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,  # Clean up in dev/staging
        )

        # --- Minimal CloudWatch Dashboard ---
        dashboard = cloudwatch.Dashboard(
            self,
            "ApiDashboard",
            dashboard_name=f"CodeCraftAI-{env_name}-Dashboard",
        )

        # ECS CPU Utilization Widget (uses actual cluster and service names)
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="API ECS CPU Utilization",
                left=[
                    cloudwatch.Metric(
                        namespace="AWS/ECS",
                        metric_name="CPUUtilization",
                        dimensions_map={
                            "ClusterName": cluster.cluster_name,
                            "ServiceName": api_service.service.service_name,
                        },
                        statistic="Average",
                        period=Duration.minutes(5),
                    )
                ],
                width=12,
                height=6,
            )
        )

        # --- Minimal CloudWatch Alarm (API 5xx errors) ---
        # Use the actual ALB ARN for the LoadBalancer dimension
        alb_arn_suffix = api_service.load_balancer.load_balancer_arn.split(
            "loadbalancer/"
        )[-1]
        alb_5xx_metric = cloudwatch.Metric(
            namespace="AWS/ApplicationELB",
            metric_name="HTTPCode_Target_5XX_Count",
            dimensions_map={
                "LoadBalancer": alb_arn_suffix,
            },
            statistic="Sum",
            period=Duration.minutes(5),
        )

        alarm_threshold = 10 if env_name == "dev" else 3
        cloudwatch.Alarm(
            self,
            "Api5xxAlarm",
            metric=alb_5xx_metric,
            threshold=alarm_threshold,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            alarm_description=f"API 5xx errors exceed {alarm_threshold} in 5 minutes ({env_name})",
        )

        # In dev, do not send notifications; in prod, add SNS or other actions as needed
        # alb_5xx_alarm.add_alarm_action(cw_actions.SnsAction(your_sns_topic))

        # --- Output dashboard URL for convenience ---
        self.dashboard_url = f"https://console.aws.amazon.com/cloudwatch/home?region={self.region}#dashboards:name={dashboard.dashboard_name}"

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
            "ApiUrl",
            description="The public URL of the API service",
            value=f"http://{api_service.load_balancer.load_balancer_dns_name}",
        )
        CfnOutput(
            self,
            "ApiKeySecretName",
            description="The name of the secret in AWS Secrets Manager containing the API key",
            value=env_secret.secret_name,
        )
        CfnOutput(self, "ApiServiceName", value=api_service.service.service_name)
        CfnOutput(
            self,
            "PrivateSubnetIds",
            description="Comma-separated list of private subnet IDs for the ECS tasks",
            value=",".join([s.subnet_id for s in vpc.private_subnets]),
        )
