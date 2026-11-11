import os
import urllib.parse
from gi.repository import Nautilus, GObject
from apdirs.core import ApdirsCore
from apdirs.gui import ApdirsGui

class ApdirsExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self.core = ApdirsCore()
        self.gui = ApdirsGui()

    def get_file_items(self, files):
        return []

    def get_background_items(self, current_folder):
        if not current_folder:
            return []

        folder_uri = current_folder.get_uri()
        folder_path = urllib.parse.unquote(folder_uri.replace("file://", ""))

        if "client-work" not in folder_path:
            return []

        item_new = Nautilus.MenuItem(
            name="Apdirs::NewProject",
            label="✨ Create New Archviz Project...",
            tip="Initialize a new standardized archviz project directory"
        )
        item_new.connect("activate", self.menu_new_project_clicked)

        item_add = Nautilus.MenuItem(
            name="Apdirs::AddDatedFolder",
            label="📁 Add Dated Folder to Project...",
            tip="Inject a new dated folder into an existing project"
        )
        item_add.connect("activate", self.menu_add_folder_clicked)

        return [item_new, item_add]

    def menu_new_project_clicked(self, menu, target):
        client, project = self.gui.prompt_new_project()
        if client and project:
            try:
                self.core.create_project(client, project)
                self.gui.show_success("Project directory structure created successfully!")
            except Exception as e:
                self.gui.show_error(str(e))

    def menu_add_folder_clicked(self, menu, target):
        projects = self.core.get_ongoing_projects()
        if not projects:
            self.gui.show_error("No ongoing projects found in client-work workspace.")
            return

        selected_project = self.gui.prompt_select_project(projects)
        if not selected_project:
            return

        target_type, label = self.gui.prompt_target_and_label()
        if not target_type:
            return

        try:
            self.core.add_dated_folder(selected_project, target_type, label)
            self.gui.show_success(f"Dated folder successfully created in {selected_project}!")
        except Exception as e:
            self.gui.show_error(str(e))