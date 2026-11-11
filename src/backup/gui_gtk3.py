import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

APP_TITLE = "Apdirs - Archviz Project Manager"


class ApdirsGui:
    def _create_dialog(self, width, height):
        dialog = Gtk.Dialog(title=APP_TITLE, flags=Gtk.DialogFlags.MODAL)
        dialog.set_default_size(width, height)
        dialog.set_resizable(False)
        dialog.set_position(Gtk.WindowPosition.CENTER)
        content = dialog.get_content_area()
        content.set_border_width(18)
        content.set_spacing(12)
        return dialog

    def _add_heading(self, container, text):
        heading = Gtk.Label()
        heading.set_markup(f"<b>{text}</b>")
        heading.set_xalign(0)
        container.pack_start(heading, False, False, 0)
        return heading

    def _show_popup(self, message, is_error=False):
        message_type = Gtk.MessageType.ERROR if is_error else Gtk.MessageType.INFO
        heading = "Error" if is_error else "Success"
        dialog = Gtk.MessageDialog(
            flags=Gtk.DialogFlags.MODAL,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=heading,
        )
        dialog.set_title(APP_TITLE)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def prompt_new_project(self):
        dialog = self._create_dialog(400, 240)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Create", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        self._add_heading(content, "Create New Archviz Project")

        entry_client = Gtk.Entry()
        entry_client.set_placeholder_text("Client Name (e.g., abc-company)")
        entry_client.set_activates_default(True)
        content.pack_start(entry_client, False, False, 0)

        entry_project = Gtk.Entry()
        entry_project.set_placeholder_text("Project Slug (e.g., modern-interior)")
        entry_project.set_activates_default(True)
        content.pack_start(entry_project, False, False, 0)
        entry_client.grab_focus()
        dialog.show_all()

        while dialog.run() == Gtk.ResponseType.OK:
            client = entry_client.get_text().strip()
            project = entry_project.get_text().strip()
            if client and project:
                dialog.destroy()
                return client, project
            self.show_error("Both client name and project slug are required.")

        dialog.destroy()
        return None, None

    def prompt_select_project(self, projects):
        if not projects:
            self.show_error("No ongoing projects found.")
            return None

        dialog = self._create_dialog(400, 380)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Select", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        self._add_heading(content, "Select Ongoing Project")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_shadow_type(Gtk.ShadowType.IN)
        content.pack_start(scrolled_window, True, True, 0)

        project_list = Gtk.ListBox()
        project_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        for project in projects:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=project, xalign=0)
            label.set_margin_start(10)
            label.set_margin_end(10)
            label.set_margin_top(7)
            label.set_margin_bottom(7)
            row.add(label)
            project_list.add(row)
        project_list.select_row(project_list.get_row_at_index(0))

        def activate_project_row(list_widget, row):
            list_widget.select_row(row)
            dialog.response(Gtk.ResponseType.OK)

        project_list.connect("row-activated", activate_project_row)
        scrolled_window.add(project_list)

        dialog.show_all()
        response = dialog.run()
        selected_row = project_list.get_selected_row()
        selected_project = (
            projects[selected_row.get_index()]
            if response == Gtk.ResponseType.OK and selected_row is not None
            else None
        )
        dialog.destroy()
        return selected_project

    def prompt_target_and_label(self):
        dialog = self._create_dialog(400, 300)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Create", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        self._add_heading(content, "Add Dated Folder")

        target_heading = Gtk.Label(label="Select Target Directory:")
        target_heading.set_xalign(0)
        content.pack_start(target_heading, False, False, 0)

        inputs_radio = Gtk.RadioButton.new_with_label_from_widget(
            None, "01-inputs (includes subfolders & brief)"
        )
        content.pack_start(inputs_radio, False, False, 0)

        deliverables_radio = Gtk.RadioButton.new_with_label_from_widget(
            inputs_radio, "03-deliverables"
        )
        content.pack_start(deliverables_radio, False, False, 0)

        entry_label = Gtk.Entry()
        entry_label.set_placeholder_text("Optional Folder Label (e.g., client-revision)")
        entry_label.set_activates_default(True)
        content.pack_start(entry_label, False, False, 0)
        entry_label.grab_focus()

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            result = (
                "1" if inputs_radio.get_active() else "2",
                entry_label.get_text().strip(),
            )
        else:
            result = (None, None)
        dialog.destroy()
        return result

    def show_success(self, message):
        self._show_popup(message)

    def show_error(self, message):
        self._show_popup(message, is_error=True)
