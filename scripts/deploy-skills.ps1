param(
    [switch]$All,
    [string[]]$Skills,
    [string]$SourceRoot = ".codex/skills",
    [string]$TargetRoot = "$env:USERPROFILE\\.codex\\skills"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SourceRoot)) {
    throw "Source root not found: $SourceRoot"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$sourceRootResolved = (Resolve-Path $SourceRoot).Path

$skillDirs = Get-ChildItem -Path $sourceRootResolved -Directory
if ($All) {
    $toDeploy = $skillDirs
} elseif ($Skills -and $Skills.Count -gt 0) {
    $lookup = @{}
    foreach ($dir in $skillDirs) { $lookup[$dir.Name] = $dir }
    $toDeploy = @()
    foreach ($name in $Skills) {
        if (-not $lookup.ContainsKey($name)) {
            throw "Skill not found in source root: $name"
        }
        $toDeploy += $lookup[$name]
    }
} else {
    throw "Specify -All or -Skills <name1,name2,...>"
}

foreach ($skill in $toDeploy) {
    $dest = Join-Path $TargetRoot $skill.Name
    if (Test-Path $dest) {
        Remove-Item -LiteralPath $dest -Recurse -Force
    }
    Copy-Item -LiteralPath $skill.FullName -Destination $dest -Recurse -Force
    Write-Output "Deployed: $($skill.Name) -> $dest"
}

Write-Output "Deployment complete."