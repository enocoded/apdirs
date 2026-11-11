#!/usr/bin/env bash
set -e

# The installer lives in platforms/linux-nautilus; resolve the repository root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
APDIRS_BIN_DIR="${APDIRS_BIN_DIR:-"$HOME/.local/bin"}"

echo "========================================="
echo "   Installing Apdirs Linux Extension     "
echo "========================================="

# 1. Install system dependencies for Nautilus Python & GUI dialogs
echo "-> Installing system packages (GTK 4, Nautilus bindings, Tkinter fallback)..."
sudo apt update
sudo apt install -y python3-gi gir1.2-gtk-4.0 python3-nautilus python3-tk python3-pip

# 2. Install the core package locally in editable user mode from repo root
echo "-> Installing python package locally..."
cd "$REPO_ROOT"
pip install --user --break-system-packages -e .

# 3. Setup Nautilus extension directory
NAUTILUS_EXT_DIR="$HOME/.local/share/nautilus-python/extensions"
mkdir -p "$NAUTILUS_EXT_DIR"

# 4. Symlink the extension file from its platform folder into Nautilus
EXT_SOURCE="$SCRIPT_DIR/apdirs_nautilus.py"
EXT_TARGET="$NAUTILUS_EXT_DIR/apdirs_nautilus.py"

if [ -f "$EXT_TARGET" ] || [ -L "$EXT_TARGET" ]; then
    rm "$EXT_TARGET"
fi

ln -s "$EXT_SOURCE" "$EXT_TARGET"
echo "-> Symlinked Nautilus extension to $EXT_TARGET"

# 5. Install the CLI command alongside the Nautilus extension
CLI_SOURCE="$SCRIPT_DIR/apdirs_cli.sh"
CLI_TARGET="$APDIRS_BIN_DIR/apdirs"
mkdir -p "$APDIRS_BIN_DIR"

if [ -L "$CLI_TARGET" ] && [ "$(readlink -f "$CLI_TARGET")" = "$(readlink -f "$CLI_SOURCE")" ]; then
    echo "-> CLI command is already linked at $CLI_TARGET"
elif [ -e "$CLI_TARGET" ] || [ -L "$CLI_TARGET" ]; then
    CLI_BACKUP="$CLI_TARGET.backup"
    if [ -e "$CLI_BACKUP" ] || [ -L "$CLI_BACKUP" ]; then
        echo "Error: Cannot install CLI; both $CLI_TARGET and $CLI_BACKUP exist."
        exit 1
    fi
    mv "$CLI_TARGET" "$CLI_BACKUP"
    ln -s "$CLI_SOURCE" "$CLI_TARGET"
    echo "-> Backed up existing CLI to $CLI_BACKUP"
    echo "-> Installed CLI command at $CLI_TARGET"
else
    ln -s "$CLI_SOURCE" "$CLI_TARGET"
    echo "-> Installed CLI command at $CLI_TARGET"
fi

DESKTOP_DATA_DIR="$HOME/.local/share"
APP_ID="io.github.enocoded.apdirs"
ICON_TARGET="$DESKTOP_DATA_DIR/icons/hicolor/256x256/apps/apdirs.png"
APPLICATIONS_DIR="$DESKTOP_DATA_DIR/applications"
DESKTOP_FILE="$APPLICATIONS_DIR/$APP_ID.desktop"
mkdir -p "$(dirname "$ICON_TARGET")" "$APPLICATIONS_DIR"
install -m 644 "$REPO_ROOT/assets/apdirs.png" "$ICON_TARGET"

WORKSPACE_TARGET="$HOME/Projects/client-work"
DESKTOP_WORKSPACE="${WORKSPACE_TARGET//\\/\\\\}"
DESKTOP_WORKSPACE="${DESKTOP_WORKSPACE//\"/\\\"}"
DESKTOP_WORKSPACE="${DESKTOP_WORKSPACE//%/%%}"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Apdirs
Comment=Open the Apdirs workspace in Nautilus
Exec=nautilus --new-window "$DESKTOP_WORKSPACE"
Terminal=false
Type=Application
Icon=apdirs
Categories=Utility;
EOF
chmod 644 "$DESKTOP_FILE"
echo "-> Installed application icon to $ICON_TARGET"
echo "-> Created desktop entry $DESKTOP_FILE"

# 7. Restart Nautilus to apply changes instantly
echo "-> Restarting Nautilus file manager..."
nautilus -q

echo ""
echo "Installation complete! Open the Apdirs workspace from your applications menu, run 'apdirs' from a terminal, or use the Nautilus right-click actions."