"""Legacy Tkinter GUI retained as a fallback."""

import tkinter as tk
from tkinter import Toplevel, Listbox, Scrollbar, END
from src.backup import style_tk as style

class ApdirsGui:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()

    def _force_focus(self, top, focus_widget=None):
        top.lift()
        top.attributes('-topmost', True)
        top.after_idle(lambda: top.attributes('-topmost', False))
        
        if focus_widget:
            top.after(150, lambda: [focus_widget.focus_force(), focus_widget.focus_set()])

    def _show_popup(self, message, is_error=False):
        top = Toplevel()
        style.setup_dialog(top, 400, 180)

        accent = style.ACCENT_ERROR if is_error else style.ACCENT_PRIMARY
        title_text = "Error" if is_error else "Success"

        header_frame = tk.Frame(top, bg=style.BG_COLOR)
        header_frame.pack(fill=tk.X, padx=25, pady=(18, 5))
        
        tk.Label(
            header_frame, text=title_text, font=style.FONT_TITLE, 
            bg=style.BG_COLOR, fg=style.FG_COLOR
        ).pack(side=tk.LEFT)

        tk.Label(
            top, text=message, font=style.FONT_BODY, 
            bg=style.BG_COLOR, fg=style.TEXT_SECONDARY, wraplength=350, justify="center"
        ).pack(pady=10, padx=25)

        btn_ok = style.RoundedButton(top, "OK", top.destroy, width=120, height=36, bg=accent)
        btn_ok.pack(pady=(5, 15))

        top.bind("<Return>", lambda event: top.destroy())
        top.bind("<Escape>", lambda event: top.destroy())
        
        self._force_focus(top, btn_ok)
        top.wait_window()

    def prompt_new_project(self):
        selection = {"client": None, "project": None}
        top = Toplevel()
        style.setup_dialog(top, 400, 240)

        tk.Label(
            top, text="Create New Archviz Project", font=style.FONT_TITLE,
            bg=style.BG_COLOR, fg=style.FG_COLOR
        ).pack(pady=(18, 12))

        form_frame = tk.Frame(top, bg=style.BG_COLOR)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25)

        entry_client = style.RoundedEntry(form_frame, placeholder="Client Name (e.g., abc-company)", width=350, height=46, border_color=style.ACCENT_PRIMARY)
        entry_client.pack(anchor="center", pady=(0, 10))

        entry_project = style.RoundedEntry(form_frame, placeholder="Project Slug (e.g., modern-interior)", width=350, height=46, border_color=style.BORDER_COLOR)
        entry_project.pack(anchor="center", pady=(0, 10))

        def on_submit():
            c = entry_client.get()
            p = entry_project.get()
            if c and p:
                selection["client"] = c
                selection["project"] = p
                top.destroy()
            else:
                self.show_error("Both client name and project slug are required.")

        btn_create = style.RoundedButton(top, "Create", on_submit, width=140, height=38)
        btn_create.pack(pady=(0, 15))

        top.bind("<Return>", lambda event: on_submit())
        top.bind("<Escape>", lambda event: top.destroy())

        self._force_focus(top, entry_client)
        top.wait_window()
        return selection["client"], selection["project"]

    def prompt_select_project(self, projects):
        if not projects:
            self.show_error("No ongoing projects found.")
            return None

        selection = [None]
        top = Toplevel()
        style.setup_dialog(top, 400, 380)

        tk.Label(
            top, text="Select Ongoing Project", font=style.FONT_TITLE,
            bg=style.BG_COLOR, fg=style.FG_COLOR
        ).pack(pady=(18, 12))

        frame = tk.Frame(top, bg=style.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=25)

        scrollbar = Scrollbar(frame, bg=style.BG_COLOR, troughcolor=style.INPUT_BG, activerelief="flat", width=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        list_canvas = tk.Canvas(
            frame, bg=style.BG_COLOR, highlightthickness=0, bd=0, width=310, height=210
        )
        list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lb = Listbox(
            list_canvas, yscrollcommand=scrollbar.set, font=style.FONT_BODY,
            bg=style.INPUT_BG, fg=style.FG_COLOR, selectbackground=style.ACCENT_PRIMARY, selectforeground=style.FG_COLOR,
            relief="flat", borderwidth=0, highlightthickness=0
        )
        for p in projects:
            lb.insert(END, p)
        lb.selection_set(0)
        lb.activate(0)

        list_window = list_canvas.create_window(6, 6, anchor="nw", window=lb)

        def resize_list(event):
            list_canvas.delete("list-border")
            style.create_rounded_rect(
                list_canvas, 1, 1, event.width - 1, event.height - 1,
                radius=12, fill=style.INPUT_BG, outline=style.BORDER_COLOR,
                width=2, tags="list-border"
            )
            list_canvas.tag_lower("list-border")
            list_canvas.itemconfigure(
                list_window, width=max(1, event.width - 12), height=max(1, event.height - 12)
            )

        list_canvas.bind("<Configure>", resize_list)
        scrollbar.config(command=lb.yview)

        def on_select():
            selected_indices = lb.curselection()
            if selected_indices:
                selection[0] = lb.get(selected_indices[0])
                top.destroy()

        btn_select = style.RoundedButton(top, "Select", on_select, width=140, height=38)
        btn_select.pack(pady=15)

        top.bind("<Double-Button-1>", lambda event: on_select())
        top.bind("<Escape>", lambda event: top.destroy())

        self._force_focus(top, lb)
        top.wait_window()
        return selection[0]

    def prompt_target_and_label(self):
        top = Toplevel()
        style.setup_dialog(top, 400, 270)

        result = {"target": None, "label": None}

        tk.Label(
            top, text="Add Dated Folder", font=style.FONT_TITLE,
            bg=style.BG_COLOR, fg=style.FG_COLOR
        ).pack(pady=(18, 10))

        content_frame = tk.Frame(top, bg=style.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25)

        tk.Label(content_frame, text="Select Target Directory:", font=style.FONT_LABEL_BOLD, bg=style.BG_COLOR, fg=style.TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
        
        target_var = tk.StringVar(value="1")
        rb1 = tk.Radiobutton(
            content_frame, text="01-inputs (includes subfolders & brief)", variable=target_var, value="1",
            indicatoron=False, relief=tk.FLAT, overrelief=tk.FLAT, borderwidth=0,
            highlightthickness=0, padx=12, pady=8, anchor="w",
            bg=style.INPUT_BG, fg=style.TEXT_SECONDARY, selectcolor=style.ACCENT_PRIMARY,
            activebackground=style.ACCENT_HOVER, activeforeground=style.FG_COLOR,
            font=style.FONT_LABEL
        )
        rb1.pack(fill=tk.X, pady=3)
        
        rb2 = tk.Radiobutton(
            content_frame, text="03-deliverables", variable=target_var, value="2",
            indicatoron=False, relief=tk.FLAT, overrelief=tk.FLAT, borderwidth=0,
            highlightthickness=0, padx=12, pady=8, anchor="w",
            bg=style.INPUT_BG, fg=style.TEXT_SECONDARY, selectcolor=style.ACCENT_PRIMARY,
            activebackground=style.ACCENT_HOVER, activeforeground=style.FG_COLOR,
            font=style.FONT_LABEL
        )
        rb2.pack(fill=tk.X, pady=3)

        entry_label = style.RoundedEntry(content_frame, placeholder="Optional Folder Label (e.g., client-revision)", width=350, height=46, border_color=style.BORDER_COLOR)
        entry_label.pack(anchor="center", pady=(10, 0))

        def on_submit():
            result["target"] = target_var.get()
            result["label"] = entry_label.get()
            top.destroy()

        btn_create = style.RoundedButton(top, "Create", on_submit, width=140, height=38)
        btn_create.pack(pady=12)

        top.bind("<Return>", lambda event: on_submit())
        top.bind("<Escape>", lambda event: top.destroy())

        self._force_focus(top, entry_label)
        top.wait_window()
        return result["target"], result["label"]

    def show_success(self, message):
        self._show_popup(message, is_error=False)

    def show_error(self, message):
        self._show_popup(message, is_error=True)