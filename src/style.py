import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gio, Gtk

_provider = None
_application = None

APP_TITLE = "Apdirs - Archviz Project Manager"
APP_ID = "io.github.enocoded.apdirs"
APP_ICON_NAME = "apdirs"
WINDOW_MARGIN = 20
POPUP_MARGIN = 24
CONTENT_SPACING = 12
FORM_SPACING = 16
BUTTON_SPACING = 12
BUTTON_MIN_WIDTH = 64
BUTTON_MIN_HEIGHT = 24
BUTTON_PADDING_VERTICAL = 10
BUTTON_PADDING_HORIZONTAL = 24
HEADING_STYLE_CLASS = "title-4"
WINDOW_STYLE_CLASS = "app-window"
BUTTON_STYLE_CLASS = "apdirs-button"
PROJECT_LIST_STYLE_CLASS = "navigation-sidebar"
ACCENT_BUTTON_STYLE_CLASS = "accent-action"

THEME_COLOR_CLASSES = {
    "primary": ACCENT_BUTTON_STYLE_CLASS,
    "destructive": "destructive-action",
    "project_selection": PROJECT_LIST_STYLE_CLASS,
}

ACCENT_PALETTES = {
    "blue": ("#3584e4", "#1c71d8", "#1558a1", "#ffffff"),
    "teal": ("#2190a4", "#1b798a", "#155f6c", "#ffffff"),
    "green": ("#3a944a", "#2f7b3d", "#245f30", "#ffffff"),
    "yellow": ("#c88800", "#a87100", "#805600", "#241f31"),
    "orange": ("#e95420", "#c84613", "#a83b10", "#ffffff"),
    "red": ("#e62d42", "#c91f34", "#a51a2b", "#ffffff"),
    "pink": ("#d56199", "#bd4e84", "#9d3e6e", "#ffffff"),
    "purple": ("#9141ac", "#793692", "#612b75", "#ffffff"),
    "slate": ("#6f8396", "#5a6e81", "#475969", "#ffffff"),
    "brown": ("#986a44", "#805838", "#66472e", "#ffffff"),
}


def _selected_accent_palette():
    schema_source = Gio.SettingsSchemaSource.get_default()
    schema = (
        schema_source.lookup("org.gnome.desktop.interface", True)
        if schema_source is not None
        else None
    )
    if schema is None or not schema.has_key("accent-color"):
        return None

    accent_name = Gio.Settings.new("org.gnome.desktop.interface").get_string(
        "accent-color"
    )
    try:
        return ACCENT_PALETTES[accent_name]
    except KeyError as error:
        raise ValueError(f"Unsupported desktop accent color: {accent_name}") from error


def _stylesheet():
    css = (
        f".{BUTTON_STYLE_CLASS} {{"
        " border-radius: 999px;"
        f" padding: {BUTTON_PADDING_VERTICAL}px {BUTTON_PADDING_HORIZONTAL}px;"
        f" min-width: {BUTTON_MIN_WIDTH}px;"
        f" min-height: {BUTTON_MIN_HEIGHT}px;"
        "}"
    )
    palette = _selected_accent_palette()
    if palette is None:
        return css

    normal, hover, active, foreground = palette
    css += (
        f"button.{BUTTON_STYLE_CLASS}.{ACCENT_BUTTON_STYLE_CLASS} {{"
        " background-image: none;"
        f" background-color: {normal};"
        f" border-color: {normal};"
        f" color: {foreground};"
        "}"
        f"button.{BUTTON_STYLE_CLASS}.{ACCENT_BUTTON_STYLE_CLASS}:hover {{"
        " background-image: none;"
        f" background-color: {hover};"
        f" border-color: {hover};"
        "}"
        f"button.{BUTTON_STYLE_CLASS}.{ACCENT_BUTTON_STYLE_CLASS}:active {{"
        " background-image: none;"
        f" background-color: {active};"
        f" border-color: {active};"
        "}"
    )
    return css


def initialize():
    global _application, _provider

    display = Gdk.Display.get_default()
    if display is None:
        raise RuntimeError("Cannot initialize GTK styling without an active display.")

    if _application is None:
        _application = Gtk.Application(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        _application.register(None)

    Gtk.Window.set_default_icon_name(APP_ICON_NAME)

    if _provider is None:
        _provider = Gtk.CssProvider()
        _provider.load_from_data(_stylesheet().encode("utf-8"))
        Gtk.StyleContext.add_provider_for_display(
            display,
            _provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


def create_window(title, width, height):
    window = Gtk.Window(title=title)
    window.set_application(_application)
    window.set_icon_name(APP_ICON_NAME)
    window.set_default_size(width, height)
    window.set_modal(True)
    window.set_resizable(False)
    window.add_css_class(WINDOW_STYLE_CLASS)
    return window


def create_content_box(spacing=CONTENT_SPACING, popup=False):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
    margin = POPUP_MARGIN if popup else WINDOW_MARGIN
    box.set_margin_top(margin)
    box.set_margin_bottom(margin)
    box.set_margin_start(margin)
    box.set_margin_end(margin)
    return box


def create_heading(text):
    heading = Gtk.Label(label=text)
    heading.add_css_class(HEADING_STYLE_CLASS)
    heading.set_xalign(0)
    return heading


def create_button(label, primary=False, destructive=False):
    button = Gtk.Button(label=label)
    button.add_css_class(BUTTON_STYLE_CLASS)
    if primary:
        button.add_css_class(THEME_COLOR_CLASSES["primary"])
    elif destructive:
        button.add_css_class(THEME_COLOR_CLASSES["destructive"])
    return button


def create_project_list():
    project_list = Gtk.ListBox()
    project_list.add_css_class(THEME_COLOR_CLASSES["project_selection"])
    return project_list


def create_button_row():
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=BUTTON_SPACING)
    box.set_halign(Gtk.Align.CENTER)
    return box
