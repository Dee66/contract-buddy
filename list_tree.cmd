@echo off
REM List all files and folders up to 3 levels deep, excluding hidden folders (names starting with a dot),
REM and '.venv' folders. 'node_modules' folders will now be included as requested.
REM Output will be saved to tree.txt in the current directory.

REM Use PowerShell to filter out hidden (dot-prefixed) folders and .venv folders
powershell -NoProfile -Command ^
    "$ErrorActionPreference = 'SilentlyContinue'; " ^
    "$root = Get-Location; " ^
    "Get-ChildItem -Recurse -Depth 3 | " ^
    "Where-Object { " ^
    "   -not ( " ^
    "       ($_.PSIsContainer -and $_.Name.StartsWith('.')) -or " ^
    "       (-not $_.PSIsContainer -and $_.DirectoryName -match '(?i)[\\/]\.') -or " ^
    "       ($_.FullName -match '(?i)[\\/]\.venv([\\/]|$)') " ^
    "   )" ^
    "} | " ^
    "ForEach-Object { " ^
    "   if ($_.PSIsContainer) { 'DIR:   ' + $_.FullName } else { 'FILE: ' + $_.FullName } " ^
    "}" > tree.txt

echo Output saved to tree.txt
pause