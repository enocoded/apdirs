import os
import urllib.parse
from gi.repository import Nautilus, GObject
# Import your core logic here once packaged
from src.core import ApdirsCore
from src.gui import ApdirsGui  # Tkinter prompt dialogs

class ApdirsExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self.core = ApdirsCore()
        self.gui = ApdirsGui()

    def get_file_items(self, files):
        return []

    def get_background_items(self, current_folder):
        """Adds options when right-clicking inside the client-work folder background."""
        if not current_folder:
            return []

        folder_uri = current_folder.get_uri()
        folder_path = urllib.parse.unquote(folder_uri.replace("file://", ""))

        # Only show menu if we are inside the client-work workspace
        if "client-work" not in folder_path:
            return []

        item = Nautilus.MenuItem(
            name="Apdirs::NewProject",
            label="✨ Create New Archviz Project...",
            tip="Initialize a new standardized archviz project directory"
        )
        item.connect("activate", self.menu_new_project_clicked)

        return [item]

    def menu_new_project_clicked(self, menu, target):
        client, project = self.gui.prompt_new_project()
        if client and project:
            try:
                self.core.create_project(client, project)
                self.gui.show_success("Project created successfully!")
            except Exception as e:
                self.gui.show_error(str(e))