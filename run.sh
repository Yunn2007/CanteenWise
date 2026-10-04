#!/bin/bash
# CanteenWise One-Click Application Launcher
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. Identify Python interpreter with Tkinter support
if [ -x "/opt/anaconda3/bin/python" ]; then
    PY_BIN="/opt/anaconda3/bin/python"
elif python -c "import tkinter" 2>/dev/null; then
    PY_BIN="python"
elif python3 -c "import tkinter" 2>/dev/null; then
    PY_BIN="python3"
else
    echo "❌ Error: Could not find Python interpreter with Tkinter support."
    exit 1
fi

echo "======================================================"
echo "  🍽️  Launching CanteenWise using: $PY_BIN"
echo "======================================================"
exec "$PY_BIN" main.py "$@"
