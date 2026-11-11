import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

from src.core import ApdirsCore


class ApdirsCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir.name
        self.core = ApdirsCore(base_dir=self.base_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_project_creates_structure_and_copies_template(self):
        template_dir = os.path.join(self.base_dir, "templates")
        os.makedirs(template_dir)
        template_path = os.path.join(template_dir, "brief-template.docx")
        with open(template_path, "wb") as template:
            template.write(b"test brief")

        with patch("src.core.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = datetime(2026, 11, 11)
            project_path = self.core.create_project("Example Client", "Modern Interior")
        today = "2026-11-11"
        project_name = f"{today}_example-client_modern-interior"

        self.assertEqual(os.path.basename(project_path), project_name)
        for relative_path in (
            f"01-inputs/{today}/drawings",
            f"01-inputs/{today}/refs",
            f"01-inputs/{today}/insps",
            "02-production/components",
            "02-production/export",
            "02-production/assets/maps",
            "02-production/assets/meshes",
            "02-production/assets/hdris",
            "02-production/ro",
            "02-production/post",
            "03-deliverables",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue(os.path.isdir(os.path.join(project_path, relative_path)))

        brief_path = os.path.join(
            project_path,
            "01-inputs",
            today,
            f"{today}_modern-interior_brief.docx",
        )
        with open(brief_path, "rb") as brief:
            self.assertEqual(brief.read(), b"test brief")

    def test_create_project_rejects_empty_names(self):
        with self.assertRaises(ValueError):
            self.core.create_project(" ", "valid-project")

    def test_get_ongoing_projects_returns_sorted_valid_project_directories(self):
        valid_projects = (
            "2026-01-15_example-client_modern-interior",
            "2026-02-02_studio-example_lakeside-house",
        )
        invalid_entries = (
            "not-a-project",
            "2026-13-02_client_project",
            "2026-02-02__missing-client",
        )
        for entry in valid_projects + invalid_entries:
            os.makedirs(os.path.join(self.base_dir, entry))
        with open(os.path.join(self.base_dir, "2026-03-10_client_file"), "w") as file:
            file.write("not a directory")

        self.assertEqual(self.core.get_ongoing_projects(), sorted(valid_projects))

    def test_add_dated_input_folder_creates_subfolders_and_copies_template(self):
        project_name = "2026-01-15_example-client_modern-interior"
        project_path = os.path.join(self.base_dir, project_name)
        os.makedirs(project_path)
        template_dir = os.path.join(self.base_dir, "templates")
        os.makedirs(template_dir)
        template_path = os.path.join(template_dir, "brief-template.docx")
        with open(template_path, "wb") as template:
            template.write(b"test brief")

        with patch("src.core.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = datetime(2026, 11, 11)
            folder_path = self.core.add_dated_folder(
                project_name, "1", "Client Revision"
            )
        expected_name = "2026-11-11_client-revision"

        self.assertEqual(os.path.basename(folder_path), expected_name)
        for subfolder in ("drawings", "refs", "insps"):
            with self.subTest(subfolder=subfolder):
                self.assertTrue(os.path.isdir(os.path.join(folder_path, subfolder)))
        self.assertTrue(
            os.path.isfile(os.path.join(folder_path, f"{expected_name}_brief.docx"))
        )

    def test_add_dated_deliverable_folder_uses_deliverables_directory(self):
        project_name = "2026-01-15_example-client_modern-interior"
        with patch("src.core.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = datetime(2026, 11, 11)
            folder_path = self.core.add_dated_folder(project_name, "2")

        self.assertEqual(
            folder_path,
            os.path.join(
                self.base_dir,
                project_name,
                "03-deliverables",
                "2026-11-11",
            ),
        )


if __name__ == "__main__":
    unittest.main()
