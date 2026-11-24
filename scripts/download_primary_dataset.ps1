$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$TargetDir = Join-Path $RootDir 'data/external/PV-Generation-Dataset'
$RepoUrl = 'https://github.com/upb-nlp/PV-Generation-Dataset.git'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required. Install Git and rerun this script.'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $TargetDir) | Out-Null
if (Test-Path (Join-Path $TargetDir '.git')) {
    Write-Host "Dataset repository already exists: $TargetDir"
    Write-Host "Update it with: git -C `"$TargetDir`" pull --ff-only"
    exit 0
}

git clone --depth 1 --filter=blob:none --sparse $RepoUrl $TargetDir
git -C $TargetDir sparse-checkout set site_a site_b
Write-Host "Dataset downloaded to: $TargetDir"
Write-Host "Next: python scripts/validate_primary_dataset.py --dataset-dir `"$TargetDir`""
