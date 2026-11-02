<#
 One-command start for Windows PowerShell.
   .\run.ps1            # real local Meta Llama via Ollama (loads the model first so the first request is fast)
   .\run.ps1 -Mock      # predefined sample assessments, no model needed (UI development only)
   .\run.ps1 -NoWarm    # skip the model warm-up
 If scripts are blocked:  Set-ExecutionPolicy -Scope Process Bypass
 NOTE: written for Windows but not yet run by the author of this repo on Windows. Report any problem.
#>
param([switch]$Mock, [switch]$NoWarm)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$be = Join-Path $root "backend"
$fe = Join-Path $root "frontend"

function Need($cmd, $hint) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "'$cmd' was not found. $hint" }
}
Need python "Install Python 3.12 from python.org and tick 'Add python.exe to PATH', then open a NEW terminal."
Need node   "Install Node.js 22 LTS (or 20.19+), then open a NEW terminal."
if (-not $Mock) { Need ollama "Install Ollama from https://ollama.com/download/windows, then run: ollama pull llama3.2:3b" }

if (-not (Test-Path (Join-Path $be ".venv"))) { Write-Host "Creating Python virtual environment..."; python -m venv (Join-Path $be ".venv") }
$py = Join-Path $be ".venv\Scripts\python.exe"
Write-Host "Installing backend requirements..."
& $py -m pip install -q -r (Join-Path $be "requirements.txt")
if (-not (Test-Path (Join-Path $be ".env"))) { Copy-Item (Join-Path $be ".env.example") (Join-Path $be ".env") }
if (-not (Test-Path (Join-Path $fe ".env"))) { Copy-Item (Join-Path $fe ".env.example") (Join-Path $fe ".env") }
if (-not (Test-Path (Join-Path $fe "node_modules"))) { Write-Host "Installing frontend packages..."; Push-Location $fe; npm install; Pop-Location }

$prov = if ($Mock) { "mock" } else { "ollama" }
$beCmd = "`$env:AI_PROVIDER='$prov'; Set-Location -LiteralPath '$be'; & '$py' -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
$feCmd = "Set-Location -LiteralPath '$fe'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $beCmd
Start-Process powershell -ArgumentList "-NoExit", "-Command", $feCmd

# wait for the backend, then (optionally) load the model into memory
$up = $false
for ($i = 0; $i -lt 30 -and -not $up; $i++) {
  Start-Sleep -Seconds 1
  try { Invoke-RestMethod "http://127.0.0.1:8000/health" | Out-Null; $up = $true } catch { }
}
if (-not $up) { Write-Warning "Backend did not answer on 127.0.0.1:8000 - check the backend window for errors."; exit 1 }
if (-not $Mock -and -not $NoWarm) {
  Write-Host "Loading the model (can take a minute on CPU)..."
  try { (Invoke-RestMethod -Method Post "http://127.0.0.1:8000/api/warmup" -TimeoutSec 300) | ConvertTo-Json }
  catch { Write-Warning "Warm-up failed: $($_.Exception.Message). Check: ollama list  and  http://127.0.0.1:8000/api/model-status" }
}
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5173"
Write-Host "Rasta is running. Close the two PowerShell windows to stop it."
