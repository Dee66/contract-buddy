REM c:\workspace\AI\codecraft-ai\pre-push.cmd (update existing)
REM Pre-push local pipeline for CodeCraft AI (Windows/cmd.exe)
REM Runs all Nox automation before allowing a git push.

@echo off
setlocal

REM Run all Nox sessions (lint, test, build, etc.)
nox -s all
if errorlevel 1 (
    echo.
    echo [ERROR] One or more pre-push checks failed. Please review the output above.
    exit /b 1
)

echo All pre-push checks passed. You are ready to commit and push!
exit /b 0
