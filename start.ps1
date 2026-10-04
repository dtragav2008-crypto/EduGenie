# ============================================================
#  EduGenie - Setup & Launch Script (Windows PowerShell)
#  Usage: Right-click > "Run with PowerShell"
#         or run: powershell -ExecutionPolicy Bypass -File start.ps1
# ============================================================

$Host.UI.RawUI.WindowTitle = "EduGenie Launcher"

function Write-Banner {
    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║   🧞  EduGenie - AI Learning Assistant   ║" -ForegroundColor Cyan
    Write-Host "  ╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "  ▶ $msg" -ForegroundColor Yellow
}

function Write-OK($msg) {
    Write-Host "  ✔ $msg" -ForegroundColor Green
}

function Write-Err($msg) {
    Write-Host "  ✘ $msg" -ForegroundColor Red
}

# ── Banner ──────────────────────────────────────────────────
Write-Banner

# ── 1. Check Python ─────────────────────────────────────────
Write-Step "Checking Python installation..."
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.(\d+)") {
            $minor = [int]$Matches[1]
            if ($minor -ge 10) {
                $python = $cmd
                Write-OK "Found $ver (using '$cmd')"
                break
            }
        }
    } catch {}
}

if (-not $python) {
    Write-Err "Python 3.10+ not found. Please install it from https://python.org"
    Read-Host "Press Enter to exit"
    exit 1
}

# ── 2. Check / Create virtual environment ───────────────────
$venvPath = Join-Path $PSScriptRoot "venv"
if (-not (Test-Path $venvPath)) {
    Write-Step "Creating virtual environment..."
    & $python -m venv $venvPath
    Write-OK "Virtual environment created at .\venv"
} else {
    Write-OK "Virtual environment already exists"
}

# ── 3. Activate venv ────────────────────────────────────────
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Step "Activating virtual environment..."
    . $activateScript
    Write-OK "Virtual environment activated"
} else {
    Write-Err "Could not activate venv. Trying system Python instead."
}

# ── 4. Install / upgrade dependencies ───────────────────────
Write-Step "Installing dependencies from requirements.txt..."
$reqFile = Join-Path $PSScriptRoot "requirements.txt"
if (Test-Path $reqFile) {
    & $python -m pip install --upgrade pip --quiet
    & $python -m pip install -r $reqFile --quiet
    Write-OK "All dependencies installed"
} else {
    Write-Err "requirements.txt not found!"
    Read-Host "Press Enter to exit"
    exit 1
}

# ── 5. Check .env / API key ──────────────────────────────────
Write-Step "Checking API key configuration..."
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "GEMINI_API_KEY=.+") {
        Write-OK ".env file found with API key"
    } else {
        Write-Host ""
        Write-Host "  ⚠  No API key found in .env!" -ForegroundColor Magenta
        $apiKey = Read-Host "  Enter your Gemini API key (or press Enter to skip)"
        if ($apiKey) {
            Add-Content $envFile "GEMINI_API_KEY=$apiKey"
            Write-OK "API key saved to .env"
        } else {
            Write-Host "  ℹ  You can set the key later via the web interface." -ForegroundColor DarkCyan
        }
    }
} else {
    Write-Host ""
    Write-Host "  ⚠  .env file not found!" -ForegroundColor Magenta
    $apiKey = Read-Host "  Enter your Gemini API key (or press Enter to skip)"
    $keyLine = if ($apiKey) { "GEMINI_API_KEY=$apiKey" } else { "GEMINI_API_KEY=" }
    Set-Content $envFile $keyLine
    Write-OK ".env file created"
}

# ── 6. Launch server ────────────────────────────────────────
Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║  🚀  Starting EduGenie on               ║" -ForegroundColor Green
Write-Host "  ║      http://127.0.0.1:8000               ║" -ForegroundColor Green
Write-Host "  ║  Press Ctrl+C to stop the server         ║" -ForegroundColor Green
Write-Host "  ╚═══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Open browser after a short delay
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

# Run the server
Set-Location $PSScriptRoot
& $python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
