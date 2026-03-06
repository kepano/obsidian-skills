#Requires -Version 5.1
<#
.SYNOPSIS
    Install obsidian-skills for Codex native skill discovery.

.DESCRIPTION
    Syncs each skill from skills/ into the Codex skills directory
    (default: ~/.agents/skills/obsidian-skills).

.PARAMETER SkillsDir
    Target skills directory (default: ~/.agents/skills/obsidian-skills)

.PARAMETER DryRun
    Print actions without writing anything

.EXAMPLE
    .\scripts\install-skills-codex.ps1

.EXAMPLE
    .\scripts\install-skills-codex.ps1 -SkillsDir C:\custom\path\skills\obsidian-skills

.EXAMPLE
    .\scripts\install-skills-codex.ps1 -DryRun
#>

param(
    [string]$SkillsDir = (Join-Path $HOME '.agents' 'skills' 'obsidian-skills'),
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir

function Write-Log {
    param([string]$Message)
    Write-Host "[install-skills] $Message"
}

function Invoke-Die {
    param([string]$Message)
    Write-Error "[install-skills] Error: $Message"
    exit 1
}

# Validate repo structure
$SkillsSrc = Join-Path $RepoRoot "skills"
if (-not (Test-Path -Path $SkillsSrc -PathType Container)) {
    Invoke-Die "skills/ directory not found under repo root: $RepoRoot"
}

# Collect skill names
$SkillNames = Get-ChildItem -Path $SkillsSrc -Directory |
    Sort-Object Name |
    Select-Object -ExpandProperty Name

if ($SkillNames.Count -eq 0) {
    Invoke-Die "No skills found in $SkillsSrc"
}

function Sync-Skill {
    param([string]$SkillName)

    $src = Join-Path $SkillsSrc $SkillName
    $dst = Join-Path $SkillsDir $SkillName

    if ($DryRun) {
        Write-Log "DRY-RUN: sync $src -> $dst"
        return
    }

    # Ensure destination parent exists
    if (-not (Test-Path -Path $dst)) {
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
    }

    # Copy all items from src to dst, overwriting existing files
    Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force

    # Remove items in dst that are no longer in src
    Get-ChildItem -Path $dst | Where-Object {
        -not (Test-Path (Join-Path $src $_.Name))
    } | Remove-Item -Recurse -Force
}

if ($DryRun) {
    Write-Log "DRY-RUN mode — no files will be written"
}

Write-Log "Installing obsidian-skills to: $SkillsDir"

foreach ($skill in $SkillNames) {
    Write-Log "Syncing skill: $skill"
    Sync-Skill -SkillName $skill
}

if (-not $DryRun) {
    Write-Log "Done. Skills installed to: $SkillsDir"
    Write-Log "Restart Codex to discover the new skills."
}
