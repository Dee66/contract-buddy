# Makefile for the CodeCraft AI Project
# Provides a unified interface for common development and operational tasks.

# --- Configuration ---
.DEFAULT_GOAL := help
SHELL := pwsh.exe
.SHELLFLAGS := -NoProfile -Command

# Variables for image names
API_IMAGE := codecraft-ai-api
INGESTION_IMAGE := codecraft-ai-ingestion
# Use the short git commit hash for traceable, immutable tags.
# Fallback to 'latest' if not in a git repository.
GIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null)
TAG := $(if $(GIT_HASH),$(GIT_HASH),latest)

# Allow overriding the target environment for all commands. This is the single source of truth.
CDK_ENV ?= prod
# APP_MODE is derived from CDK_ENV for consistency.
APP_MODE := $(CDK_ENV)

# --- Dependency Management ---
install: ## Install development dependencies from the lockfile
    pip install -r requirements/dev.txt

sync-deps: ## Re-generate all lockfiles from .in files
    pip-compile requirements/prod.in -o requirements/prod.txt
    pip-compile requirements/dev.in -o requirements/dev.txt
    pip-compile requirements/staging.in -o requirements/staging.txt

# --- Code Quality & Testing ---
lint: ## Run the linter and formatter
    ruff check . --fix
    ruff format .

test: ## Run the full test suite
    pytest

# --- Local Development ---
# Detect OS for cross-platform compatibility
ifeq ($(OS),Windows_NT)
    # Windows (PowerShell) specific commands
    SET_ENV_AND_RUN_API = $env:APP_MODE="$(APP_MODE)"; uvicorn src.adapters.api.main:app --reload
    SET_ENV_AND_RUN_INGESTION = $env:APP_MODE="$(APP_MODE)"; python src/main.py
else
    # Linux/macOS (Bash) specific commands
    SET_ENV_AND_RUN_API = APP_MODE=$(APP_MODE) uvicorn src.adapters.api.main:app --reload
    SET_ENV_AND_RUN_INGESTION = APP_MODE=$(APP_MODE) python src/main.py
endif

run-api-dev: ## Run the API server locally in development mode. Usage: make run-api-dev CDK_ENV=dev
    $(SET_ENV_AND_RUN_API)

run-ingestion-dev: ## Run the ingestion pipeline locally in development mode. Usage: make run-ingestion-dev CDK_ENV=dev
    $(SET_ENV_AND_RUN_INGESTION)

# --- Docker Builds ---
build-all: build-api build-ingestion ## Build all Docker images

build-api: ## Build the API server Docker image with a traceable tag
    docker build -f Dockerfile.api -t $(API_IMAGE):$(TAG) .

build-ingestion: ## Build the ingestion pipeline Docker image with a traceable tag
    docker build -f Dockerfile.ingestion -t $(INGESTION_IMAGE):$(TAG) .

# --- Docker Operations ---
build-and-push-api: build-api ## Build and push the API image to the specified ECR registry
    @if not defined ECR_REGISTRY (echo "ECR_REGISTRY is not set. Usage: make build-and-push-api ECR_REGISTRY=<your-registry-url>"; exit 1)
    docker tag $(API_IMAGE):$(TAG) $(ECR_REGISTRY)/$(API_IMAGE):$(TAG)
    docker push $(ECR_REGISTRY)/$(API_IMAGE):$(TAG)

build-and-push-ingestion: build-ingestion ## Build and push the ingestion image to the specified ECR registry
    @if not defined ECR_REGISTRY (echo "ECR_REGISTRY is not set. Usage: make build-and-push-ingestion ECR_REGISTRY=<your-registry-url>"; exit 1)
    docker tag $(INGESTION_IMAGE):$(TAG) $(ECR_REGISTRY)/$(INGESTION_IMAGE):$(TAG)
    docker push $(ECR_REGISTRY)/$(INGESTION_IMAGE):$(TAG)

run-ingestion-docker: ## Run ingestion via Docker. Usage: make run-ingestion-docker CDK_ENV=staging
    @echo "Running ingestion container for environment: $(CDK_ENV)"
    @echo "NOTE: This requires a configured AWS profile and mounts local data."
    $(eval STACK_NAME := CodeCraftAiStatefulStack$(shell echo $(CDK_ENV) | awk '{print toupper(substr($$0,1,1))substr($$0,2)}'))
    $(eval DATA_BUCKET := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].DataBucketName' cdk-outputs.json))
    $(eval VECTOR_STORE_BUCKET := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].VectorStoreBucketName' cdk-outputs.json))
    $(if $(DATA_BUCKET),,$(error DATA_BUCKET not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    $(if $(VECTOR_STORE_BUCKET),,$(error VECTOR_STORE_BUCKET not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    docker run --rm -it `
        -e APP_MODE=$(APP_MODE) `
        -e AWS_PROFILE=$${env:AWS_PROFILE} `
        -e DATA_BUCKET=$(DATA_BUCKET) `
        -e VECTOR_STORE_BUCKET=$(VECTOR_STORE_BUCKET) `
        -v "$${env:USERPROFILE}\.aws:/home/appuser/.aws:ro" `
        -v "${pwd}\data\raw:/app/data/raw:ro" `
        -v "${pwd}\artifacts\local_vector_store:/app/vector_store" `
        $(INGESTION_IMAGE):$(TAG)

run-api-docker: ## Run API server via Docker. Usage: make run-api-docker CDK_ENV=staging
    @echo "Running API container for environment: $(CDK_ENV)"
    $(eval STACK_NAME := CodeCraftAiStatefulStack$(shell echo $(CDK_ENV) | awk '{print toupper(substr($$0,1,1))substr($$0,2)}'))
    $(eval VECTOR_STORE_BUCKET := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].VectorStoreBucketName' cdk-outputs.json))
    $(if $(VECTOR_STORE_BUCKET),,$(error VECTOR_STORE_BUCKET not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    docker run --rm -it `
        -e APP_MODE=$(APP_MODE) `
        -e AWS_PROFILE=$${env:AWS_PROFILE} `
        -e VECTOR_STORE_BUCKET=$(VECTOR_STORE_BUCKET) `
        -p 8000:8000 `
        -v "$${env:USERPROFILE}\.aws:/home/appuser/.aws:ro" `
        -v "${pwd}\artifacts\local_vector_store:/app/vector_store:ro" `
        $(API_IMAGE):$(TAG)

# --- Infrastructure (AWS CDK) ---
infra-install: ## Install Python dependencies for CDK
    pip install -r infrastructure/requirements.txt

cdk-synth: infra-install ## Synthesize the CDK CloudFormation template. Usage: make cdk-synth CDK_ENV=staging
    cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) synth

cdk-deploy: infra-install ## Deploy infrastructure changes using CDK. Usage: make cdk-deploy CDK_ENV=staging
    cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) deploy --all --require-approval never --outputs-file cdk-outputs.json

cdk-destroy: infra-install ## Destroy the CDK stack. Usage: make cdk-destroy CDK_ENV=staging
    cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) destroy --all --force

# --- Cloud Operations ---
run-ingestion-task: ## Run the ingestion task on ECS. Usage: make run-ingestion-task CDK_ENV=staging
    @echo "Running ingestion task for environment: $(CDK_ENV)..."
    $(eval STACK_NAME := CodeCraftAiStatelessStack$(shell echo $(CDK_ENV) | awk '{print toupper(substr($$0,1,1))substr($$0,2)}'))
    $(eval CLUSTER_NAME := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].EcsClusterName' cdk-outputs.json))
    $(eval TASK_DEF_ARN := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].IngestionTaskDefArn' cdk-outputs.json))
    $(eval SUBNETS := $(shell jq -r --arg stack_name "$(STACK_NAME)" '.[$stack_name].PrivateSubnetIds' cdk-outputs.json))
    $(if $(CLUSTER_NAME),,$(error CLUSTER_NAME not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    $(if $(TASK_DEF_ARN),,$(error TASK_DEF_ARN not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    $(if $(SUBNETS),,$(error PrivateSubnetIds not found in cdk-outputs.json. Run 'make cdk-deploy' first.))
    @echo "Found Cluster: $(CLUSTER_NAME)"
    @echo "Found Task Definition: $(TASK_DEF_ARN)"
    aws ecs run-task --cluster $(CLUSTER_NAME) --task-definition $(TASK_DEF_ARN) --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[$(SUBNETS)],assignPublicIp=DISABLED}"

# --- Cleanup ---
clean: ## Remove generated artifacts and cache files
    Remove-Item -Recurse -Force .pytest_cache, .ruff_cache, __pycache__, *.egg-info, cdk.out -ErrorAction SilentlyContinue

# --- Help ---
help: ## Display this help screen
    @echo "Usage: make [target]"
    @echo ""
    @echo "Targets:"
    @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
