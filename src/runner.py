import sys
import os

# Ensure repository root is in Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.core import ApdirsCore
from src.gui import ApdirsGui

def run_new_project():
    core = ApdirsCore()
    gui = ApdirsGui()
    client, project = gui.prompt_new_project()
    if client and project:
        try:
            core.create_project(client, project)
            gui.show_success("Project directory structure created successfully!")
        except Exception as e:
            gui.show_error(str(e))

def run_add_folder():
    core = ApdirsCore()
    gui = ApdirsGui()
    projects = core.get_ongoing_projects()
    if not projects:
        gui.show_error("No ongoing projects found in client-work workspace.")
        return

    selected_project = gui.prompt_select_project(projects)
    if not selected_project:
        return

    target_type, label = gui.prompt_target_and_label()
    if not target_type:
        return

    try:
        core.add_dated_folder(selected_project, target_type, label)
        gui.show_success(f"Dated folder successfully created in {selected_project}!")
    except Exception as e:
        gui.show_error(str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "new":
            run_new_project()
        elif cmd == "add":
            run_add_folder()