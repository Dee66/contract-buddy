@echo off
REM List all files and folders up to 3 levels deep, excluding hidden folders (names starting with a dot), for AI review.
REM Output will be saved to tree.txt in the current directory.

REM Use PowerShell to filter out hidden (dot-prefixed) folders and specifically exclude .venv
powershell -NoProfile -Command ^
    "$root = Get-Location; " ^
    "Get-ChildItem -Recurse -Depth 3 | " ^
    "Where-Object { " ^
    "  -not ($_.FullName -match '\\\\\.') " ^
    "  -and -not ($_.Name.StartsWith('.')) " ^
    "  -and -not ($_.FullName -like '*\\.venv*') " ^
    "} | " ^
    "ForEach-Object { " ^
    "  if ($_.PSIsContainer) { 'DIR:  ' + $_.FullName } else { 'FILE: ' + $_.FullName } " ^
    "}" > tree.txt

echo Output saved to tree.txt
pause
