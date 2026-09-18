# Optional wrapper. The Python engine also works without this script.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Target = "",
    [switch]$Apply,
    [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$null = Get-Command $Python -CommandType Application -ErrorAction Stop
$arguments = @((Join-Path $PSScriptRoot "manage_skills.py"), "uninstall")
if ($Target) { $arguments += @("--target", $Target) }
$doApply = $Apply -and $PSCmdlet.ShouldProcess("Interface Forge: $Target", "uninstall")
if ($doApply) { $arguments += "--apply" }
& $Python @arguments
if ($LASTEXITCODE -ne 0) { throw "Interface Forge: operation did not complete (exit $LASTEXITCODE)." }
