import os
import subprocess
import sys
import urllib.parse
from pathlib import Path
from gi.repository import Nautilus, GObject

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
VERSION = Path(REPO_ROOT, "VERSION").read_text(encoding="utf-8").strip()

class ApdirsExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()

    def get_file_items(self, files):
        return []

    def get_background_items(self, current_folder):
        if not current_folder:
            return []

        try:
            folder_uri = current_folder.get_uri()
            folder_path = urllib.parse.unquote(folder_uri.replace("file://", ""))

            if "client-work" not in folder_path and "Projects" not in folder_path:
                return []

            item_new = Nautilus.MenuItem(
                name="Apdirs::NewProject",
                label=f"Create New Archviz Project...",
                tip="Initialize a new standardized archviz project directory"
            )
            item_new.connect("activate", self.menu_new_project_clicked)

            item_add = Nautilus.MenuItem(
                name="Apdirs::AddDatedFolder",
                label=f"Create Dated Folder to Project...",
                tip="Inject a new dated folder into an existing project"
            )
            item_add.connect("activate", self.menu_add_folder_clicked)

            return [item_new, item_add]
        except Exception as e:
            return []

    def menu_new_project_clicked(self, *args):
        runner_script = os.path.join(REPO_ROOT, "src", "runner.py")
        subprocess.Popen([sys.executable, runner_script, "new"])

    def menu_add_folder_clicked(self, *args):
        runner_script = os.path.join(REPO_ROOT, "src", "runner.py")
        subprocess.Popen([sys.executable, runner_script, "add"])