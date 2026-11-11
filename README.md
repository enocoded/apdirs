# Apdirs - Archviz Project Manager

Apdirs is a standardized project directory management tool built for Archviz professionals on Ubuntu GNOME. It automates clean 3-tier folder hierarchies (`01-inputs`, `02-production`, `03-deliverables`), handles master document templates, and integrates directly into GNOME Files (Nautilus) via right-click context menus.

The GTK 4 dialogs use the selected GNOME accent color for primary buttons, with rounded corners and hover/pressed states configured in `src/style.py`. Other controls inherit the selected Ubuntu theme. Legacy Tkinter and GTK 3 implementations are preserved in `src/backup/`.

To preview the dialogs without creating or changing any project files, run:
```bash
python3 tests/ui_test.py
```
Pass `create`, `select`, `target`, `success`, or `error` to preview one dialog.

## Development checks

GitHub Actions runs the automated core tests, Python syntax checks, and Linux
shell syntax checks on Ubuntu for pushes and pull requests. GTK previews remain
manual. Current CI/CD decisions and future release and Windows plans are tracked
in [CI_CD_PLAN.md](CI_CD_PLAN.md).

## Features
- **Instant Project Initialization:** Creates structured input, production, and deliverable subdirectories instantly.
- **Template Automation:** Automatically copies and timestamps master `.docx` project briefs.
- **Ongoing Project Management:** Easily inject dated folders (`YYYY-MM-DD` or `YYYY-MM-DD_label`) into existing client workspaces.
- **Nautilus Integration:** Native GUI popup dialogs right inside your file manager.

## Installation on Ubuntu

The installer adds the `apdirs` command alongside the Nautilus extension and installs the Apdirs icon and desktop entry. The entry opens `~/Projects/client-work` in Nautilus, where the Apdirs right-click actions are available; GTK dialogs opened from those actions also use the Apdirs icon in the desktop shell. The CLI remains terminal-only and has no desktop icon. By default, the command installs to `~/.local/bin`. To choose another directory, set `APDIRS_BIN_DIR` when running the installer:
```bash
APDIRS_BIN_DIR="$HOME/bin" platforms/linux-nautilus/install.sh
```
Make sure the chosen directory is on your `PATH` to run `apdirs` directly. If an `apdirs` file already exists there, the installer preserves it as `apdirs.backup`.

1. Clone or download the repository:
   ```bash
   cd ~/GitHub/apdirs