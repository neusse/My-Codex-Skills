param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [string]$Description,

    [string]$TemplatePath = ".\templates\skill-template\SKILL.md",
    [string]$SkillsRoot = ".\.codex\skills",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Convert-ToKebabCase {
    param([string]$InputText)
    $value = $InputText.ToLowerInvariant()
    $value = $value -replace "[^a-z0-9]+", "-"
    $value = $value.Trim("-")
    return $value
}

$skillName = Convert-ToKebabCase -InputText $Name
if ([string]::IsNullOrWhiteSpace($skillName)) {
    throw "Skill name resolved to empty after normalization. Provide a name with letters or numbers."
}

if (-not (Test-Path $TemplatePath)) {
    throw "Template not found: $TemplatePath"
}

New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null

$skillDir = Join-Path $SkillsRoot $skillName
$skillFile = Join-Path $skillDir "SKILL.md"

if ((Test-Path $skillDir) -and (-not $Force)) {
    throw "Skill already exists: $skillDir (use -Force to overwrite)"
}

if (Test-Path $skillDir) {
    Remove-Item -LiteralPath $skillDir -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $skillDir | Out-Null

$template = Get-Content -LiteralPath $TemplatePath -Raw
$content = $template -replace "name:\s*your-skill-name", "name: $skillName"
$content = $content -replace "description:\s*One-sentence description of what this skill helps with\.", "description: $Description"

Set-Content -LiteralPath $skillFile -Value $content -NoNewline

Write-Output "Created skill: $skillName"
Write-Output "Path: $skillFile"
