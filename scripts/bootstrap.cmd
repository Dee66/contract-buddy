@echo off
echo Discovering AWS environment...

:: Get AWS Account ID
aws sts get-caller-identity --query Account --output text > account.tmp
if %errorlevel% neq 0 (
    echo Error: 'aws sts get-caller-identity' failed. Check AWS CLI and credentials.
    del account.tmp
    exit /b 1
)
set /p AWS_ACCOUNT=<account.tmp
del account.tmp

:: Get AWS Region
aws configure get region > region.tmp
if %errorlevel% neq 0 (
    echo Error: 'aws configure get region' failed. Check AWS CLI and configuration.
    del region.tmp
    exit /b 1
)
set /p AWS_REGION=<region.tmp
del region.tmp

:: Check if variables are set
if not defined AWS_ACCOUNT (
    echo Could not determine AWS Account.
    exit /b 1
)
if not defined AWS_REGION (
    echo Could not determine AWS Region.
    exit /b 1
)

:: Run bootstrap
echo Bootstrapping aws://%AWS_ACCOUNT%/%AWS_REGION%...
cdk -a "python infrastructure/app.py" bootstrap aws://%AWS_ACCOUNT%/%AWS_REGION%
