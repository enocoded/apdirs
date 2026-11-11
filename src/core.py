import os
import shutil
from datetime import datetime

class ApdirsCore:
    def __init__(self, base_dir=None, template_dir=None):
        self.base_dir = base_dir or os.path.expanduser("~/Projects/client-work")
        self.template_dir = template_dir or os.path.join(self.base_dir, "templates")

    def create_project(self, client_input, project_input):
        client_name = client_input.strip().lower().replace(" ", "-")
        project_slug = project_input.strip().lower().replace(" ", "-")
        
        if not client_name or not project_slug:
            raise ValueError("Client name and project slug cannot be empty.")

        current_date = datetime.now().strftime("%Y-%m-%d")
        project_folder = f"{current_date}_{client_name}_{project_slug}"
        full_path = os.path.join(self.base_dir, project_folder)

        # Create structured directories
        os.makedirs(os.path.join(full_path, f"01-inputs/{current_date}/drawings"), exist_ok=True)
        os.makedirs(os.path.join(full_path, f"01-inputs/{current_date}/refs"), exist_ok=True)
        os.makedirs(os.path.join(full_path, f"01-inputs/{current_date}/insps"), exist_ok=True)

        for sub in ["components", "export", "assets/maps", "assets/meshes", "assets/hdris", "ro", "post"]:
            os.makedirs(os.path.join(full_path, "02-production", sub), exist_ok=True)

        os.makedirs(os.path.join(full_path, "03-deliverables"), exist_ok=True)

        # Copy brief template if available
        brief_src = os.path.join(self.template_dir, "brief-template.docx")
        if os.path.exists(brief_src):
            brief_dst = os.path.join(full_path, f"01-inputs/{current_date}/{current_date}_{project_slug}_brief.docx")
            shutil.copy(brief_src, brief_dst)

        return full_path

    def get_ongoing_projects(self):
        if not os.path.exists(self.base_dir):
            return []

        projects = []
        for directory in os.listdir(self.base_dir):
            if directory.startswith(".") or not os.path.isdir(os.path.join(self.base_dir, directory)):
                continue

            try:
                date, client, project = directory.split("_", 2)
                if datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d") != date:
                    continue
            except ValueError:
                continue

            if client and project:
                projects.append(directory)

        return sorted(projects)

    def add_dated_folder(self, project_name, target_type, label_input=""):
        selected_project_path = os.path.join(self.base_dir, project_name)
        target_dir = os.path.join(selected_project_path, "01-inputs" if target_type == "1" else "03-deliverables")
        
        today = datetime.now().strftime("%Y-%m-%d")
        if not label_input.strip():
            folder_name = today
        else:
            clean_label = label_input.strip().lower().replace(" ", "-")
            folder_name = f"{today}_{clean_label}"

        final_target = os.path.join(target_dir, folder_name)
        os.makedirs(final_target, exist_ok=True)

        if target_type == "1":
            for sub in ["drawings", "refs", "insps"]:
                os.makedirs(os.path.join(final_target, sub), exist_ok=True)

            brief_src = os.path.join(self.template_dir, "brief-template.docx")
            if os.path.exists(brief_src):
                brief_dst = os.path.join(final_target, f"{folder_name}_brief.docx")
                shutil.copy(brief_src, brief_dst)

        return final_target