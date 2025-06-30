@echo off
REM List all files and folders up to 3 levels deep, excluding hidden folders (names starting with a dot),
REM 'node_modules' folders (at any depth), and '.venv' folders.
REM Output will be saved to tree.txt in the current directory.

REM Use PowerShell to filter out hidden (dot-prefixed) folders, .venv, and node_modules
powershell -NoProfile -Command ^
    "$ErrorActionPreference = 'SilentlyContinue'; " ^
    "$root = Get-Location; " ^
    "Get-ChildItem -Recurse -Depth 3 | " ^
    "Where-Object { " ^
    "   ($_.FullName -notmatch '(?i)[\\/](node_modules|\.venv)([\\/]|$)') -and " ^
    "   (" ^
    "       ($_.PSIsContainer -and -not $_.Name.StartsWith('.')) -or " ^
    "       (-not $_.PSIsContainer -and -not ($_.DirectoryName -match '(?i)[\\/]\.')) " ^
    "   )" ^
    "} | " ^
    "ForEach-Object { " ^
    "   if ($_.PSIsContainer) { 'DIR:   ' + $_.FullName } else { 'FILE: ' + $_.FullName } " ^
    "}" > tree.txt

echo Output saved to tree.txt
pause
