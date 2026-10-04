#!/usr/bin/env bash
# ============================================================
#  EduGenie - Setup & Launch Script (Linux / macOS / WSL)
#  Usage: bash start.sh
# ============================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Colors ──────────────────────────────────────────────────
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; MAGENTA='\033[0;35m'; RESET='\033[0m'

step()  { echo -e "${YELLOW}  ▶ $1${RESET}"; }
ok()    { echo -e "${GREEN}  ✔ $1${RESET}"; }
err()   { echo -e "${RED}  ✘ $1${RESET}"; exit 1; }

# ── Banner ──────────────────────────────────────────────────
echo ""
echo -e "${CYAN}  ╔═══════════════════════════════════════════╗"
echo -e "  ║   🧞  EduGenie - AI Learning Assistant   ║"
echo -e "  ╚═══════════════════════════════════════════╝${RESET}"
echo ""

# ── 1. Check Python ─────────────────────────────────────────
step "Checking Python 3.10+ installation..."
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        MINOR=$("$cmd" -c "import sys; print(sys.version_info.minor)")
        MAJOR=$("$cmd" -c "import sys; print(sys.version_info.major)")
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON="$cmd"
            ok "Found $("$cmd" --version) (using '$cmd')"
            break
        fi
    fi
done
[ -z "$PYTHON" ] && err "Python 3.10+ not found. Install from https://python.org"

# ── 2. Virtual environment ──────────────────────────────────
VENV="$SCRIPT_DIR/venv"
if [ ! -d "$VENV" ]; then
    step "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV"
    ok "Virtual environment created at ./venv"
else
    ok "Virtual environment already exists"
fi

# ── 3. Activate ─────────────────────────────────────────────
step "Activating virtual environment..."
source "$VENV/bin/activate"
ok "Virtual environment activated"

# ── 4. Install dependencies ─────────────────────────────────
step "Installing dependencies from requirements.txt..."
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/requirements.txt" -q
ok "All dependencies installed"

# ── 5. API key check ────────────────────────────────────────
step "Checking API key configuration..."
ENV_FILE="$SCRIPT_DIR/.env"
if [ -f "$ENV_FILE" ] && grep -q "GEMINI_API_KEY=." "$ENV_FILE"; then
    ok ".env file found with API key"
else
    echo ""
    echo -e "${MAGENTA}  ⚠  No API key found!${RESET}"
    read -rp "  Enter your Gemini API key (or press Enter to skip): " API_KEY
    if [ -n "$API_KEY" ]; then
        echo "GEMINI_API_KEY=$API_KEY" >> "$ENV_FILE"
        ok "API key saved to .env"
    else
        echo -e "  ℹ  You can set the key later via the web interface."
    fi
fi

# ── 6. Launch server ────────────────────────────────────────
echo ""
echo -e "${GREEN}  ╔═══════════════════════════════════════════╗"
echo -e "  ║  🚀  Starting EduGenie on               ║"
echo -e "  ║      http://127.0.0.1:8000               ║"
echo -e "  ║  Press Ctrl+C to stop the server         ║"
echo -e "  ╚═══════════════════════════════════════════╝${RESET}"
echo ""

# Open browser in background (best-effort)
(sleep 2 && (xdg-open "http://127.0.0.1:8000" 2>/dev/null || open "http://127.0.0.1:8000" 2>/dev/null)) &

cd "$SCRIPT_DIR"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
