import tkinter as tk

# --- Theme Colors & Typography ---
BG_COLOR = "#242424"
FG_COLOR = "#ffffff"
TEXT_MUTED = "#888888"
TEXT_SECONDARY = "#cccccc"
TEXT_LIGHT = "#dddddd"

ACCENT_PRIMARY = "#b85b3b"
ACCENT_HOVER = "#cc6644"
ACCENT_ERROR = "#c73e3a"

INPUT_BG = "#212121"
BORDER_COLOR = "#444444"

FONT_FAMILY = "Ubuntu"
FONT_TITLE = (FONT_FAMILY, 12, "bold")
FONT_LABEL_BOLD = (FONT_FAMILY, 10, "bold")
FONT_LABEL = (FONT_FAMILY, 9)
FONT_BODY = (FONT_FAMILY, 10)

def setup_dialog(top, width, height):
    """Applies standard window configuration, dialog hints, and dark theme safely."""
    top.title("Apdirs")
    top.geometry(f"{width}x{height}")
    top.resizable(False, False)
    top.configure(bg=BG_COLOR)
    try:
        top.attributes('-type', 'dialog')
    except Exception:
        pass
    
    # Defer grab until the window is viewable and mapped by the window manager
    top.after_idle(top.grab_set)

def create_rounded_rect(canvas, x1, y1, x2, y2, radius=8, **kwargs):
    """Draws a smooth rounded rectangle on a canvas."""
    points = [
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
        x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
        x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
        x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
        x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=24)

class RoundedEntry(tk.Canvas):
    """Custom rounded text entry container with internal placeholder support."""
    def __init__(self, parent, placeholder="", width=350, height=46, bg=INPUT_BG, border_color=BORDER_COLOR, focus_color=ACCENT_PRIMARY, font=FONT_BODY):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0)
        self.placeholder = placeholder
        self.bg_color = bg
        self.border_color = border_color
        self.focus_color = focus_color
        
        self.rect = create_rounded_rect(self, 2, 2, width-2, height-2, radius=12, fill=bg, outline=border_color, width=2)
        
        self.entry = tk.Entry(
            self, bg=bg, fg=TEXT_MUTED, insertbackground=FG_COLOR, font=font, 
            relief="flat", highlightthickness=0
        )
        self.create_window(width // 2, height // 2, window=self.entry, width=width - 30, height=height - 16)
        
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.bind("<FocusIn>", self._on_focus_in)
            self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=FG_COLOR)
        self.itemconfig(self.rect, outline=self.focus_color)

    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=TEXT_MUTED)
        self.itemconfig(self.rect, outline=self.border_color)

    def get(self):
        val = self.entry.get()
        return "" if val == self.placeholder else val.strip()
        
    def focus_set(self):
        self.entry.focus_set()

class RoundedButton(tk.Canvas):
    """Custom pill-shaped rounded button with exact height and hover effect."""
    def __init__(self, parent, text, command, width=140, height=38, bg=ACCENT_PRIMARY, fg=FG_COLOR, font=FONT_LABEL_BOLD):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0, cursor="hand2")
        self.command = command
        self.bg = bg
        self.hover_bg = ACCENT_HOVER
        
        radius = 38
        self.rect = create_rounded_rect(self, 1, 1, width-1, height-1, radius=radius, fill=bg, outline="", width=0)
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill=fg, font=font)
        
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self.itemconfig(self.rect, fill=self.hover_bg))
        self.bind("<Leave>", lambda e: self.itemconfig(self.rect, fill=self.bg))