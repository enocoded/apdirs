---
description: "Use for Apdirs project changes, including Python core logic, GTK UI, Nautilus integration, testing, installation, and documentation. Covers architecture, coordinated files, and changelog maintenance."
applyTo: "**"
---

# Apdirs Project Rules

## Project Map

| Area | Files | Keep in sync |
|---|---|---|
| Project filesystem behavior | `src/core.py` | Project naming, discovery, and dated-folder creation |
| Active GUI | `src/gui.py` | Public GUI methods and return values consumed by `src/runner.py` |
| GTK styling | `src/style.py` | GTK 4 layout, selected GNOME accent color, and button styling |
| Workflow orchestration | `src/runner.py` | Calls GUI and core; preserve cancellation and return-value handling |
| Nautilus integration | `platforms/linux-nautilus/apdirs_nautilus.py` | Menu actions and launching `src/runner.py` |
| Installer and desktop launcher | `platforms/linux-nautilus/install.sh` | System packages must match GTK and Nautilus APIs used by the app; keep the GTK application ID, desktop-entry filename, and installed icon consistent |
| UI preview | `tests/ui_test.py` | Manual previews for create, select, target, success, and error dialogs |
| Legacy implementations | `src/backup/` | Reference only; do not treat as the active GUI |
| Project overview | `README.md` | User-facing usage, installation, and UI preview commands |
| Change history | `UPDATES.md` | Add dated entries at the top, in reverse chronological order |
| Python package metadata | `setup.py`, `requirements.txt` | Keep dependencies and supported Python version accurate |

## Implementation Rules

- The active GUI uses GTK 4 through PyGObject. Do not use GTK 3 APIs such as `Gtk.Dialog.run()`, `Gtk.ListBox.add()`, or `Gtk.RadioButton`.
- Associate GTK windows with the registered application ID and set the installed `apdirs` themed icon so the desktop shell can identify Apdirs windows.
- GTK modal workflows use `GLib.MainLoop`; GTK 4 grouped choices use `Gtk.CheckButton.set_group()`, and list rows use `Gtk.ListBox.append()`.
- Put GTK colors, theme/accent behavior, sizing, spacing, CSS, and reusable widget construction in `src/style.py`, not in `src/gui.py`.
- Preserve Ubuntu/GNOME theme colors unless the task specifically changes them. Primary button accent behavior must stay consistent with the desktop `org.gnome.desktop.interface` accent-color setting.
- Preserve the public GUI method names, arguments, and return shapes used by `src/runner.py`. If changing them, update all callers and tests in the same change.
- Keep GTK 3 and Tkinter backups under `src/backup/`. Do not import them into the active execution path unless explicitly requested.
- Keep Nautilus integration thin: it should invoke the runner rather than duplicate project or GUI logic.

## Validation and Documentation

- For GTK changes, run `python3 -m py_compile` on changed Python files and use `python3 tests/ui_test.py <dialog>` for relevant interactive previews when a display is available.
- Check installer package names and README installation steps whenever GUI toolkit requirements change.
- Update `UPDATES.md` for implemented user-facing or structural changes. Add the newest dated section or bullets at the top; never append newer history below older entries.
- Keep `README.md` focused on user setup and usage; use this instruction file for agent workflow and coordinated-file guidance.
