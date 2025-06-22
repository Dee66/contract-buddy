# Makefile for CodeCraft AI (cmd.exe compatible)
#
# IMPORTANT: This Makefile is written for cmd.exe.
# The 'make' executable on the target Windows environment (GNU Make via Chocolatey)
# defaults to using cmd.exe as its shell, even when 'make' is invoked from
# PowerShell. Do not use PowerShell-specific syntax (e.g., $env:VAR, ;).
# Use cmd.exe syntax (e.g., set VAR=... , &&).
.DEFAULT_GOAL := help

# Variables for image names
API_IMAGE := codecraft-ai-api
INGESTION_IMAGE := codecraft-ai-ingestion
GIT_HASH := $(shell git rev-parse --short HEAD)
TAG = $(if $(GIT_HASH),$(GIT_HASH),latest)

# Allow overriding the target environment for all commands.
CDK_ENV ?= prod
APP_MODE = $(CDK_ENV)

# --- Dependency Management ---
install: ## Install development dependencies from the lockfile
	pip install -r requirements/dev.txt

sync-deps: ## Re-generate all lockfiles from .in files
	pip-compile requirements/prod.in -o requirements/prod.txt
	pip-compile requirements/dev.in -o requirements/dev.txt
	pip-compile requirements/staging.in -o requirements/staging.txt

# --- Code Quality & Testing ---
lint: ## Run the linter and formatter
	ruff check . --fix && ruff format .

test: ## Run the full test suite
	pytest

# --- Local Development ---
run-api-dev: ## Run the API server locally in development mode. Usage: make run-api-dev CDK_ENV=dev
	set APP_MODE=$(APP_MODE) && uvicorn src.adapters.api.main:app --reload

run-ingestion-dev: ## Run the ingestion pipeline locally in development mode. Usage: make run-ingestion-dev CDK_ENV=dev
	set APP_MODE=$(APP_MODE) && python src/main.py

# --- Docker Builds ---
build-all: build-api build-ingestion ## Build all Docker images

build-api: ## Build the API server Docker image with a traceable tag
	docker build -f Dockerfile.api -t $(API_IMAGE):$(TAG) .

build-ingestion: ## Build the ingestion pipeline Docker image with a traceable tag
	docker build -f Dockerfile.ingestion -t $(INGESTION_IMAGE):$(TAG) .

# --- Infrastructure (AWS CDK) ---
infra-install: ## Install Python dependencies for CDK
	pip install -r infrastructure/requirements.txt

cdk-bootstrap: infra-install ## Bootstrap CDK automatically in the configured AWS account/region
	@cmd.exe /c scripts\\bootstrap.cmd

cdk-synth: infra-install ## Synthesize the CDK CloudFormation template. Usage: make cdk-synth CDK_ENV=staging
	cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) synth

cdk-deploy: infra-install ## Deploy infrastructure changes using CDK. Usage: make cdk-deploy CDK_ENV=staging
	cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) deploy --all --require-approval never --outputs-file cdk-outputs.json

cdk-destroy: infra-install ## Destroy the CDK stack. Usage: make cdk-destroy CDK_ENV=staging
	cdk -a "python infrastructure/app.py" -c env=$(CDK_ENV) destroy --all --force

# --- Diagnostics ---
debug-aws: ## Run AWS CLI diagnostics to check credential configuration
	@echo --- AWS CLI Debug Information ---
	@echo.
	@echo [1] Checking user profile/home directory location...
	@echo USERPROFILE is: %USERPROFILE%
	@echo.
	@echo [2] Checking for AWS config files...
	@if exist "%USERPROFILE%\\.aws\\config" (echo Found: %USERPROFILE%\\.aws\\config) else (echo Not Found: %USERPROFILE%\\.aws\\config)
	@if exist "%USERPROFILE%\\.aws\\credentials" (echo Found: %USERPROFILE%\\.aws\\credentials) else (echo Not Found: %USERPROFILE%\\.aws\\credentials)
	@echo.
	@echo [3] Attempting to get AWS region...
	@aws configure get region
	@echo.
	@echo [4] Attempting to get AWS caller identity (this may error)...
	@aws sts get-caller-identity
	@echo.
	@echo --- End Debug ---

# --- Help ---
help: ## Display this help screen
	@echo Usage: make [target]
	@echo.
	@echo Targets:
	@awk "BEGIN {FS = \":.*?## \"} /^[a-zA-Z_-]+:.*?## / {printf \"  %-20s %s\\n\", $$1, $$2}" $(MAKEFILE_LIST)

validate-config: ## Validate SSM config for the target environment before deployment
	set APP_MODE=$(APP_MODE) && python scripts/validate_config.py --env $(APP_MODE)

generate-config-schema: ## Generate Markdown config schema doc from Pydantic model
	python scripts/generate_config_schema_md.py

security-audit: ## Run pip-audit on all requirements for vulnerability scanning
    pip-audit -r requirements/dev.txt -r requirements/prod.txt
