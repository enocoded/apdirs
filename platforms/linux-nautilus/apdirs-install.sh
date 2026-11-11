#!/usr/bin/env bash
set -e

# The installer lives in platforms/linux-nautilus; resolve the repository root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "========================================="
echo "   Installing Apdirs Nautilus Extension  "
echo "========================================="

# 1. Install system dependencies for Nautilus Python & GUI dialogs
echo "-> Installing system packages (python3-nautilus, python3-tk)..."
sudo apt update
sudo apt install -y python3-nautilus python3-tk python3-pip

# 2. Install the core package locally in editable user mode
echo "-> Installing python package locally..."
cd "$REPO_ROOT"
pip install --user --break-system-packages -e .

# 3. Setup Nautilus extension directory
NAUTILUS_EXT_DIR="$HOME/.local/share/nautilus-python/extensions"
mkdir -p "$NAUTILUS_EXT_DIR"

# 4. Symlink the extension file into Nautilus
EXT_SOURCE="$REPO_ROOT/platforms/linux-nautilus/apdirs_nautilus.py"
EXT_TARGET="$NAUTILUS_EXT_DIR/apdirs_nautilus.py"

if [ -f "$EXT_TARGET" ] || [ -L "$EXT_TARGET" ]; then
    rm "$EXT_TARGET"
fi

ln -s "$EXT_SOURCE" "$EXT_TARGET"
echo "-> Symlinked Nautilus extension to $EXT_TARGET"

# 5. Restart Nautilus to apply changes instantly
echo "-> Restarting Nautilus file manager..."
nautilus -q

echo ""
echo "Installation complete! Right-click inside your 'client-work' folder in Nautilus to test."