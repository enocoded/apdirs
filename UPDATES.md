# Changelog

Entries are listed in reverse chronological order; add new updates at the top.

## CI foundation — 2026-11-11

- Added Ubuntu GitHub Actions checks for core tests, Python syntax, and Linux shell syntax.
- Renamed the GTK preview script to `tests/ui_test.py` so unittest discovery does not import GTK in headless CI.
- Recorded that CD/release automation is deferred and Windows 11 CI will be added when that platform is developed.

## 1.0.5 — 2026-11-11

- Registered GTK dialogs with a desktop application ID and configured the Apdirs themed icon so Nautilus-launched windows display the correct taskbar icon.

## 1.0.4 — 2026-11-11

- Updated the desktop launcher to use the Apdirs icon and open the client-work workspace in Nautilus. The CLI remains terminal-only without a desktop icon.

## 1.0.3 — 2026-11-11

- Added Apdirs icon installation and desktop launcher generation.

## 1.0.2 — 2026-11-11

- Updated the Linux installer to install the `apdirs` CLI alongside the Nautilus extension. The install directory is configurable with `APDIRS_BIN_DIR`, and any existing CLI is preserved as a backup.

## 1.0.1 — 2026-11-11

- Updated CLI input normalization to use Python Unicode-aware trimming and lowercasing, matching the core behavior for international project names and labels.

## 1.0.0 — 2026-11-11

- Added a shared `VERSION` file used by package metadata, the CLI banner, and Nautilus menu labels.

## Earlier changes — 2026-11-11

- Updated ongoing project discovery to include only project directories matching the dated naming convention used by project creation. The project picker selects and focuses the first project by default.
- Refined the project picker with rounded list styling, improved dialog sizing, and consistent Apdirs window titles.
- Migrated the active dialogs from Tkinter to GTK, retaining the older Tkinter and GTK 3 implementations under `src/backup/`. The active interface uses GTK 4.
- Added GTK 4 dialogs for creating a project, selecting a project, choosing a target directory, and showing success or error messages. Preserved the existing return values expected by the runner.
- Added `src/style.py` to centralize GTK layout, button sizing and alignment, semantic color roles, and rounded button styling. Primary action colors follow the selected GNOME accent color, including hover and pressed states.
- Updated GTK installation dependencies and documentation for GTK 4.
- Added `tests/ui_test.py` to preview all dialogs or an individual dialog without creating project files.
- Organized legacy GUI files in `src/backup/`, moved the UI preview script to `tests/`, and updated references in the README and requirements notes.
