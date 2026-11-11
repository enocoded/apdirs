import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk
from src import style


class ApdirsGui:
    def __init__(self):
        style.initialize()

    def _create_dialog(self, title, width, height):
        return style.create_window(title, width, height)

    def _run_modal_window(self, dialog):
        loop = GLib.MainLoop()

        def on_close_request(_dialog):
            loop.quit()
            return False

        dialog.connect("close-request", on_close_request)
        dialog.present()
        loop.run()

    def _show_popup(self, message, is_error=False):
        # In GTK 4.10+, Gtk.AlertDialog is the native way to show alerts/popups
        # Fallback implementation using a standard modal Gtk.Window template for broad compatibility:
        dialog = self._create_dialog(style.APP_TITLE, 380, 180)

        box = style.create_content_box(spacing=style.FORM_SPACING, popup=True)
        dialog.set_child(box)

        heading_text = "Error" if is_error else "Success"
        box.append(style.create_heading(heading_text))

        lbl_msg = Gtk.Label(label=message, wrap=True)
        lbl_msg.set_xalign(0)
        box.append(lbl_msg)

        btn_box = style.create_button_row()
        box.append(btn_box)
        btn_ok = style.create_button(
            "OK", primary=not is_error, destructive=is_error
        )
        btn_ok.connect("clicked", lambda *_: dialog.close())
        btn_box.append(btn_ok)

        self._run_modal_window(dialog)

    def prompt_new_project(self):
        dialog = self._create_dialog("New Archviz Project", 400, 240)

        main_box = style.create_content_box(spacing=style.FORM_SPACING)
        dialog.set_child(main_box)

        main_box.append(style.create_heading("Create New Archviz Project"))

        entry_client = Gtk.Entry()
        entry_client.set_placeholder_text("Client Name (e.g., abc-company)")
        main_box.append(entry_client)

        entry_project = Gtk.Entry()
        entry_project.set_placeholder_text("Project Slug (e.g., modern-interior)")
        main_box.append(entry_project)

        btn_box = style.create_button_row()
        main_box.append(btn_box)

        btn_cancel = style.create_button("Cancel")
        btn_cancel.connect("clicked", lambda *_: dialog.close())
        btn_box.append(btn_cancel)

        result = {"client": None, "project": None}

        def on_create(*_):
            c = entry_client.get_text().strip()
            p = entry_project.get_text().strip()
            if c and p:
                result["client"] = c
                result["project"] = p
                dialog.close()
            else:
                self.show_error("Both client name and project slug are required.")

        btn_create = style.create_button("Create", primary=True)
        btn_create.connect("clicked", on_create)
        btn_box.append(btn_create)

        entry_client.grab_focus()

        self._run_modal_window(dialog)

        return result["client"], result["project"]

    def prompt_select_project(self, projects):
        if not projects:
            self.show_error("No ongoing projects found.")
            return None

        dialog = self._create_dialog("Select Ongoing Project", 400, 380)

        main_box = style.create_content_box()
        dialog.set_child(main_box)

        main_box.append(style.create_heading("Select Ongoing Project"))

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.add_css_class("card")
        main_box.append(scrolled_window)

        project_list = style.create_project_list()
        for project in projects:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=project, xalign=0)
            label.set_margin_start(12)
            label.set_margin_end(12)
            label.set_margin_top(10)
            label.set_margin_bottom(10)
            row.set_child(label)
            project_list.append(row)
        scrolled_window.set_child(project_list)

        btn_box = style.create_button_row()
        main_box.append(btn_box)

        btn_cancel = style.create_button("Cancel")
        btn_cancel.connect("clicked", lambda *_: dialog.close())
        btn_box.append(btn_cancel)

        selected_project = [None]

        def on_select(*_):
            row = project_list.get_selected_row()
            if row:
                selected_project[0] = projects[row.get_index()]
            dialog.close()

        btn_select = style.create_button("Select", primary=True)
        btn_select.connect("clicked", on_select)
        btn_box.append(btn_select)

        project_list.connect("row-activated", lambda _, row: (project_list.select_row(row), on_select()))

        self._run_modal_window(dialog)

        return selected_project[0]

    def prompt_target_and_label(self):
        dialog = self._create_dialog("Add Dated Folder", 400, 300)

        main_box = style.create_content_box()
        dialog.set_child(main_box)

        main_box.append(style.create_heading("Add Dated Folder"))

        target_heading = Gtk.Label(label="Select Target Directory:")
        target_heading.set_xalign(0)
        main_box.append(target_heading)

        inputs_radio = Gtk.CheckButton(label="01-inputs (includes subfolders & brief)")
        inputs_radio.set_active(True)
        main_box.append(inputs_radio)

        deliverables_radio = Gtk.CheckButton(label="03-deliverables")
        deliverables_radio.set_group(inputs_radio)
        main_box.append(deliverables_radio)

        entry_label = Gtk.Entry()
        entry_label.set_placeholder_text("Optional Folder Label (e.g., client-revision)")
        main_box.append(entry_label)

        btn_box = style.create_button_row()
        main_box.append(btn_box)

        btn_cancel = style.create_button("Cancel")
        btn_cancel.connect("clicked", lambda *_: dialog.close())
        btn_box.append(btn_cancel)

        result = [None, None]

        def on_create(*_):
            target = "1" if inputs_radio.get_active() else "2"
            lbl = entry_label.get_text().strip()
            result[0] = target
            result[1] = lbl
            dialog.close()

        btn_create = style.create_button("Create", primary=True)
        btn_create.connect("clicked", on_create)
        btn_box.append(btn_create)

        self._run_modal_window(dialog)

        return result[0], result[1]

    def show_success(self, message):
        self._show_popup(message)

    def show_error(self, message):
        self._show_popup(message, is_error=True)