import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.gui import ApdirsGui


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preview Apdirs GTK dialogs.")
    parser.add_argument(
        "dialog",
        nargs="?",
        choices=("all", "create", "select", "target", "success", "error"),
        default="all",
        help="Dialog to preview (default: all)",
    )
    args = parser.parse_args(argv)
    gui = ApdirsGui()

    if args.dialog in ("all", "create"):
        print("Create project result:", gui.prompt_new_project())

    if args.dialog in ("all", "select"):
        print(
            "Selected project:",
            gui.prompt_select_project(
                [
                    "2026-01-15_example-client_modern-interior",
                    "2026-02-02_studio-example_lakeside-house",
                    "2026-03-10_archviz-demo_city-apartment",
                ]
            ),
        )

    if args.dialog in ("all", "target"):
        print("Target and label:", gui.prompt_target_and_label())

    if args.dialog in ("all", "success"):
        gui.show_success("This is a success message preview.")

    if args.dialog in ("all", "error"):
        gui.show_error("This is an error message preview.")


if __name__ == "__main__":
    main()
