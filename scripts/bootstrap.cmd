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

:: --- Python Environment Bootstrap ---
REM Prefer project .venv if present, else fallback to system Python
set PYTHON_EXE=
if exist "%~dp0\..\..\venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0\..\..\venv\Scripts\python.exe
) else if exist "%~dp0\..\..\.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0\..\..\.venv\Scripts\python.exe
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON_EXE=python
    ) else (
        echo [ERROR] Python executable not found. Please create a virtual environment or install Python.
        exit /b 1
    )
)

:: Print Python version for traceability
%PYTHON_EXE% --version

:: Run CDK bootstrap
echo Bootstrapping aws://%AWS_ACCOUNT%/%AWS_REGION%...
cdk -a "%PYTHON_EXE% infrastructure/app.py" bootstrap aws://%AWS_ACCOUNT%/%AWS_REGION%
