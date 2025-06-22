# scripts/fix_makefile.ps1
# This PowerShell script rewrites the Makefile to ensure all recipe lines use tabs (not spaces).
# It is idempotent and safe to run multiple times.

$makefile = "Makefile"
$tempfile = "Makefile.tmp"

# Read all lines from the Makefile
$lines = Get-Content $makefile

# Patterns for targets that require tabbed commands
$targets = @(
    "validate-config:",
    "generate-config-schema:"
)

# Rewrite the file, replacing leading spaces with a tab for recipe lines
$inRecipe = $false
$lines | ForEach-Object {
    $line = $_
    if ($targets | Where-Object { $line.TrimStart().StartsWith($_) }) {
        $inRecipe = $true
        $line
    }
    elseif ($inRecipe -and ($line -match "^\s+")) {
        "`t$($line.TrimStart())"
    }
    else {
        $inRecipe = $false
        $line
    }
} | Set-Content $tempfile -Encoding UTF8

# Replace the original Makefile
Move-Item -Force $tempfile $makefile

Write-Host "Makefile formatting fixed: all recipe lines now use tabs."
