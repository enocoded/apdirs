import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox, Scrollbar, END

class ApdirsGui:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()

    def prompt_new_project(self):
        client = simpledialog.askstring("New Archviz Project", "Enter Client Name (e.g., abc-company):")
        if not client or not client.strip():
            return None, None
            
        project = simpledialog.askstring("New Archviz Project", "Enter Project Slug (e.g., modern-interior):")
        if not project or not project.strip():
            return None, None
            
        return client.strip(), project.strip()

    def prompt_select_project(self, projects):
        if not projects:
            messagebox.showwarning("No Projects", "No ongoing projects found.")
            return None

        selection = [None]
        top = Toplevel()
        top.title("Select Ongoing Project")
        top.geometry("400x300")
        top.grab_set()

        tk.Label(top, text="Select a project:", font=("Arial", 10, "bold")).pack(pady=10)

        frame = tk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lb = Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        for p in projects:
            lb.insert(END, p)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lb.yview)

        def on_select():
            selected_indices = lb.curselection()
            if selected_indices:
                selection[0] = lb.get(selected_indices[0])
                top.destroy()

        tk.Button(top, text="Select Project", command=on_select, bg="#005fb8", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        top.wait_window()
        return selection[0]

    def prompt_target_and_label(self):
        top = Toplevel()
        top.title("Add Dated Folder")
        top.geometry("380x230")
        top.grab_set()

        result = {"target": None, "label": None}

        tk.Label(top, text="Select Target Directory:", font=("Arial", 10, "bold")).pack(pady=5)
        
        target_var = tk.StringVar(value="1")
        tk.Radiobutton(top, text="01-inputs (includes subfolders & brief)", variable=target_var, value="1").pack(anchor="w", padx=25)
        tk.Radiobutton(top, text="03-deliverables", variable=target_var, value="2").pack(anchor="w", padx=25)

        tk.Label(top, text="Optional Folder Label (e.g., client-revision):", font=("Arial", 9)).pack(pady=5)
        entry_label = tk.Entry(top, width=35)
        entry_label.pack(padx=20)

        def on_submit():
            result["target"] = target_var.get()
            result["label"] = entry_label.get().strip()
            top.destroy()

        tk.Button(top, text="Create Folder", command=on_submit, bg="#005fb8", fg="white").pack(pady=10)

        top.wait_window()
        return result["target"], result["label"]

    def show_success(self, message):
        messagebox.showinfo("Success", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)